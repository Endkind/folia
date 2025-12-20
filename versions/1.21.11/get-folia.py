#!/usr/bin/env python3

import argparse
import os

import requests
from result import Err, Ok, Result, is_err


def main():
    parser = argparse.ArgumentParser(
        description="Folia Download Script - Version and Build Parameters"
    )

    parser.add_argument(
        "--version",
        type=str,
        default=os.environ.get("VERSION", "latest"),
        help='Minecraft Version (Default: environment variable VERSION or "latest")',
    )

    parser.add_argument(
        "--build",
        type=str,
        default=os.environ.get("BUILD", "latest"),
        help='Build Number (Default: environment variable BUILD or "latest")',
    )

    parser.add_argument(
        "--output",
        type=str,
        default="server.jar",
        help="Output file path (Default: server.jar)",
    )

    args = parser.parse_args()

    if args.version == "latest":
        version_result = get_latest_version()
        if is_err(version_result):
            print(f"Error: {version_result.unwrap_err()}")
            exit(1)
        version = version_result.unwrap()
    else:
        version = args.version

    if args.build == "latest":
        build_result = get_latest_build(version)
        if is_err(build_result):
            print(f"Error: {build_result.unwrap_err()}")
            exit(1)
        build = build_result.unwrap()
    else:
        build = args.build

    print(f"Version: {version}")
    print(f"Build: {build}")

    download_result = download_folia(version, build, args.output)
    if is_err(download_result):
        print(f"Error: {download_result.unwrap_err()}")
        exit(1)


def download_folia(
    version: str, build: str, output: str = "server.jar"
) -> Result[None, str]:
    base_url = "https://api.papermc.io/v2/projects/folia"
    download_url = f"{base_url}/versions/{version}/builds/{build}/downloads/folia-{version}-{build}.jar"

    try:
        output_dir = os.path.dirname(output)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        response = requests.get(download_url)
        response.raise_for_status()

        with open(output, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {os.path.basename(output)}")
        return Ok(None)
    except Exception as e:
        return Err(f"Error downloading: {e}")


def get_latest_version() -> Result[str, str]:
    base_url = "https://api.papermc.io/v2/projects/folia"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        versions = data["versions"]

        for version in reversed(versions):
            build_result = get_latest_build(version)
            if not is_err(build_result):
                return Ok(version)

        return Err("No version with available builds found")
    except Exception as e:
        return Err(f"Error getting latest version: {e}")


def get_latest_build(version: str) -> Result[str, str]:
    base_url = "https://api.papermc.io/v2/projects/folia"

    try:
        response = requests.get(f"{base_url}/versions/{version}")
        response.raise_for_status()
        data = response.json()
        return Ok(str(data["builds"][-1]))
    except Exception as e:
        return Err(f"Error getting latest build for version {version}: {e}")


if __name__ == "__main__":
    main()
