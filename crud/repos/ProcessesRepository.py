from crud.repos.BaseRepository import BaseRepository
from crud.models.Process import Process

import uuid

# Το repository για τη διαχείριση των λειτουργιών βάσης δεδομένων που σχετίζονται με τα Processes.
class ProcessesRepository(BaseRepository):
    def __init__(self):
        super().__init__()

    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS Processes (
                id TEXT PRIMARY KEY,
                pid INTEGER,
                llm TEXT,
                agent_id TEXT,
                port INTEGER UNIQUE,
                FOREIGN KEY (agent_id) REFERENCES Agents(id)
            )
        ''')
    
    def get_all(self):
        data = self.sql_get_all(f'''
            SELECT Processes.id, Processes.pid, Processes.llm, Processes.agent_id, Processes.port, agent.name AS agent_name
            FROM Processes
            LEFT JOIN Agents AS agent ON Processes.agent_id = agent.id
        ''')
        
        return [Process.to_dict(row) for row in data]

    def get_by_id(self, id: str):
        row = self.sql_get_one(f'''
            SELECT Processes.id, Processes.pid, Processes.llm, Processes.agent_id, Processes.port, agent.name AS agent_name
            FROM Processes
            LEFT JOIN Agents AS agent ON Processes.agent_id = agent.id
            WHERE Processes.id = \'{id}\'
        ''')
        return Process.to_dict(row) if row else None

    def get_by_agent_id(self, id: str):
        data = self.sql_get_all(f'''
            SELECT Processes.id, Processes.pid, Processes.llm, Processes.agent_id, Processes.port, agent.name AS agent_name
            FROM Processes
            LEFT JOIN Agents AS agent ON Processes.agent_id = agent.id
            WHERE Processes.agent_id = \'{id}\'
        ''')
        return [Process.to_dict(row) for row in data]

    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = Process.to_invalid(data)
        if invalid:
            return invalid

        if self.exists('port', str(data['port'])):
            return {'error': 'Υπάρχει ήδη διαδικασία με αυτόν τον port.'}

        self.sql_command(f'INSERT INTO Processes (id, pid, llm, agent_id, port) VALUES (\'{data['id']}\', \'{data['pid']}\', \'{data['llm']}\', \'{data['agent_id']}\', \'{data['port']}\')')

        return data['id']

    def edit(self, id: str, data: dict):
        if not id:
            return {'error': 'Λείπει το ID της διαδικασίας.'}
    
        data['id'] = id

        invalid = Process.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει διαδικασία με αυτό το ID.'}

        if self.exists('port', str(data['port'])) and self.get_by_id(id)['port'] != data['port']:
            return {'error': 'Υπάρχει ήδη διαδικασία με αυτόν τον port.'}
        
        set_clause = ', '.join([f'{key} = \'{value}\'' for key, value in data.items()])
        self.sql_command(f'UPDATE Processes SET {set_clause} WHERE id = \'{id}\'')

        return id

    def delete(self, id: str):
        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει διαδικασία με αυτό το ID.'}
        
        self.sql_command(f'DELETE FROM Processes WHERE id = \'{id}\'')

    def clear_all(self):
        self.sql_command('DELETE FROM Processes')

    def exists(self, property_name: str, value: str):
        return self.sql_get_one(f'SELECT id FROM Processes WHERE {property_name} = \'{value}\'') is not None