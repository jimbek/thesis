# Runs the CRUD operations for the application.
from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.WebsitesRepository import WebsitesRepository
from crud.repos.MCPServersRepository import MCPServersRepository
from crud.repos.AgentsRepository import AgentsRepository
from crud.routes.RestAPIs import get_restapis, add_restapi, edit_restapi, delete_restapi
from crud.routes.Websites import get_websites, get_website_by_id, add_website, edit_website, delete_website
from crud.routes.MCPServers import get_mcpservers, add_mcpserver, edit_mcpserver, delete_mcpserver
from crud.routes.Agents import get_agents, add_agent, edit_agent, delete_agent

from flask import Flask

restapis_repo = RestAPIsRepository()
websites_repo = WebsitesRepository()
mcpservers_repo = MCPServersRepository()
agents_repo = AgentsRepository()

# Seed the db
if restapis_repo.table_exists('RestAPIs') is False:
    restapis_repo.apply_migrations()

if websites_repo.table_exists('Websites') is False:
    websites_repo.apply_migrations()

if mcpservers_repo.table_exists('MCPServers') is False:
    mcpservers_repo.apply_migrations()

if agents_repo.table_exists('Agents') is False:
    agents_repo.apply_migrations()

app = Flask(__name__)

app.add_url_rule('/restapis', 'get_restapis', get_restapis, methods=['GET'])
app.add_url_rule('/restapis', 'add_restapi', add_restapi, methods=['POST'])
app.add_url_rule('/restapis/<id>', 'edit_restapi', edit_restapi, methods=['PUT'])
app.add_url_rule('/restapis/<id>', 'delete_restapi', delete_restapi, methods=['DELETE'])

app.add_url_rule('/websites', 'get_websites', get_websites, methods=['GET'])
app.add_url_rule('/websites/<id>', 'get_website_by_id', get_website_by_id, methods=['GET'])
app.add_url_rule('/websites', 'add_website', add_website, methods=['POST'])
app.add_url_rule('/websites/<id>', 'edit_website', edit_website, methods=['PUT'])
app.add_url_rule('/websites/<id>', 'delete_website', delete_website, methods=['DELETE'])

app.add_url_rule('/mcpservers', 'get_mcpservers', get_mcpservers, methods=['GET'])
app.add_url_rule('/mcpservers', 'add_mcpserver', add_mcpserver, methods=['POST'])
app.add_url_rule('/mcpservers/<id>', 'edit_mcpserver', edit_mcpserver, methods=['PUT'])
app.add_url_rule('/mcpservers/<id>', 'delete_mcpserver', delete_mcpserver, methods=['DELETE'])

app.add_url_rule('/agents', 'get_agents', get_agents, methods=['GET'])
app.add_url_rule('/agents', 'add_agent', add_agent, methods=['POST'])
app.add_url_rule('/agents/<id>', 'edit_agent', edit_agent, methods=['PUT'])
app.add_url_rule('/agents/<id>', 'delete_agent', delete_agent, methods=['DELETE'])

@app.route('/')
def index():
    return '''
        Welcome!
    '''

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5000)