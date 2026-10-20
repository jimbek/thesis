# Describes the model for an AI Agent entity.
class Agent:
    def __init__(self, id: str, name: str, system_prompt: str, mcp_server_id: str, llm: str):
        self.id = id
        self.name = name
        self.system_prompt = system_prompt
        self.mcp_server_id = mcp_server_id
        self.llm = llm

    @staticmethod
    def to_dict(row: dict):
        return {
            'id': row[0],
            'name': row[1],
            'system_prompt': row[2],
            'mcp_server_id': row[3],
            'llm': row[4],
            'source': row[5]
        }

    # Returns a dictionary that describes an invalid Agent instance.
    @staticmethod
    def to_invalid(data: dict = None):
        message = ""

        if data is None:
            message = "Δεν παρέχονται δεδομένα."

        if data.get("id") is None or data.get("id") == "":
            message = "Λείπει το ID."
        elif data.get("name") is None or data.get("name") == "":
            message = "Λείπει το Όνομα."
        elif data.get("system_prompt") is None or data.get("system_prompt") == "":
            message = "Λείπει το System Prompt."
        elif data.get("mcp_server_id") is None or data.get("mcp_server_id") == "":
            message = "Λείπει ο MCP Server."
        elif data.get("llm") is None or data.get("llm") == "":
            message = "Λείπει το LLM."

        if message:
            return {
                "error": message
            }

        return None