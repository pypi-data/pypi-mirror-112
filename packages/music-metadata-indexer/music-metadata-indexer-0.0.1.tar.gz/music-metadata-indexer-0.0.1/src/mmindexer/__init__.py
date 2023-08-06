#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1-beta1"

import logging 


from . import scan, index 
from pathlib import PurePath, Path


def start(watchdir, logger:logging.logger=None): 
    if instanceof(watchdir, str): 
        watchdir = Path(watchdir)
    elif not instanceof(watchdir, PurePath): 
        raise ValueError("Invalid watchdir value, must be pathlib or string value") 
    
    db = index.IndexDB(watchdir)
    scanner = scan.DiskScanner(db, watchdir, logger) 

    db.create_tables()
    scanner.build_database(db)
    db.enable_fts()
    scanner.start_watching()

