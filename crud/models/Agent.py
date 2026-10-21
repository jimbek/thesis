# Describes the model for an AI Agent entity.
class Agent:
    def __init__(self, id: str, name: str, system_prompt: str, llm: str, mcp_server_ids: list[str]):
        self.id = id
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        self.mcp_server_ids = mcp_server_ids

    @staticmethod
    def to_dict(row: dict, mcp_server_ids: list[str]):
        return {
            'id': row[0],
            'name': row[1],
            'system_prompt': row[2],
            'llm': row[3],
            'source': row[4],
            'mcp_server_ids': mcp_server_ids
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
        elif data.get("llm") is None or data.get("llm") == "":
            message = "Λείπει το LLM."
        elif data.get("mcp_server_ids") is None or not data.get("mcp_server_ids"):
            message = "Λείπουν οι MCP Servers."

        if message:
            return {
                "error": message
            }

        return None