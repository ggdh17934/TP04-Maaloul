# Complete TP04 work plan

## Goal and interpretation
Complete the five tasks in the supplied TP04 PDF using your existing TP02 HIGGS
CSV. Deliver source, Docker configuration, real execution evidence, a brief
report and README on your GitHub account, with the application image on Docker Hub.
Installation, downloads, local Docker build, three-container checks and the full
CSV Compose run have now completed. See SETUP_STATUS.md for the actual measurements.
Docker Hub publication and the three-container run from the pulled Hub image are
now complete under amj11/tp04-higgs:v1. GitHub source/report/evidence are now available at https://github.com/ggdh17934/TP04-Maaloul.
Eight screenshots are now captured through the Edge extension; the report and
README link the gallery. Earlier native capture failures were resolved for browser capture. The phases below retain the reproducible workflow.

TP02 and TP03 use the same HIGGS dataset; TP03 adds Power BI analysis.
Reusing the existing CSV therefore supplies the dataset referenced by both labs.

## Existing resources and constraints
- Windows 10 Pro 22H2, build 19045.6466, x86_64.
- Intel i5-8350U, 8 logical processors, approximately 8 GB physical RAM.
- WSL 2.4.11.0 is installed, default distribution version 2; no user distribution.
- HypervisorPresent is true. The separate firmware flag reports false; do not infer
  that WSL is broken from that flag while the hypervisor is active. Engine startup
  is the practical validation still to perform.
- Docker Desktop and docker CLI were not found during initial inspection.
- About 14.96 GB decimal free on C: before downloads. Recheck before installation.
  Budget several GB for Desktop, its virtual disk, base image and build cache.
  If space becomes insufficient, use another drive for Docker data or free space
  manually; do not duplicate the 8 GB input.
- CSV exists at ../TP2-MALOUL/data/raw/HIGGS.csv, 8,035,497,980 bytes.
- A 100,003-row sample and prior dataset manifest already exist.
- Python 3.12 and Git already exist. Docker supplies Compose and container Python.
- No GPU, Hadoop, Spark, SQL database, Dask cluster or separate Ubuntu installation
  is required by this assignment.

Windows compatibility must be checked against the current Docker support policy:
the installation page lists Windows 10 Pro 22H2 but also limits support to Windows
versions within Microsoft's servicing timeline. If Desktop rejects this Windows
build or engine startup fails, resolve the compatibility issue or use a supported
Windows/Linux machine; do not report Docker validation as complete.

## Phase 1 - Prepare and download
1. Read both PDF pages and inspect TP02 code/schema/data metadata.
2. Download Docker Desktop x64 from Docker's official endpoint.
3. Verify the Windows Authenticode signature and save SHA-256, size and version.
4. Download Python 3.12 Linux wheels for the container, plus Windows wheels for
   local checks. Keep all large artifacts ignored by Git.
5. Prepare a small streaming app, offline-wheel Dockerfile, Compose files,
   environment template, tests, report explanations and evidence checklist.
6. Validate locally against a synthetic fixture and the existing sample.
7. Record exact completed/pending items in SETUP_STATUS.md.

Acceptance: verified installer, complete package downloads, local checks passing,
and a written plan with reproducible commands. No dataset download is needed.

## Phase 2 - Task 1: install and verify Docker
1. Recheck free disk space. Run the downloaded installer and select WSL 2/Linux
   containers. Handle Windows UAC and restart only if the installer requests it.
2. Start Docker Desktop and complete its first-run agreement prompts.
3. Open a fresh PowerShell and run the check script.
4. Require both client and server output from docker version, a working
   docker compose version, and a successful hello-world run.
5. Create/sign in to your Docker Hub account yourself. Keep credentials private.
6. Save screenshot 01 with real version output.

No separate Ubuntu download is necessary for Docker Desktop's own WSL backend.
If WSL needs updating, use wsl --update as directed by the actual engine error.
Do not change BIOS settings based only on the ambiguous firmware flag.

Acceptance: running Linux engine, working Compose, successful hello-world.

## Phase 3 - Task 2: build, push, pull
1. Build tp04-higgs:local from the Dockerfile. This downloads python:3.12-slim.
2. Validate a sample run with a read-only data mount.
3. Choose your real Docker Hub namespace and tag username/tp04-higgs:v1.
4. Run docker login interactively, then tag, push and pull as documented in README.
5. Record the image digest, repository URL and successful command outputs.
6. Use that pulled image for Task 3.

