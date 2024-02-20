#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os


storage_type = os.getenv('HBNB_TYPE_STORAGE')


if storage_type == "db":
    from models.engine import db_storage
    storage = db_storage.DB_storage()
else:
    from models.engine import file_storage
    storage = file_storage.FileStorage()
storage.reload()