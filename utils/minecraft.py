import time

from mcstatus import JavaServer
from result import Err, Ok, Result


class MinecraftHelper:
    @staticmethod
    def is_minecraft_server_reachable(
        host: str,
        port: int = 25565,
        attempts: int = 5,
        attempt_delay: float = 5.0,
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
