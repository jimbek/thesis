# Implements the base repository class that all other repositories will inherit from.
# This class provides methods for applying migrations, seeding the database, and executing SQL commands.
import sqlite3

class BaseRepository:
    def __init__(self):
        # The filename of the database.
        self.db = 'database.db'
    
    # Checks if the given table exists in the database.
    def table_exists(self, table_name: str):
        command = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        data = self.sql_get_one(command)

        return data is not None

    # Executes the given SQL command to the database.
    # This is used to apply migrations to the database in order to automatically create the schema.
    def apply_migrations(self, command: str):
        self.sql_command(command)

    # Returns the filename of the database.
    def __get_connection__(self):
        return sqlite3.connect(self.db)

    # Opens a connection to the database, executes the given SQL command, and then closes the connection.
    def sql_command(self, command: str):
        connection = self.__get_connection__()
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        connection.close()
    
    # Opens a connection to the database, executes the given SQL command, retrieves one result, and then closes the connection.
    def sql_get_one(self, command: str):
        connection = self.__get_connection__()
        cursor = connection.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        connection.close()

        return data
    
    # Opens a connection to the database, executes the given SQL command, retrieves all results, and then closes the connection.
    def sql_get_all(self, command: str):
        connection = self.__get_connection__()
        cursor = connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        connection.close()

        return data