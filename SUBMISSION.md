# TP04 submission checklist

## Completed and included
- GitHub source/report/evidence repository: https://github.com/ggdh17934/TP04-Maaloul
- Application source, Dockerfile, Compose configurations and pinned Python requirements.
- README with published-image and source-build instructions.
- Report answering all Docker/Compose questions.
- Original assignment PDF.
- Small verified execution logs/JSON in evidence/.
- Docker Hub image: https://hub.docker.com/r/amj11/tp04-higgs
- Image tag: amj11/tp04-higgs:v1
- Registry digest: sha256:eb9ae9e9a2b0e7dbc2003f1b252a11329a4fd9e1a4ec0ae47acc3b112358d4b4
- Full dataset result: 11,000,000 rows, 29 columns, 280.34 seconds, exit code 0.
- Three published-image containers passed port and Docker DNS/HTTP checks.

## Excluded from Git
The 8 GB CSV, archives/installers, wheel caches, .venv and private .env remain local.
Fresh source builds download their Python wheels using scripts/download-dependencies.ps1.
The published Docker image can be pulled directly without rebuilding.

## Screenshot evidence completed
- [Eight captured screenshots](screenshots/README.md) are included.
- The gallery distinguishes live browser pages from labelled command-output views.
- Original logs/JSON and screenshot file hashes are included in evidence/.
- The local ZIP is regenerated from the final committed source tree.

TP02 and TP03 use the same HIGGS dataset; TP03 adds Power BI analysis.
The shared CSV is reused in TP04. No further implementation or screenshot tasks remain.
