from crud.repos.BaseRepository import BaseRepository
from crud.models.LLM import LLM

import uuid

# Describes the repository for managing LLM-related database operations.
class LLMsRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS LLMs (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE
            )
        ''')
    
    # Retrieves all 'LLM' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM LLMs')
        
        return [LLM.to_dict(row) for row in data]

    # Retrieves an 'LLM' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM LLMs WHERE id = "{id}"')
        return LLM.to_dict(row) if row else None

    # Adds a new 'LLM' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict, restapi_id: str = None, website_id: str = None):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO LLMs (id, name) VALUES ("{data['id']}", "{data['name']}")')

        return data['id']

    # Edits an existing 'LLM' entry by its ID.
    def edit(self, id: str, data: dict):
        set_clause = ', '.join([f'{key} = "{value}"' for key, value in data.items()])
        self.sql_command(f'UPDATE LLMs SET {set_clause} WHERE id = "{id}"')

    # Checks if an 'LLM' entry exists in the database by its name.
    def exists(self, name: str):
        return self.sql_get_one(f'SELECT id FROM LLMs WHERE name = "{name}"') is not None

    # Deletes a 'LLM' entry by its ID.
    def delete(self, id: str):
        self.sql_command(f'DELETE FROM LLMs WHERE id = "{id}"')