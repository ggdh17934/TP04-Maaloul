# Evidence checklist
Save real screenshots after performing each task:
1. Docker Desktop running, docker version and docker compose version.
2. Docker Hub repository and successful docker push output.
3. Successful pull with digest.
4. docker ps showing three running containers and ports 8001/8002/8003.
5. docker network inspect and container-to-container HTTP request.
6. Browser http://localhost:8001/result with completed sample analysis.
7. Full Compose output and results/summary.json showing 11,000,000 rows.
8. docker compose ps -a after batch exit; docker compose down output.
Never include passwords, access tokens or login codes in screenshots.

## Current capture status
Genuine UI screenshots are still pending because the computer-use tool denied
access to Edge. Actual command logs and analysis results are included in ../evidence/.
For browser-result screenshots, the three published-image containers are running:
- http://localhost:8001/result
- http://localhost:8002/result
- http://localhost:8003/result

Docker Hub repository: https://hub.docker.com/r/amj11/tp04-higgs
Save only the relevant application window or tab, without unrelated personal tabs.
