import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from enums import PaperMCAPIProject, VersionSupportStatus

from utils import GitHubAPIUtils, PaperMCAPIUtils, VersionUtils


def main():
    all_papermc_api_folia_versions = PaperMCAPIUtils.get_all_versions(
        PaperMCAPIProject.FOLIA
    )
    all_local_versions = VersionUtils.get_all_local_versions()
    all_local_disabled_versions = VersionUtils.get_all_local_disabled_versions()
    open_gh_issues = GitHubAPIUtils.get_open_issues().unwrap_or([])
    open_gh_issue_titles = [issue["title"] for issue in open_gh_issues]
    version_support_status: Dict[str, VersionSupportStatus] = {}

    if all_papermc_api_folia_versions.is_err():
        print(
            f"Failed to fetch Folia versions: {all_papermc_api_folia_versions.unwrap_err()}"
        )
        raise SystemExit(1)

    all_papermc_api_folia_versions = all_papermc_api_folia_versions.unwrap()

    for papermc_api_folia_version in all_papermc_api_folia_versions:
        if papermc_api_folia_version in all_local_disabled_versions:
            current_status = VersionSupportStatus.DISABLED
        elif papermc_api_folia_version in all_local_versions:
            current_status = VersionSupportStatus.SUPPORTED
        else:
            current_status = VersionSupportStatus.UNSUPPORTED

        version_support_status[papermc_api_folia_version] = current_status

        if current_status == VersionSupportStatus.UNSUPPORTED:
            issue_title = f"New Folia version `{papermc_api_folia_version}`"
            if issue_title not in open_gh_issue_titles:
                result = GitHubAPIUtils.create_issue(
                    title=issue_title,
                    body=f"Version `{papermc_api_folia_version}` is not supported by this repository yet. Please add support for this version.",
                    assignees=["Endkind"],
                    labels=["update"],
                )

                if result.is_ok():
                    print(f"Issue created for version {papermc_api_folia_version}")
                else:
                    print(
                        f"Failed to create issue for version {papermc_api_folia_version}: {result.unwrap_err()}"
                    )
    create_report(version_support_status)


def create_report(
    version_support_status: Dict[str, VersionSupportStatus],
    base_path: Path = Path("./report"),
):
    if base_path.suffix == ".json":
        output_file = base_path
    else:
        base_path.mkdir(parents=True, exist_ok=True)
        output_file = base_path / "version_support_status.json"

    serialized_versions = {
        version: support_status.value
        for version, support_status in version_support_status.items()
    }
    raw_counts = Counter(serialized_versions.values())
    counts = {
        support_status.value: raw_counts.get(support_status.value, 0)
        for support_status in VersionSupportStatus
    }
    report_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "counts": counts,
        "versions": serialized_versions,
    }

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(report_payload, file, indent=4)
        file.write("\n")


if __name__ == "__main__":
    main()