The 8 GB dataset stays outside the image. This keeps pushes small and lets the
same image analyze a different mounted CSV. A fresh image alone is not enough;
the user must also supply the dataset mount.
For stronger reproducibility after the first successful build, record/pin the
resolved base-image digest and freeze all resolved package versions.

Acceptance: build succeeds; Hub push and subsequent pull succeed; digest saved.

## Phase 4 - Task 3: three containers, ports and network
1. Use the literal docker network create and three docker run commands in README.
2. Reuse the existing sample for this demonstration to avoid three concurrent
   full-dataset scans on an 8 GB laptop.
3. Map container port 8000 to localhost ports 8001, 8002 and 8003.
4. Verify docker ps, network membership, each HTTP endpoint and a request from
   node1 to node2 using container DNS.
5. Demonstrate stop and start on these three containers.
6. Capture real screenshots and logs, then clean up only the named lab resources.
7. Optionally repeat using compose.three.yaml to demonstrate declarative setup.

Acceptance: three running containers, three working port mappings, and proven
container-to-container connectivity. Sharing a network alone is not proof of
communication. Each container computes independently; no distributed-processing
performance claim is made.

## Phase 5 - Task 4: full-dataset Compose execution
1. Confirm .env points at the TP02 data directory and full raw/HIGGS.csv.
2. Run docker compose config to validate path interpolation and the service.
3. Run docker compose up --build --exit-code-from data-analysis.
4. The application validates the headerless schema, streams 50,000 rows at a time,
   and writes results/summary.json to the host directory.
5. Require exit code 0, 29 columns and exactly 11,000,000 rows. Check sums/counts/
   means against TP02 full results where the metric definitions match.
6. Save actual duration and docker stats observations if useful; do not predict
   performance or copy sample timings into full-run results.
7. Run docker compose ps -a and capture the expected successful batch exit.
8. Run docker compose down and save evidence.

The input mount is read-only. A second bind mount preserves outputs after down.
The Compose memory cap is 1 GB and CPU limit 2; actual engine execution will
confirm suitability. Avoid running the three-service demonstration concurrently.

Acceptance: full-data JSON, exact row count, successful exit, persisted output,
and screenshots of up, ps -a and down.

## Phase 6 - Task 5: finalize the report
The prepared report answers all six conceptual questions:
- Docker and its usefulness for data science.
- Images versus containers.
- FROM, WORKDIR, COPY, RUN and CMD.
- The purpose of Compose.
- docker run versus docker compose up.
- How to add a database service.

Add measured results, exact versions/digests, image/repository links and evidence.
Explain the shared TP02/TP03 dataset, headerless schema, chunked algorithm, mounts, port maps,
memory limits and why the three sample containers are independent.
Do not leave execution claims without corresponding evidence.

Acceptance: brief, accurate report linked to real screenshots and outputs.

## Phase 7 - GitHub submission
1. Review .gitignore and dockerignore; exclude data, installer, wheels, environment
   and credentials. Keep source, original assignment, docs, tests and screenshots.
2. Commit real small result JSON deliberately if wanted (results/*.json is ignored
   by default; use git add -f for the specific reviewed summaries).
3. Create/select the intended GitHub repository and push using your account.
4. Test README instructions from a clean checkout: download dependencies, configure
   DATA_DIR, supply the existing dataset, then build and run.
5. Ensure the teacher can access the GitHub repository and Docker Hub image.

Acceptance: accessible GitHub source/report/evidence and accessible Hub image.

## Expected downloads and what is already available
| Resource | Action |
| --- | --- |
| HIGGS CSV and sample | Reuse TP02 files; no second copy |
| Docker Desktop Windows x64 | Download to downloads/ and verify |
| WSL | Already 2.4.11.0; update only if required by engine |
| Ubuntu | Not required |
| Python 3.12 host | Already installed |
| pandas, NumPy and dependencies | Download Linux/Windows wheels to vendor/ |
| Python base image | docker build --pull after the engine starts |
| hello-world image | docker run --rm hello-world after installation |
| Docker Compose | Included with Docker Desktop |
| Git | Already installed |
| Docker Hub/GitHub accounts | User authentication and publication step |

## Sources
- Assignment: TP04_Containerization_and_Big_Data_Environment_Deployment_Using.pdf
- Docker Windows installation: https://docs.docker.com/desktop/setup/install/windows-install/
- WSL backend: https://docs.docker.com/desktop/features/wsl/
- Dataset metadata: ../TP2-MALOUL/data/manifest.json
- Dataset publisher: https://archive.ics.uci.edu/dataset/280/higgs
