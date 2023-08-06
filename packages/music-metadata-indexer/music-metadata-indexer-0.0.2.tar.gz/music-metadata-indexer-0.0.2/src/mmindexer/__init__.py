#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1-beta1"

import logging 
from time import sleep

from typing import Union
from mmindexer import scan, index 
from pathlib import PurePath, Path


def start(watchdir:Union[PurePath, str], dbpath: Union[PurePath, str], logger:logging.Logger=None) -> None: 
    watchdir = Path(watchdir) 
    dbpath = Path(dbpath)
    
    dbpath.unlink() #reset database
    db = index.IndexDB(dbpath)
    scanner = scan.DiskScanner(db, watchdir, logger) 

    db.create_tables()
    db.enable_fts()
    scanner.build_database()
    scanner.start_watching()
    while True:
        for row in db.get_rows("songs"):
            print(row)
        sleep(10)

if __name__ == "__main__":
    start("/home/ethan/git/music-metadata-indexer/sample", "/home/ethan/git/music-metadata-indexer/test.db")