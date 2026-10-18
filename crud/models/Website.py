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

    # Returns a dictionary that describes an invalid Website instance.
    @staticmethod
    def to_invalid(data: dict = None):
        message = ""
        
        if data is None:
            message = "Δεν παρέχονται δεδομένα."

        if data.get("id") is None or data.get("id") == "":
            message = "Λείπει το ID."
        elif data.get("name") is None or data.get("name") == "":
            message = "Λείπει το Όνομα."
        elif data.get("description") is None or data.get("description") == "":
            message = "Λείπει η Περιγραφή."
        elif data.get("domain") is None or data.get("domain") == "":
            message = "Λείπει το Domain."

        if message:
            return {
                "error": message
            }

        return None