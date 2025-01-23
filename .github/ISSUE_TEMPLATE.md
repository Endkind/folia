---
title: ❌ CI/CD Pipeline Failed
assignees: octocat
labels: bug
---

The CI/CD pipeline failed for the commit: `{{ payload.sha }}`.

**Details:**
- **Workflow:** {{ payload.workflow }}
- **Job:** {{ payload.job }}
- **Run ID:** {{ payload.runId }}
- **Repository:** {{ repository.full_name }}

[View logs here]({{ payload.server_url }}/{{ repository.full_name }}/actions/runs/{{ payload.runId }}).

Please investigate the issue and resolve it.
