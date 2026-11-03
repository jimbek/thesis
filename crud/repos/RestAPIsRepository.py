from crud.repos.BaseRepository import BaseRepository
from crud.models.RestAPI import RestAPI

import uuid

# Το repository για τη διαχείριση των λειτουργιών βάσης δεδομένων που σχετίζονται με τα RestAPIs.
class RestAPIsRepository(BaseRepository):
    def __init__(self):
        super().__init__()
    
    def apply_migrations(self):
        super().apply_migrations('''
            CREATE TABLE IF NOT EXISTS RestAPIs (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                domain TEXT UNIQUE,
                openapi_spec TEXT
            )
        ''')

    def seed_db(self):
        super().seed_db('''
            INSERT OR IGNORE INTO RestAPIs (id, name, description, domain, openapi_spec) VALUES ("31625a2a-a9a3-41a9-9412-c5705341e070", "Ε.Δ.ΥΠ. - Εργαλεία Δημοσίων Υπαλλήλων", "Παρέχει endpoints για τον υπολογισμό μισθού δημοσίου υπαλλήλου και τη λήψη πληροφοριών αναφορικά με μισθοδοσία, επιδόματα, κρατήσεις και φορολογία.", "https://edyp.gr", "/v3/api-docs");
            INSERT OR IGNORE INTO RestAPIs (id, name, description, domain, openapi_spec) VALUES ("31625a2a-a9a3-41a9-9412-c5705341e071", "Petstore", "This is a sample Pet Store Server based on the OpenAPI 3.0 specification.", "https://petstore3.swagger.io", "/api/v3/openapi.json");
        ''')
    
    def get_all(self):
        data = self.sql_get_all(f'SELECT * FROM RestAPIs')
        return [RestAPI.to_dict(row) for row in data]

    def get_by_id(self, id: str):
        row = self.sql_get_one(f'SELECT * FROM RestAPIs WHERE id = \'{id}\'')
        return RestAPI.to_dict(row) if row else None
    
    def add(self, data: dict):
        data['id'] = str(uuid.uuid4())

        invalid = RestAPI.to_invalid(data)
        if invalid:
            return invalid

        if self.exists('domain', data['domain']):
            return {'error': 'Υπάρχει ήδη RestAPI με αυτό το domain.'}
        
        self.sql_command(f'INSERT INTO RestAPIs (id, name, description, domain, openapi_spec) VALUES (\'{data['id']}\', \'{data['name']}\', \'{data['description']}\', \'{data['domain']}\', \'{data['openapi_spec']}\')')

        return data['id']

    def edit(self, id: str, data: dict):
        if not id:
            return {'error': 'Λείπει το ID του RestAPI.'}

        data['id'] = id

        invalid = RestAPI.to_invalid(data)
        if invalid:
            return invalid

        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει RestAPI με αυτό το ID.'}

        if self.exists('domain', data['domain']) and self.get_by_id(id)['domain'] != data['domain']:
            return {'error': 'Υπάρχει ήδη RestAPI με αυτό το domain.'}
        
        set_clause = ', '.join([f'{key} = \'{value}\'' for key, value in data.items() if key != 'id'])
        self.sql_command(f'UPDATE RestAPIs SET {set_clause} WHERE id = \'{id}\'')

        return id
    
    def delete(self, id: str):
        if not self.exists('id', id):
            return {'error': 'Δεν υπάρχει RestAPI με αυτό το ID.'}
        
        mcp_servers = self.sql_get_all(f'SELECT id FROM MCPServers WHERE restapi_id = \'{id}\'')
        if mcp_servers and len(mcp_servers) > 0:
            return {'error': 'Δεν μπορείτε να διαγράψετε το RestAPI καθώς χρησιμοποιείται.'}
        
        self.sql_command(f'DELETE FROM RestAPIs WHERE id = \'{id}\'')
        return {}

    def exists(self, property_name: str, value: str):
        return self.sql_get_one(f'SELECT id FROM RestAPIs WHERE {property_name} = \'{value}\'') is not None