from crud.repos.BaseRepository import BaseRepository
from crud.models.Website import Website

import uuid

# Το repository για τη διαχείριση των λειτουργιών βάσης δεδομένων που σχετίζονται με τα Websites.
class WebsitesRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS Websites (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                domain TEXT UNIQUE
            )
        ''')

    def seed_db(self):
        super().seed_db(f'''
            INSERT OR IGNORE INTO Websites (id, name, description, domain) VALUES ("71625d2a-a4a3-41a9-9412-f5706341e010", "WebMCP Website", "This is an open directory of websites that expose interfaces to agents via WebMCP.", "https://webmcp.com");
            INSERT OR IGNORE INTO Websites (id, name, description, domain) VALUES ("71625d2a-a4a3-41a9-9412-f5706341e011", "Redbus", "Bus ticket booking platform of India.", "https://www.redbus.in");
        ''')

    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM Websites')
        return [Website.to_dict(row) for row in data]

    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM Websites WHERE id = \'{id}\'')
        return Website.to_dict(row) if row else None

    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = Website.to_invalid(data)
        if invalid:
            return invalid

        if self.exists('domain', data['domain']):
            return {'error': 'Υπάρχει ήδη Website με αυτό το domain.'}
        
        self.sql_command(f'INSERT INTO Websites (id, name, description, domain) VALUES (\'{data['id']}\', \'{data['name']}\', \'{data['description']}\', \'{data['domain']}\')')

        return data['id']

    def edit(self, id: str, data: dict):
        if not id:
            return {'error': 'Λείπει το ID του Website.'}

        data['id'] = id

        invalid = Website.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει Website με αυτό το ID.'}

        if self.exists('domain', data['domain']) and self.get_by_id(id)['domain'] != data['domain']:
            return {'error': 'Υπάρχει ήδη Website με αυτό το domain.'}

        set_clause = ', '.join([f'{key} = \'{value}\'' for key, value in data.items() if key != 'id'])
        self.sql_command(f'UPDATE Websites SET {set_clause} WHERE id = \'{id}\'')

        return id

    def delete(self, id: str):
        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει Website με αυτό το ID.'}
        
        self.sql_command(f'DELETE FROM Websites WHERE id = \'{id}\'')

    def exists(self, property_name: str, value: str):
        return self.sql_get_one(f'SELECT id FROM Websites WHERE {property_name} = \'{value}\'') is not None