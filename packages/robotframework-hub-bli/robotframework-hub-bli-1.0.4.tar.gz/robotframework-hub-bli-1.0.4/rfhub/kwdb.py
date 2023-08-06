"""keywordtable - an SQLite database of keywords

Keywords can be loaded from resource files, test suite files,
and libdoc-formatted xml, or from python libraries. These
are referred to as "collections".

"""

import json
import logging
import os
import re
import sqlite3
from operator import itemgetter

import robot.libraries
from robot.libdocpkg import LibraryDocumentation
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

"""
Note: It seems to be possible for watchdog to fire an event
when a file is modified, but before the file is _finished_
being modified (ie: you get the event when some other program
writes the first byte, rather than waiting until the other
program closes the file)

For that reason, we might want to mark a collection as
"dirty", and only reload after some period of time has
elapsed? I haven't yet experienced this problem, but
I haven't done extensive testing.
"""


class WatchdogHandler(PatternMatchingEventHandler):
    patterns = ["*.robot", "*.txt", "*.py", "*.tsv", "*.resource"]

    def __init__(self, kwdb, path):
        PatternMatchingEventHandler.__init__(self)
        self.kwdb = kwdb
        self.path = path

    def on_created(self, event):
        # monitor=False because we're already monitoring
        # ancestor of the file that was created. Duh.
        self.kwdb.add(event.src_path, monitor=False)

    def on_deleted(self, event):
        # FIXME: need to implement this
        pass

    def on_modified(self, event):
        self.kwdb.on_change(event.src_path, event.event_type)


