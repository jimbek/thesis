from crud.repos.BaseRepository import BaseRepository
from crud.models.Process import Process

import uuid

# Describes the repository for managing Process-related database operations.
class ProcessesRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS Processes (
                id TEXT PRIMARY KEY,
                agent_id TEXT,
                port INTEGER,
                FOREIGN KEY (agent_id) REFERENCES Agents(id)
            )
        ''')
    
    # Retrieves all 'Process' entries.
    def get_all(self):
        data = self.sql_get_all(f'''
            SELECT Processes.id, Processes.agent_id, Processes.port, agent.name AS agent_name
            FROM Processes
            LEFT JOIN Agents AS agent ON Processes.agent_id = agent.id
        ''')
        
        return [Process.to_dict(row) for row in data]

    # Retrieves a 'Process' entry by its ID.
    def get_by_id(self, id: str):
        row = self.sql_get_one(f'''
            SELECT Processes.id, Processes.agent_id, Processes.port, agent.name AS agent_name
            FROM Processes
            LEFT JOIN Agents AS agent ON Processes.agent_id = agent.id
            WHERE Processes.id = \'{id}\'
        ''')
        return Process.to_dict(row) if row else None

    # Retrieves 'Process' entries by their AI Agent ID.
    def get_by_agent_id(self, id: str):
        data = self.sql_get_all(f'''
            SELECT Processes.id, Processes.agent_id, Processes.port, agent.name AS agent_name
            FROM Processes
            LEFT JOIN Agents AS agent ON Processes.agent_id = agent.id
            WHERE Processes.agent_id = \'{id}\'
        ''')
        return [Process.to_dict(row) for row in data]

    # Adds a new 'Process' entry to the database and returns the ID of the newly created entry.
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = Process.to_invalid(data)
        if invalid:
            return invalid

        self.sql_command(f'INSERT INTO Processes (id, agent_id, port) VALUES (\'{data['id']}\', \'{data['agent_id']}\', \'{data['port']}\')')

        return data['id']

    # Edits an existing 'Process' entry by its ID.
    def edit(self, id: str, data: dict):
        if not id:
            return {'error': 'Λείπει το ID της διαδικασίας.'}
    
        data['id'] = id

        invalid = Process.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει διαδικασία με αυτό το ID.'}
        
        set_clause = ', '.join([f'{key} = \'{value}\'' for key, value in data.items()])
        self.sql_command(f'UPDATE Processes SET {set_clause} WHERE id = \'{id}\'')

        return id
    # Deletes a 'Process' entry by its ID.
    def delete(self, id: str):
        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει διαδικασία με αυτό το ID.'}
        
        self.sql_command(f'DELETE FROM Processes WHERE id = \'{id}\'')

    # Checks if a 'Process' entry exists in the database by one of its properties.
    def exists(self, property_name: str, value: str):
        return self.sql_get_one(f'SELECT id FROM Processes WHERE {property_name} = \'{value}\'') is not None