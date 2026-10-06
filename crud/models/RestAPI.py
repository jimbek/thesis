# Describes the table 'RestAPI'.
class RestAPI:
    def __init__(self, id: str, name: str, description: str, domain: str, openapi_spec: str):
        self.id = id
        self.name = name
        self.description = description
        self.domain = domain
        self.openapi_spec = openapi_spec

    # Returns a dictionary representation of the RestAPI instance.
    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "domain": row[3],
            "openapi_spec": row[4]
        }