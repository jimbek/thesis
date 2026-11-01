# Describes the model for a Process entity.
class Process:
    def __init__(self, id: str, pid: int, llm: str, agent_id: str, port: int):
        self.id = id
        self.pid = pid
        self.llm = llm
        self.agent_id = agent_id
        self.port = port

    @staticmethod
    def to_dict(row: dict):
        return {
            'id': row[0],
            'pid': row[1],
            'llm': row[2],
            'agent_id': row[3],
            'port': row[4],
            'agent_name': row[5]
        }

    # Returns a dictionary that describes an invalid Process instance.
    @staticmethod
    def to_invalid(data: dict = None):
        message = ""

        if data is None:
            message = "Δεν παρέχονται δεδομένα."

        if data.get("id") is None or data.get("id") == "":
            message = "Λείπει το ID."
        elif data.get("llm") is None or data.get("llm") == "":
            message = "Λείπει το LLM."
        elif data.get("agent_id") is None or data.get("agent_id") == "":
            message = "Λείπει το ID του Agent."
        elif data.get("port") is None or data.get("port") == "":
            message = "Λείπει η Θύρα."

        if message:
            return {
                "error": message
            }

        return None