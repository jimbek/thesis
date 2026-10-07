# Applies database migrations
from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.WebsitesRepository import WebsitesRepository
from crud.repos.MCPServersRepository import MCPServersRepository

restapis_repo = RestAPIsRepository()
websites_repo = WebsitesRepository()
mcpservers_repo = MCPServersRepository()

if restapis_repo.table_exists('RestAPIs') is False:
    restapis_repo.apply_migrations()

if websites_repo.table_exists('Websites') is False:
    websites_repo.apply_migrations()

if mcpservers_repo.table_exists('MCPServers') is False:
    mcpservers_repo.apply_migrations()