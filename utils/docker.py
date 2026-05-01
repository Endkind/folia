import time
from pathlib import Path
from typing import List, Optional, Tuple, Union

import docker
from docker.errors import APIError, DockerException, ImageNotFound, NotFound
from docker.models.containers import Container
from result import Err, Ok, Result, is_err, is_ok


class DockerHelper:
    @staticmethod
    def create(
        image_name: str,
        *,
        container_name: Optional[str] = None,
        ports: List[Tuple[int, int]] = None,
        volumes: Optional[List[Tuple[Union[str, Path], str]]] = None,
        auto_remove: bool = False,
    ) -> Result[Container, str]:
        client = docker.from_env()

        try:
            docker_ports = None
            docker_volumes = None

            if ports:
                docker_ports = {
                    f"{container_port}/tcp": host_port
                    for host_port, container_port in ports
                }

            if volumes:
                docker_volumes = {
                    host_path: {"bind": container_path, "mode": "rw"}
                    for host_path, container_path in volumes
                }

            container = client.containers.create(
                image=image_name,
                name=container_name,
                ports=docker_ports,
                volumes=docker_volumes,
                detach=True,
                auto_remove=auto_remove,
            )

            return Ok(container)
        except ImageNotFound:
            return Err(f"Image not found: {image_name}")
        except APIError as e:
            return Err(f"Failed to create Container: {e}")
        except DockerException as e:
            return Err(f"Docker error: {e}")

    @staticmethod
    def start(container: Container) -> Result[Container, str]:
        try:
            container.start()
            container.reload()

            return Ok(container)

        except APIError as e:
            return Err(f"Failed to start Container: {e}")

        except DockerException as e:
            return Err(f"Docker error: {e}")

    @staticmethod
    def stop(container: Container) -> Result[Container, str]:
        try:
            container.reload()

            if container.status == "running":
                container.stop()

            container.reload()

            return Ok(container)

        except APIError as e:
            return Err(f"Failed to stop Container: {e}")

        except DockerException as e:
            return Err(f"Docker error: {e}")

    @staticmethod
    def is_running(
        container: Container, *, attempts: int = 5, attempt_delay: float = 5.0
    ) -> Result[bool, str]:
        try:
            for attempt in range(attempts):
                container.reload()

                if container.status == "running":
                    return Ok(True)

                time.sleep(attempt_delay)

        except APIError as e:
            return Err(f"Failed to check status: {e}")

        except DockerException as e:
            return Err(f"Docker error: {e}")

    @staticmethod
    def remove(
        container: Union[Container, str], force: bool = False
    ) -> Result[None, str]:
        try:
            if isinstance(container, str):
                client = docker.from_env()
                container = client.containers.get(container)

            container.remove(force=force)

            return Ok(None)

        except APIError as e:
            return Err(f"Failed to remove Container: {e}")

        except DockerException as e:
            return Err(f"Docker error: {e}")
