from crud.repos.BaseRepository import BaseRepository
from crud.models.Agent import Agent

import uuid

# Το repository για τη διαχείριση των λειτουργιών βάσης δεδομένων που σχετίζονται με τους AI Agents.
class AgentsRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS Agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                system_prompt TEXT
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

    def seed_db(self):
        super().seed_db('''
            INSERT OR IGNORE INTO Agents (id, name, system_prompt) VALUES ("41265a2a-f9a3-81d9-5412-b5715342e070", "EDYP AI Agent", "Provide public employee related information. Use only available tools. Return results in HTML format if necessary.");
            INSERT OR IGNORE INTO Agents (id, name, system_prompt) VALUES ("41265a2a-f9a3-81d9-5412-b5715342e071", "Webmcp AI Agent", "Provide information based on the WebMCP directory. Use only available tools. Return results in HTML format if necessary.");
            INSERT OR IGNORE INTO Agents (id, name, system_prompt) VALUES ("41265a2a-f9a3-81d9-5412-b5715342e072", "Jobbbler AI Agent", "Provide open technology roles related information. Use only available tools. Return results in HTML format if necessary.");
        ''')

        super().seed_db('''
            INSERT OR IGNORE INTO AgentMCPServers (agent_id, mcp_server_id) VALUES ("41265a2a-f9a3-81d9-5412-b5715342e070", "41275a2a-a9a3-81d9-9412-b5715342e070");
            INSERT OR IGNORE INTO AgentMCPServers (agent_id, mcp_server_id) VALUES ("41265a2a-f9a3-81d9-5412-b5715342e071", "41275a2a-a9a3-81d9-9412-b5715342e071");
            INSERT OR IGNORE INTO AgentMCPServers (agent_id, mcp_server_id) VALUES ("41265a2a-f9a3-81d9-5412-b5715342e072", "41275a2a-a9a3-81d9-9412-b5715342e072");
        ''')
    
    def get_all(self):
        data = self.sql_get_all(f'''
            SELECT Agents.id, Agents.name, Agents.system_prompt
            FROM Agents
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

    def get_by_id(self, id: str):
        row = self.sql_get_one(f'''
            SELECT Agents.id, Agents.name, Agents.system_prompt
            FROM Agents
            WHERE Agents.id = \'{id}\'
        ''')

        mcp_server_ids = self.sql_get_all(f'''
            SELECT agent_id, mcp_server_id
            FROM AgentMCPServers
            WHERE agent_id = \'{id}\'
        ''')

        return Agent.to_dict(row, [row[1] for row in mcp_server_ids]) if row else None

    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = Agent.to_invalid(data)
        if invalid:
            return invalid

        self.sql_command(f'INSERT INTO Agents (id, name, system_prompt) VALUES (\'{data['id']}\', \'{data['name']}\', \'{data['system_prompt']}\')')
        
        for mcp_server_id in data['mcp_server_ids']:
            self.sql_command(f'INSERT INTO AgentMCPServers (agent_id, mcp_server_id) VALUES (\'{data['id']}\', \'{mcp_server_id}\')')

        return data['id']

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

    def delete(self, id: str):
        if not self.exists(id):
            return {'error': 'Δεν υπάρχει AI Agent με αυτό το ID.'}

        self.sql_command(f'DELETE FROM AgentMCPServers WHERE agent_id = \'{id}\'')
        self.sql_command(f'DELETE FROM Agents WHERE id = \'{id}\'')

    def exists(self, id: str):
        return self.sql_get_one(f'SELECT id FROM Agents WHERE id = \'{id}\'') is not None