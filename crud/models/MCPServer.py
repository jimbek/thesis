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
            "website_id": row[4],
            "type": "Rest API" if row[3] is not None and row[3] != "" and row[3] != "None" else "Website",
            "source": row[5] if row[3] is not None and row[3] != "" and row[3] != "None" else row[6]
        }

    # Returns a dictionary that describes an invalid MCPServer instance.
    @staticmethod
    def to_invalid(data: dict = None):
        message = ""
            
        if data is None:
            message = "Δεν παρέχονται δεδομένα."

        if data.get("id") is None or data.get("id") == "":
            message = "Λείπει το ID."
        elif data.get("name") is None or data.get("name") == "":
            message = "Λείπει το Όνομα."
        elif data.get("instructions") is None or data.get("instructions") == "":
            message = "Λείπουν οι Οδηγίες."
        elif (data.get("restapi_id") is None or data.get("restapi_id") == "") and (data.get("website_id") is None or data.get("website_id") == ""):
            message = "Πρέπει να παρέχεται είτε REST API είτε Website."
        elif data.get("restapi_id") is not None and data.get("restapi_id") != "" and data.get("website_id") is not None and data.get("website_id") != "":
            message = "Δεν μπορεί να παρέχονται ταυτόχρονα REST API και Website."

        if message:
            return {
                "message": message
            }

        return None