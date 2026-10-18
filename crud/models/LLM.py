# Describes the model for an LLM (Large Language Model) entity.
class LLM:
    def __init__(self, name: str):
        self.name = name

    # Returns a dictionary representation of the LLM instance.
    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "name": row[0]
        }