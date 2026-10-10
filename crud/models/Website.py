# Describes the model for a Website entity.
class Website:
    def __init__(self, id: str, name: str, description: str, domain: str):
        self.id = id
        self.name = name
        self.description = description
        self.domain = domain

    # Returns a dictionary representation of the Website instance.
    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "domain": row[3]
        }