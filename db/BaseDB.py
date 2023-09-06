#!/usr/bin/env python
from typing import override, Iterator
import logging




class BaseDB:

    @override
    def __init__(self, *args, **kwargs) -> None:
        """Initialize database for connecting.
        """
        self.logger = logging.Logger(name="sqlite.log", level=logging.DEBUG)
        pass

    @override
    def bulk_create(self, *args, **kwargs) -> (bool, Iterator):
        """Inserts multiple data in database at once
        """
        pass

    @override
    def bulk_delete(self, *args, **kwargs) -> bool:
        """Delete multiple data in database at once
        """
        pass

    @override
    def bulk_update(self, *args, **kwargs) -> (bool, Iterator):
        """Updates multiple data in database at once
        """
        pass

    @override
    def create(self, *args, **kwargs) -> object:
        """Inserts new data in database
        """
        pass

    @override
    def delete(self, *args, **kwargs) -> bool:
        """Delete data in database
        """
        pass

    @override
    def filter(self, *args, **kwargs) -> Iterator:
        """Filters data in database by filtraions
        """
        pass

    @override
    def get(self, *args, **kwargs) -> Iterator:
        """Get specific data from database by filtraions
        """
        pass

    @override
    def get_or_create(self, *args, **kwargs) -> (bool, Iterator):
        """Get specific data from database by filtraions
        If it dosnt exists creates it
        """
        pass

    @override
    def update(self, *args, **kwargs) -> (bool, Iterator):
        """Get specific data from database by filtraions
        If it dosnt exists creates it
        """
        pass

    @override
    def create_table(self, *args, **kwargs) -> bool:
        """Create table in database. 
        """
        pass

    @override
    def commit(self, *args, **kwargs) -> bool:
        """Save (commit) the changes.
        """
        pass

    @override
    def close(self) -> bool:
        """We can also close the connection if we are done with it.
        Just be sure any changes have been committed or they will be lost.
        """
        pass


    @override
    def execute(self, *args, **kwargs):
        """Execute commands directly
        """
        pass