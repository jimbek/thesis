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

        invalid = RestAPI.to_invalid(data)
        if invalid:
            return invalid

        if self.exists('domain', data['domain']):
            return {'message': 'Υπάρχει ήδη RestAPI με αυτό το domain.'}

        self.sql_command(f'INSERT INTO RestAPIs (id, name, description, domain, openapi_spec) VALUES ("{data['id']}", "{data['name']}", "{data['description']}", "{data['domain']}", "{data['openapi_spec']}")')

        return data['id']

    # Edits an existing 'RestAPI' entry by its ID.
    def edit(self, data: dict):
        invalid = RestAPI.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists('id', data['id']):
            return {'message': 'Δεν υπάρχει RestAPI με αυτό το ID.'}

        if self.exists('domain', data['domain']) and self.get_by_id(data['id'])['domain'] != data['domain']:
            return {'message': 'Υπάρχει ήδη RestAPI με αυτό το domain.'}
        
        set_clause = ', '.join([f'{key} = "{value}"' for key, value in data.items() if key != 'id'])
        self.sql_command(f'UPDATE RestAPIs SET {set_clause} WHERE id = "{data.get("id")}"')
    
    # Deletes a 'RestAPI' entry by its ID.
    def delete(self, id: str):
        if not self.exists('id', id):
            return {'message': 'Δεν υπάρχει RestAPI με αυτό το ID.'}
        
        self.sql_command(f'DELETE FROM RestAPIs WHERE id = "{id}"')

    # Checks if a 'RestAPI' entry exists in the database by one of its properties.
    def exists(self, property_name: str, value: str):
        return self.sql_get_one(f'SELECT id FROM RestAPIs WHERE {property_name} = "{value}"') is not None