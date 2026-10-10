from crud.repos.BaseRepository import BaseRepository
from crud.models.Agent import Agent

import uuid

# Describes the repository for managing Agent-related database operations.
class AgentsRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS Agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                system_prompt TEXT,
                llm_id TEXT,
                mcp_server_id TEXT,
                FOREIGN KEY (llm_id) REFERENCES LLMs(id),
                FOREIGN KEY (mcp_server_id) REFERENCES MCPServers(id)
            )
        ''')
    
    # Retrieves all 'Agent' entries.
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM Agents')
        
        return [Agent.to_dict(row) for row in data]

    # Retrieves an 'Agent' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM Agents WHERE id = "{id}"')
        return Agent.to_dict(row) if row else None

    # Adds a new 'Agent' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict, llm_id: str = None, mcp_server_id: str = None):
        data['id'] = str(uuid.uuid4())

        self.sql_command(f'INSERT INTO Agents (id, name, system_prompt, llm_id, mcp_server_id) VALUES ("{data['id']}", "{data['name']}", "{data['system_prompt']}", "{llm_id}", "{mcp_server_id}")')

        return data['id']

    # Edits an existing 'Agent' entry by its ID.
    def edit(self, id: str, data: dict):
        set_clause = ', '.join([f'{key} = "{value}"' for key, value in data.items()])
        self.sql_command(f'UPDATE Agents SET {set_clause} WHERE id = "{id}"')

    # Checks if an 'Agent' entry exists in the database by its ID.
    def exists(self, id: str):
        return self.sql_get_one(f'SELECT id FROM Agents WHERE id = "{id}"') is not None

    # Deletes an 'Agent' entry by its ID.
    def delete(self, id: str):
        self.sql_command(f'DELETE FROM Agents WHERE id = "{id}"')