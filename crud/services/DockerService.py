# This service communicates with docker to run on-demand AI Agents.
import docker

class DockerService:
    def __init__(self):
        self.client = docker.from_env()

    def run_container(self, image: str, name: str) -> str:
        try:
            container = self.client.containers.run(image, name=name, detach=True)
            return container.id
        except docker.errors.DockerException as e:
            return str(e)

    def pause_container(self, name: str) -> str:
        try:
            container = self.client.containers.get(name)
            container.pause()
            return "OK"
        except docker.errors.DockerException as e:
            return str(e)

    def delete_container(self, name: str) -> str:
        try:
            container = self.client.containers.get(name)
            container.remove(force=True)
            return "OK"
        except docker.errors.DockerException as e:
            return str(e)