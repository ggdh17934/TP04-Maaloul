# TP04 report - verified Docker execution and Docker Hub publication

## What is Docker and why use it in data science?
Docker packages an application and its runtime dependencies into an image.
Containers run that image in isolated processes. This makes Python versions and
libraries reproducible between machines. Read-only mounts keep the large HIGGS
input outside the image, while the results directory persists outside the container.

## Image versus container
An image is the reusable filesystem and execution configuration. A container is a
created instance of an image, with its own process, writable layer and network
identity. Three containers can use the same image and have different host ports.

## Dockerfile instructions
- FROM chooses the base image (Python 3.12 on slim Debian).
- WORKDIR sets the directory for subsequent commands.
- COPY brings selected source files and downloaded packages into the image.
- RUN executes build-time commands, here installing packages from local wheels.
- CMD sets the default command used when the container starts.

## What problem does Compose solve?
Compose stores services, images/build instructions, mounts, ports, networks and
resource limits in one YAML file. A single command creates the environment
consistently, and another command removes its containers and project network.

## docker run versus docker compose up
docker run starts an individual container from command-line options.
docker compose up reads a declarative project and starts its services, creating
the required network and applying the declared mounts and settings. The single
batch service exits successfully after writing its result; that is expected.

## Extending with a database
Add a PostgreSQL service, a named volume for /var/lib/postgresql/data, credentials
through secrets or an ignored environment file, and a pg_isready health check.
The application connects using the service name (for example db:5432), waits for
readiness, and inserts the small aggregation results through a PostgreSQL driver.
A read-only CSV mount is sufficient for this assignment; no SQL server is needed now.

## Dataset and application
Uses the existing TP02 HIGGS CSV: 29 numeric columns without a header.
The prior manifest records 11,000,000 rows, 8,035,497,980 bytes and SHA-256
9a7cf07203c2e348a261920a80179e42024b8c43cc6e39d4c42a7b0aa8114815.
These are inherited metadata, not a fresh hash verification. Streaming aggregation
uses 50,000-row chunks and computes sums, valid/missing counts and global means
for label, lepton_pt, m_jj and m_wwbb. The sample run is explicitly distinct from
the full input. A validation pass checks each row's 29 fields before parsing.

## Verified Docker execution (2026-10-27)
Docker Desktop 4.97.0.244584, engine/client 29.9.2 and Compose v5.6.1
ran using the existing WSL 2 backend. hello-world ran successfully.
The image tp04-higgs:local was built from the downloaded Linux Python wheels.

Three Compose containers became healthy, served completed 100,003-row sample
results through ports 8001, 8002 and 8003, and communicated using Docker DNS.
Stop/start and cleanup were demonstrated for the local image. A subsequent
three-container run used the published image pulled from Docker Hub, as documented below.

The full HIGGS run processed 11,000,000 rows and 29 columns
in 280.34 seconds, including the schema-validation pass.
It used a 1 GB configured container memory limit and a 2 CPU limit, exited 0
and was not OOM-killed. Counts, sums and means matched the TP02 full chunks
reference (rtol 1e-10, atol 1e-8). This is a single run, not a repeated benchmark.
The validation pass uses an 8 MiB buffer to reduce mount I/O overhead.
Results and command evidence for submission are stored in ../evidence/.
The memory snapshot is one observation and does not establish peak memory.

## Docker Hub push, pull and three-container verification
On 2026-10-27, amj11/tp04-higgs:v1 was pushed successfully to:
https://hub.docker.com/r/amj11/tp04-higgs

The push returned registry digest:
sha256:eb9ae9e9a2b0e7dbc2003f1b252a11329a4fd9e1a4ec0ae47acc3b112358d4b4

A subsequent docker pull returned the same digest. Three containers were created
from that published image and became healthy. Their host ports 8001, 8002 and 8003
each returned a completed 100,003-row, 29-column sample result. Container analysis1
requested http://analysis2:8000/result through the shared Docker network and
received the completed analysis result.

The three demonstration containers remain running for screenshot capture.
Evidence is saved in ../evidence/publication.json and the ../evidence/hub-* files.

## GitHub submission
Source, configuration, this report and curated execution evidence:
https://github.com/ggdh17934/TP04-Maaloul

The original assignment PDF is included. The large input CSV, installer, package
caches and local Python environment are excluded. README.md explains how to reuse
the dataset and pull the published Docker image or rebuild the source.

## Screenshot evidence
[Eight screenshots](../screenshots/README.md) cover installation versions, the
published Hub image, saved push/pull output, three containers and mapped ports,
network membership and DNS/HTTP, the live sample endpoint, the saved full-data
result, and the saved Compose batch exit/cleanup.

All images were captured by the Edge browser extension. Native Windows capture
timed out. Images 02 and 06 directly capture live browser pages; other images
capture labelled evidence viewers showing actual current command snapshots or
saved output. These are browser screenshots, not terminal screenshots.
The recorded 8 GB run was not rerun or represented as a new run for capture.
Raw logs/JSON and the image SHA-256 manifest are included in ../evidence/.
