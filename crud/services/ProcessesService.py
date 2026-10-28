# This service communicates with Processes-related CRUD endpoints.
import os
import psutil
import requests
import subprocess
import time

class ProcessesService:
    def __init__(self):
        self.DOMAIN = "http://api:5000"

    # Returns the list of Processes.
    def get_all(self) -> list[str]:
        processes = requests.get(f"{self.DOMAIN}/processes").json()
        return processes

    # Retrieves a Process by its ID.
    def get_by_id(self, id: str) -> dict:
        response = requests.get(f"{self.DOMAIN}/processes/{id}")
        return None if response.status_code == 404 else response.json()

    # Retrieves a Process by its AI Agent ID.
    def get_by_agent_id(self, id: str) -> list[dict]:
        response = requests.get(f"{self.DOMAIN}/processes/agent/{id}").json()
        return response
    
    # Adds a new Process.
    def add(self, data: dict) -> str:
        response = requests.post(f"{self.DOMAIN}/processes", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Edit an existing Process.
    def edit(self, id: str, data: dict) -> str:
        response = requests.put(f"{self.DOMAIN}/processes/{id}", json=data)
        return response.json() if response.status_code >= 400 else "OK"

    # Checks if a Process is running.
    def is_running(self, pid: int) -> bool:
        return psutil.pid_exists(pid)

    # Deletes an existing Process.
    def delete(self, id: str) -> str:
        response = requests.delete(f"{self.DOMAIN}/processes/{id}")
        return response

    # Runs the subprocess of a Process given its PID.
    def run_process(self, pid: int, file_id: str, content: str) -> str:
        try:
            self.__write_temp_file__(file_id, content)

            result = subprocess.Popen(["python", f"temp/{file_id}.py", str(pid)])
            time.sleep(5)

            if result.poll() is not None:
                return ""

            return "OK"
        except Exception as e:
            return str(e)

    # Deletes the subprocess of a Process.
    def delete_process(self, pid: int) -> str:
        try:
            psutil.Process(pid).terminate()
            return "OK"
        except Exception as e:
            return str(e)

    # Writes the agent.py temporary file.
    def __write_temp_file__(self, name: str, content: str) -> None:
        with open(f"temp/{name}.py", "w") as file:
            file.write(content)

    # Deletes the temporary file of a Process.
    def __delete_temp_file__(self, name: str) -> None:
        try:
            os.remove(f"temp/{name}.py")
        except FileNotFoundError:
            pass