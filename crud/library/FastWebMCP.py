from playwright.sync_api import sync_playwright

# Define a wrapper for the MCP server
class FastWebMCP:
    # Initialize FastWebMCP from a Website instance.
    @staticmethod
    def list_tools(website: str):
        with sync_playwright() as p:
            # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
            browser = p.chromium.launch(channel="msedge")

            # Create a new page and navigate to the website
            page = browser.new_page()
            page.goto(website)

            # Retrieve the tools from the model context using JavaScript
            tools = page.evaluate("document.modelContext.getTools()")

            # For each tool, return the name and description
            tool_list = []
            for tool in tools:
                tool_name = tool['name']
                tool_description = tool['description']
                tool_list.append({"name": tool_name, "description": tool_description})

            browser.close()

            return tool_list