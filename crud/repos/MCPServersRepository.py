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

    # Adds a new 'MCPServer' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict, restapi_id: str = None, website_id: str = None):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO MCPServers (id, name, restapi_id, website_id) VALUES ("{data['id']}", "{data['name']}", "{restapi_id}", "{website_id}")')

        return data['id']

    # Deletes a 'MCPServer' entry by its ID.
    def delete_by_id(self, id: str):
        self.sql_command(f'DELETE FROM MCPServers WHERE id = "{id}"')