# Azure Data Factory - Git-integrated artifacts

This folder is the Git integration root for the Azure Data Factory instance
used in AZURE-001 and later phases.

**Do not hand-craft pipeline, dataset, linked-service, or trigger JSON here.**
Once an ADF instance is configured with Git integration pointing at this
folder, ADF itself generates and synchronizes those artifacts (`pipeline/`,
`dataset/`, `linkedService/`, `factory/`, etc.) whenever changes are
published from the ADF Studio authoring UI. Committing fake/manual
versions of those artifacts would misrepresent what was actually built and
tested in ADF.

Until that integration is connected, this folder intentionally stays empty
aside from this README. See [docs/azure/02_target_architecture.md](../docs/azure/02_target_architecture.md)
for the pipeline design these artifacts will eventually implement.
