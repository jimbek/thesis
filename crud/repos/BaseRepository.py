import sqlite3

# Το βασικό repository που κληρονομούν όλα τα άλλα repositories.
class BaseRepository:
    def __init__(self):
        # Το όνομα του αρχείου της βάσης δεδομένων.
        self.db = 'database.db'
    
    # Ελέγχει αν υπάρχει ο πίνακας με το δοσμένο όνομα στη βάση δεδομένων.
    def table_exists(self, table_name: str):
        command = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        data = self.sql_get_one(command)

        return data is not None

    # Εκτελεί το SQL command στη βάση δεδομένων.
    # Χρησιμοποιείται για να δημιουργηθεί αυτόματα το σχήμα της βάσης δεδομένων.
    def apply_migrations(self, command: str):
        self.sql_command(command)

    # Εκτελεί το SQL command στη βάση δεδομένων.
    # Χρησιμοποιείται για την αρχικοποίηση της βάσης δεδομένων με αρχικά δεδομένα.
    def seed_db(self, command: str):
        commands = command.split(';')

        for command in commands:
            self.sql_command(command)

    # Ανοίγει μια σύνδεση με τη βάση δεδομένων, εκτελεί το SQL command και στη συνέχεια κλείνει τη σύνδεση.
    def sql_command(self, command: str):
        connection = self.__get_connection__()
        cursor = connection.cursor()
        cursor.execute(command)
        connection.commit()
        connection.close()
    
    # Ανοίγει μια σύνδεση με τη βάση δεδομένων, εκτελεί το SQL command, κλείνει τη σύνδεση κι επιστρέφει ένα αποτέλεσμα.
    def sql_get_one(self, command: str):
        connection = self.__get_connection__()
        cursor = connection.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        connection.close()

        return data
    
    # Ανοίγει μια σύνδεση με τη βάση δεδομένων, εκτελεί το SQL command, κλείνει τη σύνδεση κι επιστρέφει όλα τα αποτελέσματα.
    def sql_get_all(self, command: str):
        connection = self.__get_connection__()
        cursor = connection.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        connection.close()

        return data

    # Δημιουργεί τη σύνδεση με τη βάση δεδομένων.
    def __get_connection__(self):
        return sqlite3.connect(self.db)