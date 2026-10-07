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
                domain TEXT
            )
        ''')

    # Retrieves all 'Website' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM Websites')
        
        return [Website.to_dict(row) for row in data]

    # Adds a new 'Website' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO Websites (id, name, description, domain) VALUES ("{data['id']}", "{data['name']}", "{data['description']}", "{data['domain']}")')

        return data['id']

    # Deletes a 'Website' entry by its ID.
    def delete_by_id(self, id: str):
        self.sql_command(f'DELETE FROM Websites WHERE id = "{id}"')