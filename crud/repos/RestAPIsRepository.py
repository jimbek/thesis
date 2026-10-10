from crud.repos.BaseRepository import BaseRepository
from crud.models.RestAPI import RestAPI

import uuid

# Describes the repository for managing RestAPI-related database operations.
class RestAPIsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS RestAPIs (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                domain TEXT UNIQUE,
                openapi_spec TEXT
            )
        ''')
    
    # Retrieves all 'RestAPI' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM RestAPIs')
        
        return [RestAPI.to_dict(row) for row in data]

    # Retrieves a 'RestAPI' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM RestAPIs WHERE id = "{id}"')
        return RestAPI.to_dict(row) if row else None
    
    # Adds a new 'RestAPI' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO RestAPIs (id, name, description, domain, openapi_spec) VALUES ("{data['id']}", "{data['name']}", "{data['description']}", "{data['domain']}", "{data['openapi_spec']}")')

        return data['id']

    # Edits an existing 'RestAPI' entry by its ID.
    def edit(self, id: str, data: dict):
        set_clause = ', '.join([f'{key} = "{value}"' for key, value in data.items()])
        self.sql_command(f'UPDATE RestAPIs SET {set_clause} WHERE id = "{id}"')

    # Checks if a 'RestAPI' entry exists in the database by its domain.
    def exists(self, domain: str):
        return self.sql_get_one(f'SELECT id FROM RestAPIs WHERE domain = "{domain}"') is not None
    
    # Deletes a 'RestAPI' entry by its ID.
    def delete(self, id: str):
        self.sql_command(f'DELETE FROM RestAPIs WHERE id = "{id}"')