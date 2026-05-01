import os
import sys

from utils import GitHubAPIUtils


def main() -> None:
    workflow_name = os.getenv("WORKFLOW_NAME", "unknown-workflow")
    workflow_event = os.getenv("WORKFLOW_EVENT", "unknown-event")
    workflow_ref = os.getenv("WORKFLOW_REF", "unknown-ref")
    workflow_sha = os.getenv("WORKFLOW_SHA", "unknown-sha")
    failed_job = os.getenv("FAILED_JOB", "unknown-job")
    workflow_run_url = os.getenv("WORKFLOW_RUN_URL", "not-provided")

    title = f"Workflow failed: {workflow_name}"
    body = "\n".join(
        [
            "A release workflow run has failed.",
            "",
            f"- Workflow: {workflow_name}",
            f"- Job: {failed_job}",
            f"- Event: {workflow_event}",
            f"- Ref: {workflow_ref}",
            f"- SHA: {workflow_sha}",
            f"- Run: {workflow_run_url}",
        ]
    )

    result = GitHubAPIUtils.create_issue(
        title=title,
        body=body,
        assignees=["Endkind"],
        labels=["workflow-failed"],
    )

    if result.is_ok():
        print(f"Created failure report issue for workflow: {workflow_name}")
        return

    print(f"Failed to create failure report issue: {result.unwrap_err()}")
    sys.exit(1)


if __name__ == "__main__":
    main()
