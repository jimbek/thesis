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
            'id': row['id'],
            'name': row['name'],
            'system_prompt': row['system_prompt'],
            'mcp_server_id': row.get('mcp_server_id'),
            'llm': row.get('llm')
        }