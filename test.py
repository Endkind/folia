import math
import shutil
import sys
import time
from pathlib import Path
from typing import Final, List
from uuid import UUID, uuid4

from docker.models.containers import Container
from result import Err, Ok, Result, is_err, is_ok

from utils import DockerHelper, MinecraftHelper, discover_versions

TEST_PATH: Final[Path] = Path("/tmp/endkind/test/folia")
ATTEMPT_RETRY_DELAY: Final[float] = 2.0
ATTEMPTS: Final[int] = math.ceil(120 / ATTEMPT_RETRY_DELAY)
CONTAINER_NAME = "endkind-folia-test"


def main():
    if len(sys.argv) > 1:
        versions = sys.argv[1:]
        result = test_all(versions)
    else:
        result = test_all()

    if is_ok(result):
        print(f"Test process succeeded: {result.unwrap()}")
    else:
        print(f"Test process failed: {result.unwrap_err()}")
        exit(1)


def _setup_test_environment(path: Path = TEST_PATH) -> None:
    DockerHelper.remove(CONTAINER_NAME, force=True)

    if path.exists():
        shutil.rmtree(path, ignore_errors=True)

    path.mkdir(parents=True, exist_ok=True)
    (path / "eula.txt").write_text("eula=true", encoding="utf-8")


def _cleanup_test_environment(container: Container, path: Path = TEST_PATH) -> None:
    DockerHelper.remove(container, force=True)

    shutil.rmtree(path, ignore_errors=True)


def test(tag: str) -> Result[str, str]:
    uuid: UUID = uuid4()
    path = TEST_PATH / str(uuid)
    while path.exists():
        uuid = uuid4()
        path = TEST_PATH / str(uuid)

    _setup_test_environment(path)
    image_name = f"endkind/folia:{tag}"

    container = DockerHelper.create(
        image_name,
        container_name=CONTAINER_NAME,
        ports=[(25565, 25565)],
        volumes=[(path, "/data")],
        auto_remove=True,
    )

    if is_ok(container):
        container = container.unwrap()
    else:
        return Err(container.unwrap_err())

    container.start()

    time.sleep(5)

    if not DockerHelper.is_running(
        container,
        attempts=ATTEMPTS,
        attempt_delay=ATTEMPT_RETRY_DELAY,
    ).unwrap_or(False):
        _cleanup_test_environment(container, path)
        return Err(f"Container failed to start for image '{image_name}'")

    result = MinecraftHelper.is_minecraft_server_reachable(
        "127.0.0.1",
        25565,
        ATTEMPTS,
        ATTEMPT_RETRY_DELAY,
    )

    _cleanup_test_environment(container, path)

    if is_err(result):
        return Err("Minecraft Server is not reachable")

    return Ok(f"Docker image '{image_name}' tested successfully")


def test_all(versions: List[str] | None = None) -> Result[str, str]:
    if versions is None:
        versions = discover_versions()

    if not versions:
        return Err("No versions found")

    print(f"Found {len(versions)} versions:")
    for version in versions:
        print(f" - folia/{version}")

    print("\nStarting tests...\n")

    success_count = 0

    for version in versions:
        print(f"--- Testing folia:{version} ---")
        result = test(version)

        if is_ok(result):
            print(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            print(f"❌ {result.unwrap_err()}")
        print()

    if success_count < len(versions):
        return Err(f"Test incomplete: only {success_count}/{len(versions)} succeeded")
    return Ok(f"Test complete: {success_count}/{len(versions)} succeeded")


if __name__ == "__main__":
    main()
