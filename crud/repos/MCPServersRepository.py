from .BaseRepository import BaseRepository
from models.MCPServer import MCPServer

import uuid

# Describes the repository for managing MCPServer-related database operations.
class MCPServersRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS MCPServer (
                id TEXT PRIMARY KEY,
                name TEXT
            )
        ''')
    
    # Retrieves all 'MCPServer' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM MCPServer')
        
        return [MCPServer.to_dict(row) for row in data]

    # Adds a new 'MCPServer' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO MCPServer (id, name) VALUES ("{data['id']}", "{data['name']}")')

        return data['id']

    # Deletes a 'MCPServer' entry by its ID.
    def delete_by_id(self, id: str):
        self.sql_command(f'DELETE FROM MCPServer WHERE id = "{id}"')