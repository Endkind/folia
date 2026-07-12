import time
from typing import Annotated

from mcstatus import JavaServer
from pydantic import Field, validate_call
from result import Err, Ok, Result


class MinecraftHelper:
    @staticmethod
    @validate_call
    def is_minecraft_server_reachable(
        host: str,
        port: Annotated[int, Field(ge=1, le=65535)] = 25565,
        attempts: Annotated[int, Field(ge=1)] = 5,
        attempt_delay: Annotated[float, Field(ge=1.0)] = 5.0,
    ) -> Result[str, str]:
        last_error: Exception | None = None

        for attempt in range(attempts):
            try:
                server = JavaServer.lookup(f"{host}:{port}")
                status = server.status()

                version = status.version.name

                return Ok(version)
            except Exception as exc:
                last_error = exc
                if attempt < attempts - 1:
                    time.sleep(attempt_delay)

        error_details = (
            f" Last error: {last_error.__class__.__name__}: {last_error}"
            if last_error is not None
            else ""
        )
        return Err(
            f"Unable to reach Minecraft server at '{host}:{port}' after {attempts} attempt(s) "
            f"with {attempt_delay:g}s delay between attempts. "
            f"Please verify that the server is running and the port is accessible.{error_details}"
        )
