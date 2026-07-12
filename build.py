import os
import subprocess
import sys
from typing import List

from result import Err, Ok, Result, is_err, is_ok

from config.project import ProjectConfig
from utils import discover_versions


def main():
    if len(sys.argv) > 1:
        versions = sys.argv[1:]
        result = build_all(versions)
    else:
        result = build_all()

    if is_ok(result):
        print(f"Build process succeeded: {result.unwrap()}")
    elif is_err(result):
        print(f"Build process failed: {result.unwrap_err()}")
        exit(1)


def build(tag: str) -> Result[str, str]:
    """
    Build a Docker image with the specified tag.

    Args:
        tag: The tag of the image

    Returns:
        Result[str, str]: Ok with success message or Err with error message
    """
    try:
        image_name = f"endkind/{ProjectConfig.PROJECT}:{tag}"

        context_path = f"./versions/{tag}"

        if not os.path.exists(context_path):
            return Err(f"Build context path '{context_path}' does not exist")

        cmd = ["docker", "build", "-t", image_name, context_path]

        print(f"Building Docker image: {image_name}")
        print(f"Build context: {context_path}")
        print(f"Command: {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        return Ok(f"Docker image '{image_name}' built successfully")

    except subprocess.CalledProcessError as e:
        error_msg = f"Docker build failed: {e.stderr if e.stderr else e.stdout}"
        return Err(error_msg)
    except Exception as e:
        return Err(f"Unexpected error: {str(e)}")


def build_all(versions: List[str] = discover_versions()) -> Result[str, str]:
    """
    Build all available Docker images by auto-discovering available configurations.
    """

    if not versions:
        return Err("No build configurations found!")

    print(f"Found {len(versions)} build configurations:")
    for version in versions:
        print(f" - {ProjectConfig.PROJECT}:{version}")

    print("\nStarting builds...\n")

    success_count = 0

    for version in versions:
        print(f"--- Building {ProjectConfig.PROJECT}:{version} ---")
        result = build(version)

        if is_ok(result):
            print(f"✅ {result.unwrap()}")
            success_count += 1
        else:
            print(f"❌ {result.unwrap_err()}")
        print()

    if success_count < len(versions):
        return Err(f"Build incomplete: only {success_count}/{len(versions)} succeeded")
    return Ok(f"Build complete: {success_count}/{len(versions)} succeeded")


if __name__ == "__main__":
    main()
