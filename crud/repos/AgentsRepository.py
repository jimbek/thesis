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
                mcp_server_id TEXT,
                llm TEXT,
                FOREIGN KEY (mcp_server_id) REFERENCES MCPServers(id)
            )
        ''')

        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS AgentMCPServers (
                agent_id TEXT,
                mcp_server_id TEXT,
                FOREIGN KEY (agent_id) REFERENCES Agents(id),
                FOREIGN KEY (mcp_server_id) REFERENCES MCPServers(id)
            )
        ''')
    
    # Retrieves all 'Agent' entries.
    def get_all(self):
        data = self.sql_get_all(f'''
            SELECT Agents.id, Agents.name, Agents.system_prompt, Agents.llm, MCPServers.name
            FROM Agents
            LEFT JOIN MCPServers ON Agents.mcp_server_id = MCPServers.id
        ''')

        mcp_server_ids = self.sql_get_all(f'''
            SELECT agent_id, mcp_server_id
            FROM AgentMCPServers
        ''')

        mcp_server_ids_dict = {}
        for row in mcp_server_ids:
            agent_id = row[0]
            mcp_server_id = row[1]

            if agent_id not in mcp_server_ids_dict:
                mcp_server_ids_dict[agent_id] = []
                
            mcp_server_ids_dict[agent_id].append(mcp_server_id)

        return [Agent.to_dict(row, mcp_server_ids_dict.get(row[0], [])) for row in data]

    # Retrieves an 'AI Agent' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'''
            SELECT Agents.id, Agents.name, Agents.system_prompt, Agents.llm, MCPServers.name
            FROM Agents
            LEFT JOIN MCPServers ON Agents.mcp_server_id = MCPServers.id
            WHERE Agents.id = \'{id}\'
        ''')

        mcp_server_ids = self.sql_get_all(f'''
            SELECT agent_id, mcp_server_id
            FROM AgentMCPServers
            WHERE agent_id = \'{id}\'
        ''')

        return Agent.to_dict(row, [row[1] for row in mcp_server_ids]) if row else None

    # Adds a new 'AI Agent' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = Agent.to_invalid(data)
        if invalid:
            return invalid

        self.sql_command(f'INSERT INTO Agents (id, name, system_prompt, llm) VALUES (\'{data['id']}\', \'{data['name']}\', \'{data['system_prompt']}\', \'{data['llm']}\')')
        
        for mcp_server_id in data['mcp_server_ids']:
            self.sql_command(f'INSERT INTO AgentMCPServers (agent_id, mcp_server_id) VALUES (\'{data['id']}\', \'{mcp_server_id}\')')

        return data['id']

    # Edits an existing 'AI Agent' entry by its ID.
    def edit(self, id: str, data: dict):
        if not id:
            return {'error': 'Λείπει το ID του AI Agent.'}

        data['id'] = id

        invalid = Agent.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists(id):
            return {'error': 'Δεν υπάρχει AI Agent με αυτό το ID.'}
        
        set_clause = ', '.join([f'{key} = \'{value}\'' for key, value in data.items() if key != 'mcp_server_ids'])
        self.sql_command(f'UPDATE Agents SET {set_clause} WHERE id = \'{id}\'')

        self.sql_command(f'DELETE FROM AgentMCPServers WHERE agent_id = \'{id}\'')
        for mcp_server_id in data['mcp_server_ids']:
            self.sql_command(f'INSERT INTO AgentMCPServers (agent_id, mcp_server_id) VALUES (\'{id}\', \'{mcp_server_id}\')')

        return id

    # Deletes an 'AI Agent' entry by its ID.
    def delete(self, id: str):
        if not self.exists(id):
            return {'error': 'Δεν υπάρχει AI Agent με αυτό το ID.'}

        self.sql_command(f'DELETE FROM AgentMCPServers WHERE agent_id = \'{id}\'')
        self.sql_command(f'DELETE FROM Agents WHERE id = \'{id}\'')

    # Checks if an 'AI Agent' entry exists in the database by its ID.
    def exists(self, id: str):
        return self.sql_get_one(f'SELECT id FROM Agents WHERE id = \'{id}\'') is not None