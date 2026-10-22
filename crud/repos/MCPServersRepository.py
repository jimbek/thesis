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

    def seed_db(self):
        super().seed_db('''
            INSERT OR IGNORE INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("41275a2a-a9a3-81d9-9412-b5715342e070", "Ε.Δ.ΥΠ MCP Server", "Instructions for Ε.Δ.ΥΠ MCP Server", "31625a2a-a9a3-41a9-9412-c5705341e070", NULL);
            INSERT OR IGNORE INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("41275a2a-a9a3-81d9-9412-b5715342e071", "ΚΗΜΔΗΣ MCP Server", "Instructions for ΚΗΜΔΗΣ MCP Server", "31625a2a-a9a3-41a9-9412-c5705341e071", NULL);
            INSERT OR IGNORE INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("41275a2a-a9a3-81d9-9412-b5715342e072", "Petstore MCP Server", "Instructions for Petstore MCP Server", "31625a2a-a9a3-41a9-9412-c5705341e073", NULL);
            INSERT OR IGNORE INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("41275a2a-a9a3-81d9-9412-b5715342e073", "WebMCP MCP Server", "Instructions for WebMCP MCP Server", NULL, "71625d2a-a4a3-41a9-9412-f5706341e010");
            INSERT OR IGNORE INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("41275a2a-a9a3-81d9-9412-b5715342e074", "OpenAI MCP Server", "Instructions for OpenAI MCP Server", NULL, "71625d2a-a4a3-41a9-9412-f5706341e011");
            INSERT OR IGNORE INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES ("41275a2a-a9a3-81d9-9412-b5715342e075", "Target.com MCP Server", "Instructions for Target.com MCP Server", NULL, "71625d2a-a4a3-41a9-9412-f5706341e013");
        ''')
    
    # Retrieves all 'MCPServer' entries including the name of the associated REST API and website.
    def get_all(self):
        data = self.sql_get_all(f'''
            SELECT MCPServers.id, MCPServers.name, MCPServers.instructions, MCPServers.restapi_id, MCPServers.website_id, restapi.name AS restapi_name, website.name AS website_name
            FROM MCPServers
            LEFT JOIN RestAPIs AS restapi ON MCPServers.restapi_id = restapi.id
            LEFT JOIN Websites AS website ON MCPServers.website_id = website.id
        ''')
        
        return [MCPServer.to_dict(row) for row in data]

    # Retrieves an 'MCPServer' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'''
            SELECT MCPServers.id, MCPServers.name, MCPServers.instructions, MCPServers.restapi_id, MCPServers.website_id, restapi.name AS restapi_name, website.name AS website_name
            FROM MCPServers
            LEFT JOIN RestAPIs AS restapi ON MCPServers.restapi_id = restapi.id
            LEFT JOIN Websites AS website ON MCPServers.website_id = website.id
            WHERE MCPServers.id = \'{id}\'
        ''')
        return MCPServer.to_dict(row) if row else None

    # Adds a new 'MCPServer' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = MCPServer.to_invalid(data)
        if invalid:
            return invalid

        self.sql_command(f'INSERT INTO MCPServers (id, name, instructions, restapi_id, website_id) VALUES (\'{data['id']}\', \'{data['name']}\', \'{data['instructions']}\', \'{data['restapi_id']}\', \'{data['website_id']}\')')

        return data['id']

    # Edits an existing 'MCPServer' entry by its ID.
    def edit(self, id: str, data: dict):
        if not id:
            return {'error': 'Λείπει το ID του MCP Server.'}
    
        data['id'] = id

        invalid = MCPServer.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει MCP Server με αυτό το ID.'}
        
        set_clause = ', '.join([f'{key} = \'{value}\'' for key, value in data.items()])
        self.sql_command(f'UPDATE MCPServers SET {set_clause} WHERE id = \'{id}\'')

        return id
    # Deletes a 'MCPServer' entry by its ID.
    def delete(self, id: str):
        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει MCP Server με αυτό το ID.'}
        
        self.sql_command(f'DELETE FROM MCPServers WHERE id = \'{id}\'')

    # Checks if an 'MCPServer' entry exists in the database by one of its properties.
    def exists(self, property_name: str, value: str):
        return self.sql_get_one(f'SELECT id FROM MCPServers WHERE {property_name} = \'{value}\'') is not None