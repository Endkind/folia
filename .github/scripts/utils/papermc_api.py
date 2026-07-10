import requests
from config import PaperMCAPIConfig
from enums import PaperMCAPIProject
from result import Err, Ok, Result
from yarl import URL


class PaperMCAPIUtils:
    @classmethod
    def get_all_versions(cls, project: PaperMCAPIProject) -> Result[list[str], str]:
        base_url = URL(PaperMCAPIConfig.BASE_URL)

        url = base_url / project.value

        try:
            response = requests.get(url.__str__())
        except requests.RequestException as error:
            return Err(
                f"Failed to fetch versions for project {project.value}. Request error: {error}"
            )

        if response.status_code != 200:
            return Err(
                f"Failed to fetch versions for project {project.value}. Status code: {response.status_code}"
            )

        try:
            payload = response.json()
        except ValueError as error:
            return Err(
                f"Failed to fetch versions for project {project.value}. Invalid JSON response: {error}"
            )

        versions_by_release = payload.get("versions")
        if not isinstance(versions_by_release, dict):
            return Err(
                f"Failed to fetch versions for project {project.value}. Invalid response shape: missing or invalid 'versions' object"
            )

        all_versions = []

        for release, versions in versions_by_release.items():
            if not isinstance(versions, list) or not all(
                isinstance(version, str) for version in versions
            ):
                return Err(
                    f"Failed to fetch versions for project {project.value}. Invalid versions list for release '{release}'"
                )

            all_versions.extend(versions)

        return Ok(all_versions)
