# Describes the table 'MCPServer'.
class MCPServer:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    # Returns a dictionary representation of the MCPServer instance.
    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "id": row[0],
            "name": row[1]
        }