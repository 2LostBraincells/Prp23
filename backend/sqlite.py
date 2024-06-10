import sqlite3
from typing import Protocol
from pathlib import Path

INSERT_PERSON_QUERY = \
"""
INSERT INTO person (name)
"""


class InsertableObject(Protocol):
    def _database_insert(self, cursor: sqlite3.Cursor):
        ...


    def _database_update(self, cursor: sqlite3.Cursor, **kwargs):
        ...


    def _database_delete(self, cursor: sqlite3.Cursor):
        ...



class Database():

    slots = [
        "__conn",
        "__cursor",
    ]

    def __init__(self, filename: str = "example.db"):
        filepath = Path(filename)

        if not filepath.exists():
            filepath.touch()

        self.__conn = sqlite3.connect(filename)
        self.__init_tables()

        self.__cursor = self.__conn.cursor()


    def __del__(self):
        self.__cursor.close()
        self.__conn.close()


    def __init_tables(self):
        schemapath = Path("src/sql_schema/database_schema.sql")
        if not schemapath.exists():
            raise FileNotFoundError("Schema file not found")

        schema = schemapath.read_text()

        cursor = self.__conn.cursor()

        try:    
            cursor.executescript(schema)
        except sqlite3.Error as e:
            self.__conn.rollback()
            raise e


    def insert(self, obj: InsertableObject):
        obj._database_insert(self.__cursor)
        self.__conn.commit()


    def update(self, obj: InsertableObject, **kwargs):
        obj._database_update(self.__cursor, **kwargs)
        self.__conn.commit()


    def delete(self, obj: InsertableObject):
        obj._database_delete(self.__cursor)
        self.__conn.commit()




db = Database("elever.db")
