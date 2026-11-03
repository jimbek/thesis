# Περιγράφει το μοντέλο LLM (Large Language Model).
class LLM:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def to_dict(row: tuple = None):
        return {
            "name": row[0]
        }