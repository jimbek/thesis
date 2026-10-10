# Applies database migrations
from crud.repos.RestAPIsRepository import RestAPIsRepository
from crud.repos.WebsitesRepository import WebsitesRepository
from crud.repos.MCPServersRepository import MCPServersRepository
from crud.repos.LLMsRepository import LLMsRepository
from crud.repos.AgentsRepository import AgentsRepository

restapis_repo = RestAPIsRepository()
websites_repo = WebsitesRepository()
mcpservers_repo = MCPServersRepository()
llms_repo = LLMsRepository()
agents_repo = AgentsRepository()

if restapis_repo.table_exists('RestAPIs') is False:
    restapis_repo.apply_migrations()

if websites_repo.table_exists('Websites') is False:
    websites_repo.apply_migrations()

if mcpservers_repo.table_exists('MCPServers') is False:
    mcpservers_repo.apply_migrations()

if llms_repo.table_exists('LLMs') is False:
    llms_repo.apply_migrations()

if agents_repo.table_exists('Agents') is False:
    agents_repo.apply_migrations()