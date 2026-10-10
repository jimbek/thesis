from crud.repos.BaseRepository import BaseRepository
from crud.models.Website import Website

import uuid

# Describes the repository for managing Website-related database operations.
class WebsitesRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS Websites (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                domain TEXT UNIQUE
            )
        ''')

    # Retrieves all 'Website' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM Websites')
        
        return [Website.to_dict(row) for row in data]

    # Retrieves a 'Website' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM Websites WHERE id = "{id}"')
        return Website.to_dict(row) if row else None

    # Adds a new 'Website' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO Websites (id, name, description, domain) VALUES ("{data['id']}", "{data['name']}", "{data['description']}", "{data['domain']}")')

        return data['id']

    # Edits an existing 'Website' entry by its ID.
    def edit(self, id: str, data: dict):
        set_clause = ', '.join([f'{key} = "{value}"' for key, value in data.items()])
        self.sql_command(f'UPDATE Websites SET {set_clause} WHERE id = "{id}"')

    # Checks if a 'Website' entry exists in the database by its domain.
    def exists(self, domain: str):
        return self.sql_get_one(f'SELECT id FROM Websites WHERE domain = "{domain}"') is not None

    # Deletes a 'Website' entry by its ID.
    def delete(self, id: str):
        self.sql_command(f'DELETE FROM Websites WHERE id = "{id}"')