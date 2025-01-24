---
title: ❌ CI/CD Pipeline Failed
assignees: endkind
labels: worflow-failed
---

The CI/CD pipeline failed for the commit: `{{ content.payload.sha }}`.

**Details:**
- **Workflow:** {{ content.payload.workflow }}
- **Job:** {{ content.payload.job }}
- **Run ID:** {{ content.payload.runId }}
- **Repository:** {{ repository.full_name }}

[View logs here]({{ content.payload.server_url }}/{{ repository.full_name }}/actions/runs/{{ content.payload.runId }}).

Please investigate the issue and resolve it.
