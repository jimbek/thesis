# Describes the model for an AI Agent entity.
class Agent:
    def __init__(self, id: str, name: str, system_prompt: str, llm_id: str, mcp_server_id: str):
        self.id = id
        self.name = name
        self.system_prompt = system_prompt
        self.llm_id = llm_id
        self.mcp_server_id = mcp_server_id

    @staticmethod
    def to_dict(row: dict):
        return {
            'id': row['id'],
            'name': row['name'],
            'system_prompt': row['system_prompt'],
            'llm_id': row.get('llm_id'),
            'mcp_server_id': row.get('mcp_server_id')
        }