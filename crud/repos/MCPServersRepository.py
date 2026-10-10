from crud.repos.BaseRepository import BaseRepository
from crud.models.MCPServer import MCPServer

import uuid

# Describes the repository for managing MCPServer-related database operations.
class MCPServersRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS MCPServers (
                id TEXT PRIMARY KEY,
                name TEXT,
                instructions TEXT,
                restapi_id TEXT,
                website_id TEXT,
                FOREIGN KEY (restapi_id) REFERENCES RestAPIs(id),
                FOREIGN KEY (website_id) REFERENCES Websites(id)
            )
        ''')
    
    # Retrieves all 'MCPServer' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM MCPServers')
        
        return [MCPServer.to_dict(row) for row in data]

    # Retrieves an 'MCPServer' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM MCPServers WHERE id = "{id}"')
        return MCPServer.to_dict(row) if row else None

    # Adds a new 'MCPServer' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict, restapi_id: str = None, website_id: str = None):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("{data['id']}", "{data['name']}", "{data['instructions']}", "{restapi_id}", "{website_id}")')

        return data['id']

    # Edits an existing 'MCPServer' entry by its ID.
    def edit(self, id: str, data: dict):
        set_clause = ', '.join([f'{key} = "{value}"' for key, value in data.items()])
        self.sql_command(f'UPDATE MCPServers SET {set_clause} WHERE id = "{id}"')

    # Checks if an 'MCPServer' entry exists in the database by its domain.
    def exists(self, domain: str):
        return self.sql_get_one(f'SELECT id FROM MCPServers WHERE name = "{domain}"') is not None

    # Deletes a 'MCPServer' entry by its ID.
    def delete(self, id: str):
        self.sql_command(f'DELETE FROM MCPServers WHERE id = "{id}"')