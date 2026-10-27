# Verified execution evidence
These small files are copied from actual Docker commands and analysis outputs.
Environment-specific Windows user paths are redacted as <workspace-parent>;
numeric results and digests are unchanged. These files are logs/JSON, not screenshots.
- summary.json: complete 11,000,000-row HIGGS run.
- docker-validation.json: comparison against the TP02 full streaming result.
- docker-version.txt and compose-version.txt: installed tool versions.
- hub-push.log and hub-pull.log: registry push digest and subsequent pull.
- hub-port-checks.json: all three host ports returned completed sample results.
- hub-network-check.json: analysis1 retrieved analysis2's result by Docker DNS/HTTP.
- hub-three-containers.json and hub-network-inspect.json: actual services/network.
- compose-run.log, compose-ps.txt and compose-down.log: full batch run and cleanup.
- publication.json: publication and verification metadata.
The sample results do not replace the full dataset run.

## Screenshot sources
The screenshot gallery is ../screenshots/README.md; file hashes and capture source
types are in capture-manifest.json. Browser captures of HTML views are explicitly
labelled as command-output/result viewers. views/ contains those static HTML
sources, and scripts/build-evidence-views.py regenerates them from actual logs
and read-only Docker queries. Native window capture is not claimed.
