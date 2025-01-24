---
title: ❌ CI/CD Pipeline Failed
assignees: endkind
labels: workflow-failed
---

The CI/CD pipeline failed for the commit: `${{ github.sha }}`.

**Details:**
- **Workflow:** ${{ github.workflow }}
- **Job:** ${{ github.job }}
- **Run ID:** ${{ github.run_id }}
- **Repository:** ${{ github.repository }}

[View logs here](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}).

Please investigate the issue and resolve it.
