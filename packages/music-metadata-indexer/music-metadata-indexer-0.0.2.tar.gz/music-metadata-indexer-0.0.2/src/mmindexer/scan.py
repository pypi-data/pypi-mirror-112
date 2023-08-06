#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time 
from pathlib import Path
import logging 

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileSystemEventHandler

try: 
    import magic
    HAS_MAGIC = True
except ImportError: 
    HAS_MAGIC = False

from mmindexer.index import IndexDB, CannotImportFileError

def _import_song(db: IndexDB, filepath: str, logger:logging.Logger=None) -> None: 
    filepath =  Path(filepath) 

    try:  
        db.add_song(filepath)
        if logger is not None:
            logger.info("Added file at {} to index".format(str(filepath)))
    except CannotImportFileError: 
        if HAS_MAGIC and logger is not None:
            mimetype = magic.from_file(filepath, mime=True)
            if mimetype.split('/')[0].casefold() == "audio".casefold(): 
                logger.warning(""" 
                    Found file at {} that has a mimetype {} yet is incompatible with music_tag library. 
                    Check if the file also does not work with mutagen. """.format(str(filepath), mimetype))

class NewFileEventHandler(FileSystemEventHandler): 
    def __init__(self, db: IndexDB) -> None: 
        self.db = db
        
    def on_created(event) -> None: 
        if not event.is_directory: 
            _import_song(db, Path(event.src_path))

    def on_moved(event) -> None:
        path = Path(event.src_path)
        if not event.is_directory and db.file_not_in_songs(path): 
            _import_song(db, path)

class DiskScanner:
    def __init__(self, db: IndexDB, watchdir: Path, logger:logging.Logger=None) -> None:
        self.db = db 
        self.logger = logger 
        self.watchdir = watchdir
        self.observer = Observer()

    def start_watching(self) -> None: 
        self.observer.schedule(NewFileEventHandler(self.db), self.watchdir, recursive=True)
        self.observer.start()

    def stop_watching(self) -> None: 
       self.observer.stop()
       self.observer.join()

    def set_logger(self, logger:logging.Logger) -> None: 
        self.logger = logger

    def _files_in_tree(self, path: Path) -> None: 
        for child in path.resolve().iterdir(): 
            if child.is_file():
                yield child
            elif child.is_dir(): 
                yield self._files_in_tree() 

    def build_database(self) -> None: 
        for file in self._files_in_tree(self.watchdir): 
           _import_song(self.db, file) 