class KeywordTable(object):
    """A SQLite database of keywords"""

    def __init__(self, dbfile=":memory:", poll=False):
        self.db = sqlite3.connect(dbfile, check_same_thread=False)
        self.log = logging.getLogger(__name__)
        self._create_db()
        self.top_level_path = None
        self.combined_libdoc = None
        self.libdoc_path = None
        self.libdoc_src_name = None
        # self.log.warning("I'm warnin' ya!")

        # set up watchdog observer to monitor changes to
        # keyword files (or more correctly, to directories
        # of keyword files)
        self.observer = PollingObserver() if poll else Observer()
        self.observer.start()

    def set_top_level_path(self, name):
        self.top_level_path = name

    def get_top_level_path(self):
        return self.top_level_path

    def add(self, name):
        """Add a folder, library (.py) or resource file (.robot, .tsv, .txt, .resource) to the database
        """

        if os.path.isdir(name):
            if not os.path.basename(name).startswith("."):
                self.add_folder(name)

        elif os.path.isfile(name):
            if ((self._looks_like_resource_file(name)) or
                    (self._looks_like_libdoc_file(name)) or
                    (self._looks_like_library_file(name))):
                self.add_file(name)
        else:
            # let's hope it's a library name!
            self.add_library(name)

    # noinspection PyUnusedLocal
    def on_change(self, path, event_type):
        """Respond to changes in the file system

        This method will be given the path to a file that
        has changed on disk. We need to reload the keywords
        from that file
        """
        # I can do all this work in a sql statement, but
        # for debugging it's easier to do it in stages.
        sql = """SELECT collection_id
                 FROM collection_table
                 WHERE path == ?
        """
        cursor = self._execute(sql, (path,))
        results = cursor.fetchall()
        # there should always be exactly one result, but
        # there's no harm in using a loop to process the
        # single result
        for result in results:
            collection_id = result[0]
            # remove all keywords in this collection
            sql = """DELETE from keyword_table
                     WHERE collection_id == ?
            """
            # noinspection PyUnusedLocal
            cursor = self._execute(sql, (collection_id,))
            self._load_keywords(collection_id, path=path)

    def _load_keywords(self, collection_id, path=None, libdoc=None):
        """Load a collection of keywords

           One of path or libdoc needs to be passed in...
        """
        if libdoc is None and path is None:
            raise (Exception("You must provide either a path or libdoc argument"))

        if libdoc is None:
            libdoc = LibraryDocumentation(path)

        if len(libdoc.keywords) > 0:
            for keyword in libdoc.keywords:
                self._add_keyword(collection_id, keyword.name, keyword.doc, keyword.args)

    @staticmethod
    def removeprefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    def get_file(self, path):
        """Generate library documentation for specified file"""
        libdoc = LibraryDocumentation(path)
        if self.get_top_level_path() is None:
            src_name = libdoc.name
        else:
            src_name = self.removeprefix(libdoc.source, self.get_top_level_path())
            src_name = self.removeprefix(src_name, "/")
        return path, src_name, libdoc

    def add_combined_file(self, path, src_name, libdoc):
        if len(libdoc.keywords) > 0:
            try:
                _named_args = libdoc.named_args
            except AttributeError:
                # Attribute was dropped in Robot 4.x
                _named_args = None
            collection_id = self.add_collection(path, src_name, libdoc.type,
                                                libdoc.doc, libdoc.version,
                                                libdoc.scope, _named_args,
                                                libdoc.doc_format)
            self._load_keywords(collection_id, libdoc=libdoc)

    def add_file(self, path):
        """Add a resource file or library file to the database"""
        (path, src_name, libdoc) = self.get_file(path)
        self.add_combined_file(path, src_name, libdoc)

    def add_library(self, name):
        """Add a library to the database

        This method is for adding a library by name (eg: "BuiltIn")
        rather than by a file.
        """
        libdoc = LibraryDocumentation(name)
        if len(libdoc.keywords) > 0:
            try:
                _named_args = libdoc.named_args
            except AttributeError:
                # Attribute was dropped in Robot 4.x
                _named_args = None

            collection_id = self.add_collection(libdoc.source, libdoc.name, libdoc.type,
                                                libdoc.doc, libdoc.version,
                                                libdoc.scope, _named_args,
                                                libdoc.doc_format)
            self._load_keywords(collection_id, libdoc=libdoc)

    def add_folder(self, dirname, watch=True, exclude_patterns=None):
        """Recursively add all files in a folder to the database

        By "all files" I mean, "all files that are resource files
        or library files". It will silently ignore files that don't
        look like they belong in the database. Pity the fool who
        uses non-standard suffixes.

        N.B. folders with names that begin with '." will be skipped
        """
        _exclude_patterns = exclude_patterns if exclude_patterns is not None else []
        _initial_combine = self.combined_libdoc
        _ignore_file = os.path.join(dirname, ".rfhubignore")
        if os.path.exists(_ignore_file):
            # noinspection PyBroadException
            try:
                with open(_ignore_file, "r") as f:
                    for line in f.readlines():
                        line = line.strip()
                        if re.match(r'^\s*#', line):
                            continue
                        if len(line) > 0:
                            _exclude_patterns.append(line)
            except:
                pass

        # Support umbrella resource files, i.e. resource file
        # that collects multiple other resource files and should
        # be used as include by coding standard.
        if _initial_combine is None:
            combine_as_file = None
            combine_file = os.path.join(dirname, ".rfhubcombine")
            if os.path.exists(combine_file):
                # noinspection PyBroadException
                try:
                    with open(combine_file, "r") as f:
                        for line in f.readlines():
                            line = line.strip()
                            if re.match(r'^\s*#', line):
                                continue
                            if len(line.strip()) > 0:
                                combine_as_file = line
                                combine_as_path = os.path.join(dirname, combine_as_file)
                except:
                    pass

            if combine_as_file is not None:
                if self.combined_libdoc is None:
                    if os.path.exists(combine_as_path):
                        try:
                            (self.libdoc_path, self.libdoc_src_name, self.combined_libdoc) = self.get_file(
                                combine_as_path)
                            _exclude_patterns.append(combine_as_file)
                        except Exception as e:
                            self.log.error(
                                e.__class__.__name__ + ": Error to read top-level resource file " +
                                combine_as_path + "\n" + str(e))

        # Get list of files and directories, remove matching exclude patterns
        dirlist = os.listdir(dirname)
        dirlist = [x for x in dirlist if not any(re.search(r, x) for r in _exclude_patterns)]

        for filename in sorted(dirlist):
            path = os.path.join(dirname, filename)
            (basename, ext) = os.path.splitext(filename.lower())

            try:
                if os.path.isdir(path):
                    if not basename.startswith("."):
                        if os.access(path, os.R_OK):
                            self.add_folder(path, watch=False, exclude_patterns=_exclude_patterns)
                else:
                    if ext in (".xml", ".robot", ".txt", ".py", ".tsv", ".resource"):
                        if os.access(path, os.R_OK):
                            if self.combined_libdoc is None:
                                self.add(path)
                            else:
                                (__path, __src_name, __libdoc) = self.get_file(path)
                                if __libdoc is not None:
                                    if len(__libdoc.keywords) > 0:
                                        self.combined_libdoc.keywords.extend(__libdoc.keywords)
            except Exception as e:
                # I really need to get the logging situation figured out.
                self.log.error(e.__class__.__name__ + ": Error to process " + path + "\n" + str(e))

        if _initial_combine is None \
                and self.combined_libdoc is not None:
            # Write documentation for umbrella resource and reset instance variables
            self.add_combined_file(self.libdoc_path, self.libdoc_src_name, self.combined_libdoc)
            self.libdoc_path = None
            self.libdoc_src_name = None
            self.combined_libdoc = None

        # FIXME:
        # instead of passing a flag around, I should just keep track
        # of which folders we're watching, and don't add watchers for
        # any subfolders. That will work better in the case where
        # the user accidentally starts up the hub giving the same
        # folder, or a folder and it's children, on the command line...
        if watch:
            # add watcher on normalized path
            dirname = os.path.abspath(dirname)
            event_handler = WatchdogHandler(self, dirname)
            self.observer.schedule(event_handler, dirname, recursive=True)

    def add_collection(self, path, c_name, c_type, c_doc, c_version="unknown",
                       c_scope="", c_namedargs="yes", c_doc_format="ROBOT"):
        """Insert data into the collection table"""
        if path is not None:
            # We want to store the normalized form of the path in the
            # database
            path = os.path.abspath(path)

        cursor = self.db.cursor()
        cursor.execute("""
            INSERT INTO collection_table
                (name, type, version, scope, namedargs, path, doc, doc_format)
            VALUES
                (?,?,?,?,?,?,?,?)
        """, (c_name, c_type, c_version, c_scope, c_namedargs, path, c_doc, c_doc_format))
        collection_id = cursor.lastrowid
        return collection_id

    def add_installed_libraries(self):
        """Add any installed libraries that we can find

        We do this by looking in the `libraries` folder where
        robot is installed. If you have libraries installed
        in a non-standard place, this won't pick them up.
        """

        libdir = os.path.dirname(robot.libraries.__file__)
        loaded = []
        for filename in os.listdir(libdir):
            if filename.endswith(".py") or filename.endswith(".pyc"):
                libname, ext = os.path.splitext(filename)
                if (libname.lower() not in loaded and
                        not self._should_ignore(libname)):

                    try:
                        self.add(libname)
                        loaded.append(libname.lower())
                    except Exception as e:
                        # need a better way to log this...
                        self.log.debug("unable to add library: " + str(e))

        # Use information from 'robotframework_*dist-info to get installed Robot libraries
        basedir = os.path.dirname(robot.__file__)
        basedir = os.path.dirname(basedir)
        for filename in os.listdir(basedir):
            fullpath = os.path.join(basedir, filename)
            filepath = os.path.join(fullpath, 'top_level.txt')
            if filename.startswith('robotframework_') \
                    and filename.endswith('.dist-info') \
                    and os.path.exists(filepath):
                # noinspection PyBroadException
                try:
                    with open(filepath, "r") as f:
                        for line in f.readlines():
                            line = line.strip()
                            if re.match(r'^\s*#', line):
                                continue
                            if len(line) > 0:
                                library = line
                except:
                    pass

                if (library.lower() not in loaded and
                        not self._should_ignore(library)):
                    try:
                        self.add(library)
                        loaded.append(library.lower())
                    except Exception as e:
                        self.log.debug("unable to add external library %s: %s" %
                                       (library, str(e)))

    def get_collection(self, collection_id):
        """Get a specific collection"""
        sql = """SELECT collection.collection_id, collection.type,
                        collection.name, collection.path,
                        collection.doc,
                        collection.version, collection.scope,
                        collection.namedargs,
                        collection.doc_format
                 FROM collection_table as collection
                 WHERE collection_id == ? OR collection.name like ?
        """
        cursor = self._execute(sql, (collection_id, collection_id))
        # need to handle the case where we get more than one result...
        sql_result = cursor.fetchone()
        return {
            "collection_id": sql_result[0],
            "type": sql_result[1],
            "name": sql_result[2],
            "path": sql_result[3],
            "doc": sql_result[4],
            "version": sql_result[5],
            "scope": sql_result[6],
            "namedargs": sql_result[7],
            "doc_format": sql_result[8]
        }

    def get_collections(self, pattern="*", libtype="*"):
        """Returns a list of collection name/summary tuples"""

        sql = """SELECT collection.collection_id, collection.name, collection.doc,
                        collection.type, collection.path
                 FROM collection_table as collection
                 WHERE name like ?
                 AND type like ?
                 ORDER BY collection.name
              """

        cursor = self._execute(sql, (self._glob_to_sql(pattern),
                                     self._glob_to_sql(libtype)))
        sql_result = cursor.fetchall()

        return [{"collection_id": result[0],
                 "name": result[1],
                 "synopsis": result[2].split("\n")[0],
                 "type": result[3],
                 "path": result[4]
                 } for result in sql_result]

    def get_keyword_data(self, collection_id):
        sql = """SELECT keyword.keyword_id, keyword.name, keyword.args, keyword.doc
                 FROM keyword_table as keyword
                 WHERE keyword.collection_id == ?
                 ORDER BY keyword.name
              """
        cursor = self._execute(sql, (collection_id,))
        return cursor.fetchall()

    def get_keyword(self, collection_id, name):
        """Get a specific keyword from a library"""
        sql = """SELECT keyword.name, keyword.args, keyword.doc
                 FROM keyword_table as keyword
                 WHERE keyword.collection_id == ?
                 AND keyword.name like ?
              """
        cursor = self._execute(sql, (collection_id, name))
        # We're going to assume no library has duplicate keywords
        # While that in theory _could_ happen, it never _should_,
        # and you get what you deserve if it does.
        row = cursor.fetchone()
        if row is not None:
            return {"name": row[0],
                    "args": json.loads(row[1]),
                    "doc": row[2],
                    "collection_id": collection_id
                    }
        return {}

    def get_keyword_hierarchy(self, pattern="*"):
        """Returns all keywords that match a glob-style pattern

        The result is a list of dictionaries, sorted by collection
        name.

        The pattern matching is insensitive to case. The function
        returns a list of (library_name, keyword_name,
        keyword_synopsis tuples) sorted by keyword name

        """

        sql = """SELECT collection.collection_id, collection.name, collection.path,
                 keyword.name, keyword.doc
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND keyword.name like ?
                 ORDER by collection.name, collection.collection_id, keyword.name
             """
        cursor = self._execute(sql, (self._glob_to_sql(pattern),))
        libraries = []
        current_library = None
        for row in cursor.fetchall():
            (c_id, c_name, c_path, k_name, k_doc) = row
            if c_id != current_library:
                current_library = c_id
                libraries.append({"name": c_name, "collection_id": c_id, "keywords": [], "path": c_path})
            libraries[-1]["keywords"].append({"name": k_name, "doc": k_doc})
        return libraries

    def search(self, pattern="*", mode="both"):
        """Perform a pattern-based search on keyword names and documentation

        The pattern matching is insensitive to case. The function
        returns a list of tuples of the form library_id, library_name,
        keyword_name, keyword_synopsis, sorted by library id,
        library name, and then keyword name

        If a pattern begins with "name:", only the keyword names will
        be searched. Otherwise, the pattern is searched for in both
        the name and keyword documentation.

        You can limit the search to a single library by specifying
        "in:" followed by the name of the library or resource
        file. For example, "screenshot in:SeleniumLibrary" will only
        search for the word 'screenshot' in the SeleniumLibrary.

        """
        pattern = self._glob_to_sql(pattern)

        cond = "(keyword.name like ? OR keyword.doc like ?)"
        args = [pattern, pattern]
        if mode == "name":
            cond = "(keyword.name like ?)"
            args = [pattern, ]

        sql = """SELECT collection.collection_id, collection.name, keyword.name, keyword.doc
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND %s
                 ORDER by collection.collection_id, collection.name, keyword.name
             """ % cond

        cursor = self._execute(sql, args)
        result = [(row[0], row[1], row[2], row[3].strip().split("\n")[0])
                  for row in cursor.fetchall()]
        return list(set(result))

    def get_keywords(self, pattern="*"):
        """Returns all keywords that match a glob-style pattern

        The pattern matching is insensitive to case. The function
        returns a list of (library_name, keyword_name,
        keyword_synopsis tuples) sorted by keyword name

        """

        sql = """SELECT collection.collection_id, collection.name,
                        keyword.name, keyword.doc, keyword.args
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND keyword.name like ?
                 ORDER by collection.name, keyword.name
             """
        pattern = self._glob_to_sql(pattern)
        cursor = self._execute(sql, (pattern,))
        result = [(row[0], row[1], row[2], row[3], row[4])
                  for row in cursor.fetchall()]
        return list(sorted(set(result), key=itemgetter(2)))

    def reset(self):
        """Remove all data from the database, but leave the tables intact"""
        self._execute("DELETE FROM collection_table")
        self._execute("DELETE FROM keyword_table")

    @staticmethod
    def _looks_like_library_file(name):
        return name.endswith(".py")

    @staticmethod
    def _looks_like_libdoc_file(name):
        """Return true if an xml file looks like a libdoc file"""
        # inefficient since we end up reading the file twice,
        # but it's fast enough for our purposes, and prevents
        # us from doing a full parse of files that are obviously
        # not libdoc files
        if name.lower().endswith(".xml"):
            with open(name, "r") as f:
                # read the first few lines; if we don't see
                # what looks like libdoc data, return false
                data = f.read(200)
                index = data.lower().find("<keywordspec ")
                if index > 0:
                    return True
        return False

    @staticmethod
    def _looks_like_resource_file(name):
        """Return true if the file has a keyword table but not a testcase table"""
        # inefficient since we end up reading the file twice,
        # but it's fast enough for our purposes, and prevents
        # us from doing a full parse of files that are obviously
        # not robot files

        if re.search(r'__init__.(txt|robot|html|tsv)$', name):
            # These are initialize files, not resource files
            return False

        found_keyword_table = False
        if (name.lower().endswith(".robot") or
                name.lower().endswith(".txt") or
                name.lower().endswith(".tsv") or
                name.lower().endswith(".resource")):

            with open(name, "r") as f:
                data = f.read()
                for match in re.finditer(r'^\*+\s*(Test Cases?|(?:User )?Keywords?)',
                                         data, re.MULTILINE | re.IGNORECASE):
                    if re.match(r'Test Cases?', match.group(1), re.IGNORECASE):
                        # if there's a test case table, it's not a keyword file
                        return False

                    if (not found_keyword_table and
                            re.match(r'(User )?Keywords?', match.group(1), re.IGNORECASE)):
                        found_keyword_table = True
        return found_keyword_table

    @staticmethod
    def _should_ignore(name):
        """Return True if a given library name should be ignored

        This is necessary because not all files we find in the library
        folder are libraries. I wish there was a public robot API
        for "give me a list of installed libraries"...
        """
        _name = name.lower()
        return (_name.startswith("deprecated") or
                _name.startswith("_") or
                _name in ("remote", "reserved",
                          "dialogs_py", "dialogs_ipy", "dialogs_jy"))

    def _execute(self, *args):
        """Execute an SQL query

        This exists because I think it's tedious to get a cursor and
        then use a cursor.
        """
        cursor = self.db.cursor()
        cursor.execute(*args)
        return cursor

    @staticmethod
    def _convert_to_dict(obj):
        """
          A function takes in a custom object and returns a dictionary representation of the object.
          This dict representation includes meta data such as the object's module and class names.
          """

        #  Populate the dictionary with object meta data
        obj_dict = {
            "__class__": obj.__class__.__name__,
            "__module__": obj.__module__
        }

        # Populate the dictionary with object properties, but
        # remove non-serializable '_setter__types'
        _temp_dict = obj.__dict__
        _temp_dict.pop('_setter__types', None)
        obj_dict.update(_temp_dict)

        return obj_dict

    def _add_keyword(self, collection_id, name, doc, args):
        """Insert data into the keyword table

        'args' should be a list, but since we can't store a list in an
        sqlite database we'll make it json we can can convert it back
        to a list later.
        """
        argstring = json.dumps(args, default=self._convert_to_dict)
        self.db.execute("""
            INSERT INTO keyword_table
                (collection_id, name, doc, args)
            VALUES
                (?,?,?,?)
        """, (collection_id, name, doc, argstring))

    def _create_db(self):

        if not self._table_exists("collection_table"):
            self.db.execute("""
                CREATE TABLE collection_table
                (collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name          TEXT COLLATE NOCASE,
                 type          COLLATE NOCASE,
                 version       TEXT,
                 scope         TEXT,
                 namedargs     TEXT,
                 path          TEXT,
                 doc           TEXT,
                 doc_format    TEXT)
            """)
            self.db.execute("""
                CREATE INDEX collection_index
                ON collection_table (name)
            """)

        if not self._table_exists("keyword_table"):
            self.db.execute("""
                CREATE TABLE keyword_table
                (keyword_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                 name          TEXT COLLATE NOCASE,
                 collection_id INTEGER,
                 doc           TEXT,
                 args          TEXT)
            """)
            self.db.execute("""
                CREATE INDEX keyword_index
                ON keyword_table (name)
            """)

    @staticmethod
    def _glob_to_sql(string):
        """Convert glob-like wildcards to SQL wildcards

        * becomes %
        ? becomes _
        % becomes \%
        \\ remains \\
        \* remains \*
        \? remains \?

        This also adds a leading and trailing %, unless the pattern begins with
        ^ or ends with $
        """

        # What's with the chr(1) and chr(2) nonsense? It's a trick to
        # hide \* and \? from the * and ? substitutions. This trick
        # depends on the substitutiones being done in order.  chr(1)
        # and chr(2) were picked because I know those characters
        # almost certainly won't be in the input string
        table = ((r'\\', chr(1)), (r'\*', chr(2)), (r'\?', chr(3)),
                 (r'%', r'\%'), (r'?', '_'), (r'*', '%'),
                 (chr(1), r'\\'), (chr(2), r'\*'), (chr(3), r'\?'))

        for (a, b) in table:
            string = string.replace(a, b)

        string = string[1:] if string.startswith("^") else "%" + string
        string = string[:-1] if string.endswith("$") else string + "%"

        return string

    def _table_exists(self, name):
        cursor = self.db.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='%s'
        """ % name)
        return len(cursor.fetchall()) > 0
