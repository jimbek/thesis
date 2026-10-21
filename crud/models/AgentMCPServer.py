# Describes the model for an one-one AI Agent - MCP Server entity.
class AgentMCPServer:
    def __init__(self, agent_id: str, mcp_server_id: str):
        self.agent_id = agent_id
        self.mcp_server_id = mcp_server_id

    @staticmethod
    def to_dict(row: dict):
        return {
            'agent_id': row[0],
            'mcp_server_id': row[1]
        }

    # Returns a dictionary that describes an invalid Agent instance.
    @staticmethod
    def to_invalid(data: dict = None):
        message = ""

        if data is None:
            message = "Δεν παρέχονται δεδομένα."

        if data.get("agent_id") is None or data.get("agent_id") == "":
            message = "Λείπει ο AI Agent."
        elif data.get("mcp_server_id") is None or data.get("mcp_server_id") == "":
            message = "Λείπει ο MCP Server."

        if message:
            return {
                "error": message
            }

        return None