# Communicates with Ollama server.
from crud.models.LLM import LLM

import requests

class LLMsService:
    def __init__(self):
        self.DOMAIN = "http://ollama:11434"

    # Returns the list of locally downloaded models.
    def get_all(self) -> list[str]:
        models = requests.get(f"{self.DOMAIN}/api/tags").json()
        return [model['name'] if ':' not in model['name'] else model['name'].split(':')[0] for model in models["models"]]

    # Downloads a model locally.
    def download_model(self, model_name: str) -> None:
        response = requests.post(f"{self.DOMAIN}/api/pull", json={"model": model_name})
        response.raise_for_status()
        return True if response.status_code == 200 else False

    # Removes a locally downloaded model.
    def remove_model(self, model_name: str) -> None:
        response = requests.delete(f"{self.DOMAIN}/api/delete", json={"model": model_name})
        response.raise_for_status()
        return True if response.status_code == 200 else False