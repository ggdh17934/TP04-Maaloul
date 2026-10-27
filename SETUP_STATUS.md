# TP04 setup status - 2026-10-27

## Installed and downloaded
- Docker Desktop 4.97.0.244584, installed per-user with WSL 2.
- Docker engine/client 29.9.2 and Docker Compose v5.6.1.
- hello-world image downloaded and ran successfully.
- python:3.12-slim downloaded; digest: python@sha256:12316debbfb86890f6b2d825820612741ba527ad5a44e3902759141d572bfe8f.
- Application image built: tp04-higgs:local; image ID sha256:eb9ae9e9a2b0e7dbc2003f1b252a11329a4fd9e1a4ec0ae47acc3b112358d4b4.
- All six Python dependencies downloaded for both Linux and Windows (12 wheels),
  integrity checked and hashed; requirements.txt pins resolved versions.
- Original Docker installer signature valid (Docker Inc); hash in downloads/manifest.json.
- Existing 8 GB CSV reused without duplication.

## Verified
- Both Compose configurations passed docker compose config.
- 3 local correctness tests passed after the read-buffer adjustment.
- Local sample matched TP02; local /health and /result passed.
- Three Compose containers ran and became healthy on localhost ports 8001/8002/8003.
- Each port returned a completed 100,003-row, 29-column sample result.
- Container analysis1 reached analysis2 using Docker DNS and HTTP.
- Stop/start and down completed for the three-service demonstration.
- Full 8,035,497,980-byte CSV processed through Compose with 1 GB memory / 2 CPU limits.
- Full result: 11,000,000 rows, 29 columns,
  280.34 seconds including schema validation.
- Container exit code 0, OOMKilled false.
- Counts exactly match TP02 full chunks reference; sums and means match with
  relative tolerance 1e-10 and absolute tolerance 1e-8.
- Full summary and evidence persisted in results/; lab containers cleaned up afterward.

## Docker Hub publication completed
- Repository: https://hub.docker.com/r/amj11/tp04-higgs
- Published image: amj11/tp04-higgs:v1
- Registry digest: sha256:eb9ae9e9a2b0e7dbc2003f1b252a11329a4fd9e1a4ec0ae47acc3b112358d4b4
- Push completed successfully; subsequent pull returned the matching digest.
- Three containers launched from the published/pulled image and are healthy.
- Ports 8001/8002/8003 returned completed 100,003-row, 29-column sample results.
- analysis1 reached analysis2 by Docker DNS and retrieved its completed result.
- .env and .env.example now select the published image.
- Three demonstration containers are left running for review/screenshots.

## GitHub submission
- Repository: https://github.com/ggdh17934/TP04-Maaloul
- Source, Docker/Compose configuration, report, original assignment, tests and
  curated execution evidence are included.
- Downloads, .venv, private .env, wheel caches and the dataset are excluded.
- Public execution evidence is under evidence/; raw results/ remains local.

## Submission evidence completed
- Eight browser screenshots captured through the working Edge extension.
- Gallery and capture provenance: screenshots/README.md.
- Hashes and dimensions: evidence/capture-manifest.json.
- Hub and live container result pages captured directly.
- Other images capture labelled browser views of actual command output and saved results.
- The two absolute Windows user-path references identified in the audit were redacted.
- Report and README link the completed screenshot gallery.
- GitHub and submission ZIP are refreshed with this evidence.

## Evidence
- results/publication.json, hub-push.log, hub-pull.log and hub-image.json.
- results/hub-three-containers.json, hub-port-checks.json and hub-network-check.json.
- results/hub-network-inspect.json.
- results/summary.json: full-dataset aggregation.
- results/docker-validation.json: comparison against TP02.
- results/docker-version.txt and compose-version.txt.
- results/image-inspection.json and container-state.json.
- results/three-containers.json, port-checks.json and network-check.json.
- results/memory-snapshot.json: one observation, not a measured peak.
- results/compose-run.log and compose-ps.txt.
- downloads/manifest.json and vendor/manifest.json.

The first full scan was intentionally stopped to increase read buffering across
the Windows-to-WSL mount; the successful measured run uses an 8 MiB validation buffer.

## Dataset continuity confirmed
TP02 and TP03 use the same HIGGS data; TP03 adds Power BI analysis.
The TP04 Docker application uses that shared CSV, so no dataset change is pending.
