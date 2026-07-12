import math
from pathlib import Path
from typing import Final

from .project import ProjectConfig


class TestConfig:
    TEST_PATH: Final[Path] = Path(f"/tmp/endkind/test/{ProjectConfig.PROJECT}")
    CONTAINER_NAME: Final[str] = f"endkind-{ProjectConfig.PROJECT}-test"
    ATTEMPT_RETRY_DELAY: Final[float] = 2.0
    ATTEMPTS: Final[int] = math.ceil(120 / ATTEMPT_RETRY_DELAY)
