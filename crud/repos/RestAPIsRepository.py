from .BaseRepository import BaseRepository
from models.RestAPI import RestAPI

import uuid

# Describes the repository for managing RestAPI-related database operations.
class RestAPIsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS RestAPI (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                domain TEXT,
                openapi_spec TEXT
            )
        ''')
    
    # Retrieves all 'RestAPI' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM RestAPI')
        
        return [RestAPI.to_dict(row) for row in data]
    
    # Adds a new 'RestAPI' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO RestAPI (id, name, description, domain, openapi_spec) VALUES ("{data['id']}", "{data['name']}", "{data['description']}", "{data['domain']}", "{data['openapi_spec']}")')

        return data['id']
    
    # Deletes a 'RestAPI' entry by its ID.
    def delete_by_id(self, id: str):
        self.sql_command(f'DELETE FROM RestAPI WHERE id = "{id}"')