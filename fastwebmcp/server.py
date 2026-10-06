import httpx

from fastmcp import FastMCP

# Define a wrapper for the MCP server
class FastWebMCP:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain
        self.client = httpx.AsyncClient(base_url=domain)

    #TODO: Implement method to initialize FastWebMCP from a Website instance.
    def from_website(self):
        self.mcp = FastMCP.from_openapi(
            client=self.client,
            name=self.name
        )