# Describes the model for an MCPServer entity.
class MCPServer:
    def __init__(self, id: str, name: str, instructions: str, restapi_id: str = None, website_id: str = None):
        self.id = id
        self.name = name
        self.instructions = instructions
        self.restapi_id = restapi_id
        self.website_id = website_id

    # Returns a dictionary representation of the MCPServer instance.
    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "id": row[0],
            "name": row[1],
            "instructions": row[2],
            "restapi_id": row[3],
            "website_id": row[4]
        }