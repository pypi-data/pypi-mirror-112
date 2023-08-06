#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from pathlib import Path
from typing import Generator, Iterable


import music_tag
from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

class CursorContextManager: 
    def __init__(self, db: sqlite3.Connection) -> None: 
        self.db = db

    def __enter__(self) -> sqlite3.Cursor: 
        self.cursor = self.db.cursor()
        return self.cursor 

    def __exit__(self, exc_class, exc, traceback) -> None: 
        self.db.commit()

class InvalidTableError(Exception):
    """ Raised when a table is not deemed as a valid existing table by IndexDB. 
    Distinct from sqlite_utils.db.NotFoundError, which is for a failure to retrieve some id (i.e. by rowid). 
    """
    pass

class DatabaseNotInitalised(Exception): 
    pass

class CannotImportFileError(Exception): 
    pass

class IndexDB: 
    def __init__(self, path:Path) -> None:
        self.sqdb = sqlite3.connect(path)
        self.db = Database(self.sqdb, use_counts_table=True)
        self.valid_tables = set()

    def _check_valid_table(self, table: str) -> None:
        if table not in self.valid_tables: 
                raise InvalidTableError("Table {} is invalid".format(table))

    def _check_valid_table_set(self, tables: set) -> None: 
        if not tables.issubset(self.valid_tables):
            raise InvalidTableError("Table {} is invalid".format(table))

    def _check_initalised(self) -> None: 
        if not self.is_properly_initalised():
            raise DatabaseNotInitalised()

    def is_properly_initalised(self) -> None:
        all_tables = set(self.db.table_names())

        for table in self.valid_tables:
            if table not in all_tables:
                return False
            if self.db[table].detect_fts() is None:
                return False

        return True
    
    def create_tables(self) -> None: 
        """ Notes on table values: 
                Overall
                    - artistid and albumid are unique, and start at one, incrementing by one for each album 
                    - In SQLite, a column with type INTEGER PRIMARY KEY is an alias for the ROWID 
                        (i.e. artistid and albumid id are rowid for those tables respectively)
                    - All tables are searchable by name via LTS 
                (Artists table)
                    - artistid 1 is hardcoded to Various Artists
                Albums Table
                Songs Table 
                    - index is the songs position on the album
                    - Can also search filepaths
        """

        self.db["artists"].create({
           "artistid": int,
           "name": str
        }, pk="artistid" )
        self.db["artists"].insert({"artistid": 1, "name": "Various Artists"}) # hard coded for direct usage

        self.db["albums"].create({
            "albumid" : int, 
            "artistid": int, 
            "name": str,
        }, pk="albumid" )

        self.db["songs"].create({
            "index": int, 
            "albumid": int, 
            "artistid": int, 
            "name": str, 
            "filepath": str, 
        })
    
        self.db.enable_counts()    
        self.valid_tables.update({"artists", "albums", "songs"})
        return self.valid_tables

    def enable_fts(self) -> None: 
        for table in self.valid_tables:
            try:
                if table != "songs": 
                    cols = ["name"]
                else:
                    cols = ["name", "filepath"]
                self.db[table].enable_fts(cols, create_triggers=True, tokenize="unicode61")
            except sqlite3.OperationalError: # allow already configured LTS to silently fail
                pass 

    def search(self, table: str, string: str) -> Generator:
        self._check_valid_table(table)
        return self.db[table].search(string)

    def file_not_in_songs(self, filepath: Path): 
        for result in self.db["songs"].sarch(str(filepath)): 
            if result.casefold()  == str(filepath).casefold(): 
                return False 
        return True 

    def get_row_counts(self) -> dict: 
        return self.db.cached_counts()

    def get_last_rowid(self) -> int:
        """ Returns rowid/int pk of last insert operation on the database """
        return self.db.execute('SELECT last_insert_rowid()').fetchone()[0]

    def get_row_by_id(self, table: str, albumid: int) -> dict: 
        self._check_valid_table(table)
        try: 
            return self.db[table].get(albumid)
        except NotFoundError: 
            return None

    def get_rows(self, table:str) -> Generator: 
        self._check_valid_table(table)
        for row in self.db[table].rows:
            yield row 

    def add_song(self, filepath: Path) -> int: 
        try: 
            metadata = music_tag.load_file(filepath)
        except NotImplementedError:
            raise CannotImportFileError() 
        self._check_initalised()
        artistid, albumid, index = None, None, None

        if len(metadata['artist'].values) > 1:  
            artistid = 1  
        elif len(metadata['artist'].values) == 1: 
            artist = metadata['artist'].first.casefold() 
            for match in self.search("artists", artist): 
                if match["name"] == artist:
                    artistid = match["artistid"] 
                    break 
                else: 
                    self.db["artists"].insert({"name": artist})
                    artistid = self.get_last_rowid()

        album = metadata["album"].first.casefold()
        if len(metadata["album"]) >= 1: 
            for match in self.search("albums", album): 
                if match["name"] == album: 
                    albumid = match["albumid"]
                    break 
            else: 
                self.db["albums"].insert({
                    "artistid": artistid, 
                    "name": album
                })
                albumid = self.get_last_rowid()

        if len(metadata['tracknumber'].values) >= 1: 
            index = metadata['tracknumber'].first

        if len(metadata['title'].values) >= 1: 
            name = metadata["title"].first 
        else: 
            name = filepath.stem

        self.db["songs"].insert({
            "index": index,
            "albumid": albumid,
            "artistid": artistid, 
            "name": name, 
            "filepath": str(filepath) 
        })

        return self.get_last_rowid() 




