# TP04 - HIGGS data analysis with Docker

[GitHub repository](https://github.com/ggdh17934/TP04-Maaloul) | [Docker Hub image](https://hub.docker.com/r/amj11/tp04-higgs)

This folder contains the TP04 assignment and a verified implementation using the
existing TP02 HIGGS dataset. Start with [the full plan](PROJECT_PLAN.md).
Installation, Docker execution, Docker Hub publication and final screenshots are
separate milestones; see [setup status](SETUP_STATUS.md) for completion and measured results.

## Published Docker image
[Docker Hub repository](https://hub.docker.com/r/amj11/tp04-higgs):
amj11/tp04-higgs:v1

Registry digest: sha256:eb9ae9e9a2b0e7dbc2003f1b252a11329a4fd9e1a4ec0ae47acc3b112358d4b4

Push and pull succeeded. Three containers from this image passed port, health
and Docker DNS/HTTP checks and remain running for review:
http://localhost:8001/result, http://localhost:8002/result, http://localhost:8003/result.
The full 11,000,000-row Compose run also passed before publication.
See [the evidence directory](evidence/README.md), [the report](report/REPORT.md) and SETUP_STATUS.md.

## Start from a fresh checkout
1. Reuse the TP02 dataset directory containing raw/HIGGS.csv and
   samples/first_100003.csv. The complete CSV must be supplied separately.
2. Copy .env.example to .env and adjust DATA_DIR to the actual data directory.
3. With Docker Desktop running, launch the published image:
   docker compose -f compose.three.yaml up -d --wait --pull always
4. Open http://localhost:8001/result, http://localhost:8002/result or
   http://localhost:8003/result. Each uses the explicitly identified sample.
5. For the full CSV batch without rebuilding:
   docker compose up --no-build --exit-code-from data-analysis
   Then inspect results/summary.json and run docker compose down.

To rebuild from source, run scripts/download-dependencies.ps1 with Python 3.12
before docker build. This downloads the Linux wheels required by the Dockerfile.
For local tests, create .venv with python -m venv .venv and install requirements.txt
using .venv/Scripts/python.exe -m pip install -r requirements.txt.

## Screenshot evidence

[View all eight screenshots](screenshots/README.md). These include the live Docker Hub
page and live result endpoint, plus labelled browser views of real command output.

## Files
- app/analyze.py: stream the CSV in 50,000-row chunks; optional HTTP status.
- Dockerfile: Python 3.12 slim image, packages installed from downloaded Linux wheels.
- compose.yaml: full-dataset batch job with read-only input and persistent JSON output.
- compose.three.yaml: three HTTP containers and a shared network, sample input.
- requirements.txt: pinned complete dependency set.
- vendor/: downloaded Python wheels, excluded from Git and mostly excluded from build context.
- scripts/: prerequisite check and repeatable package downloads.
- tests/: aggregation correctness and malformed-record checks.
- report/REPORT.md: answers to the assignment questions and evidence placeholders.
- screenshots/: [eight captured screenshots and source/provenance notes](screenshots/README.md).
- downloads/: installer and its verification manifest, excluded from Git.

## Dataset
The existing data is a CSV file, not a SQL database:
`../TP2-MALOUL/data/raw/HIGGS.csv`.
Size measured during setup: 8,035,497,980 bytes. The TP02 manifest records
11,000,000 rows and 29 columns, no header.
We reuse it through a read-only bind mount; it is not copied into Git or the image.

TP02 and TP03 use the same HIGGS dataset. TP03 adds Power BI analysis of that
same data. TP04 therefore reuses the shared CSV for the Docker application;
no different TP03 dataset or additional Power BI work is required for this lab.

## Local verification
Open PowerShell and run:
```powershell
Set-Location -LiteralPath 'C:\path\to\TP4-maalool'
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe app/analyze.py --input '../TP2-MALOUL/data/samples/first_100003.csv' --output results/sample-summary.json
```
The 100,003-row sample is only a quick check. Full-data results require the
8 GB input and should be recorded separately.

## First Docker run
Install the verified installer from downloads/, start Docker Desktop with the
WSL 2 backend and Linux containers, then reopen PowerShell. No separate Ubuntu
installation is needed. Review the full plan for compatibility and storage notes.

```powershell
Set-Location -LiteralPath 'C:\path\to\TP4-maalool'
docker version
docker compose version
docker run --rm hello-world
docker build --pull -t tp04-higgs:local .
docker compose config
docker compose up --build --exit-code-from data-analysis
docker compose ps -a
Get-Content results/summary.json
docker compose down
```
Require an exit code of 0 and 11,000,000 rows for the full run.
A batch container exits when its work finishes; `Exited (0)` is expected.

## Docker Hub: push then pull
Create/sign in to your own account at https://hub.docker.com/.
Replace the username with your actual Docker Hub username.
```powershell
$hubUser = 'amj11'
$image = "$hubUser/tp04-higgs:v1"
docker login
docker tag tp04-higgs:local $image
docker push $image
docker pull $image
```
Save the real repository URL and digest. Never save tokens in source files.
Set IMAGE_NAME in .env to the pushed/pulled tag for the three-service Compose file.
The data remains mounted from the host; the shared image contains the analysis code.

## Three containers: literal Task 3 commands
Run these after the push/pull above, in the same PowerShell session.
If any name already exists, inspect it first; do not delete unrelated containers.

```powershell
$dataDir = (Resolve-Path '../TP2-MALOUL/data').Path
docker network create tp04-net
docker run -d --name tp04-node1 --network tp04-net --memory 512m --cpus 1 -p 127.0.0.1:8001:8000 --mount "type=bind,source=$dataDir,target=/app/data,readonly" -e DATA_FILE=/app/data/samples/first_100003.csv $image python app/analyze.py --serve
docker run -d --name tp04-node2 --network tp04-net --memory 512m --cpus 1 -p 127.0.0.1:8002:8000 --mount "type=bind,source=$dataDir,target=/app/data,readonly" -e DATA_FILE=/app/data/samples/first_100003.csv $image python app/analyze.py --serve
docker run -d --name tp04-node3 --network tp04-net --memory 512m --cpus 1 -p 127.0.0.1:8003:8000 --mount "type=bind,source=$dataDir,target=/app/data,readonly" -e DATA_FILE=/app/data/samples/first_100003.csv $image python app/analyze.py --serve
docker ps --filter network=tp04-net
docker network inspect tp04-net
docker exec tp04-node1 python -c "import urllib.request; print(urllib.request.urlopen('http://tp04-node2:8000/health').read().decode())"
Invoke-RestMethod http://localhost:8001/result
Invoke-RestMethod http://localhost:8002/result
Invoke-RestMethod http://localhost:8003/result
docker stop tp04-node1 tp04-node2 tp04-node3
docker start tp04-node1 tp04-node2 tp04-node3
docker ps --filter network=tp04-net
```
`/health` shows that the process is alive; `/result` returns status
`processing` until analysis completes, then status `complete` with its result.
The three containers independently analyze the sample; this is a networking and
lifecycle demonstration, not a distributed speedup claim.

After saving evidence, remove only these lab containers and network:
```powershell
docker stop tp04-node1 tp04-node2 tp04-node3
docker rm tp04-node1 tp04-node2 tp04-node3
docker network rm tp04-net
```

## Equivalent three-service Compose project
After setting IMAGE_NAME in .env to your pulled Docker Hub image:
```powershell
docker compose -f compose.three.yaml config
docker compose -f compose.three.yaml up -d --pull always
docker compose -f compose.three.yaml ps
docker compose -f compose.three.yaml exec analysis1 python -c "import urllib.request; print(urllib.request.urlopen('http://analysis2:8000/health').read().decode())"
docker compose -f compose.three.yaml down
```
Stop the literal docker-run demonstration first so the three host ports are free.

## Reproducing package downloads
```powershell
powershell -ExecutionPolicy Bypass -File scripts/download-dependencies.ps1
```
On a different OS or Python version, use Python 3.12 and adjust only the local
verification wheel target. Docker always uses Linux x86_64 wheels here.
The base image must still be downloaded by Docker; wheels alone are not an image.

## Submission
Commit source, Compose files, report, README, tests, evidence/ and real screenshots to your
GitHub repository. Do not commit installer, wheel archives, .venv, .env or HIGGS.
The evidence/ folder contains the selected small logs and results; results/ stays local.
Run the package download script before rebuilding a fresh checkout. Include
Docker Hub repository URL and image digest plus the dataset source/license:
https://archive.ics.uci.edu/dataset/280/higgs (CC BY 4.0).
