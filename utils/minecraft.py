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
    ) -> Result[str, None]:
        for attempt in range(attempts):
            try:
                server = JavaServer.lookup(f"{host}:{port}")
                status = server.status()

                version = status.version.name

                return Ok(version)
            except Exception:
                if attempt < attempts - 1:
                    time.sleep(attempt_delay)

        return Err(None)
