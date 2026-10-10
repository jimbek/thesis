# Describes the model for an LLM (Large Language Model) entity.
class LLM:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    # Returns a dictionary representation of the LLM instance.
    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "id": row[0],
            "name": row[1]
        }