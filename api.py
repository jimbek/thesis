# Runs the CRUD operations for the application.
from crud.routes.RestAPIs import get_restapis, create_restapi
from crud.routes.Websites import get_websites, create_website
from crud.routes.MCPServers import get_mcpservers, create_mcpserver

from flask import Flask

app = Flask(__name__)

app.add_url_rule('/restapis', 'get_restapis', get_restapis, methods=['GET'])
app.add_url_rule('/restapis', 'create_restapi', create_restapi, methods=['POST'])

app.add_url_rule('/websites', 'get_websites', get_websites, methods=['GET'])
app.add_url_rule('/websites', 'create_website', create_website, methods=['POST'])

app.add_url_rule('/mcpservers', 'get_mcpservers', get_mcpservers, methods=['GET'])
app.add_url_rule('/mcpservers', 'create_mcpserver', create_mcpserver, methods=['POST'])

@app.route('/')
def index():
    return '''
        Welcome!
    '''

if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', port = 5000)