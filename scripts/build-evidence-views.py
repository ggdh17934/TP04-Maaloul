"""Build clearly labelled browser views of actual TP04 command output."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import html
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
VIEWS = EVIDENCE / "views"
DOCKER = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/DockerDesktop/resources/bin/docker.exe"
if not DOCKER.is_file():
    DOCKER = Path("docker")
ENV = os.environ.copy()
if DOCKER.is_absolute():
    ENV["PATH"] = str(DOCKER.parent) + os.pathsep + ENV.get("PATH", "")

def command(*args):
    return subprocess.check_output([str(DOCKER), *args], cwd=ROOT, env=ENV, text=True, encoding="utf-8")

def saved(name):
    return (EVIDENCE / name).read_text(encoding="utf-8-sig")

def redact(value):
    if isinstance(value, str):
        for prefix in (str(ROOT.parent), str(ROOT.parent).replace("\\", "/"), str(ROOT.parent).replace("\\", "\\\\")):
            value = value.replace(prefix, "<workspace-parent>")
        return value
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, dict):
        return {key: redact(item) for key, item in value.items()}
    return value

# Redact decoded JSON strings, including JSON-lines Docker ps output.
for name in ("docker-validation.json", "hub-three-containers.json"):
    path = EVIDENCE / name
    text = path.read_text(encoding="utf-8-sig")
    try:
        value = json.loads(text)
        path.write_text(json.dumps(redact(value), indent=2) + "\n", encoding="utf-8")
    except json.JSONDecodeError:
        objects = [redact(json.loads(line)) for line in text.splitlines() if line.strip()]
        path.write_text("".join(json.dumps(item) + "\n" for item in objects), encoding="utf-8")

stamp = datetime.now(timezone(timedelta(hours=1))).isoformat(timespec="seconds")
versions = command("version") + "\n" + command("compose", "version") + "\n" + command("info", "--format", "OS: {{.OperatingSystem}} | Memory: {{.MemTotal}} bytes | CPUs: {{.NCPU}}")
containers = command("ps", "--format", "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}")
network = json.loads(command("network", "inspect", "tp4-maalool_tp04-net"))[0]
network_summary = {key: network[key] for key in ("Name", "Driver", "Scope", "Internal", "Containers")}
peer = command("compose", "-f", "compose.three.yaml", "exec", "-T", "analysis1", "python", "-c", "import urllib.request; print(urllib.request.urlopen('http://analysis2:8000/result').read().decode())")
peer_text = json.dumps(json.loads(peer), indent=2)
for name, text in (("versions-snapshot.txt", versions), ("containers-snapshot.txt", containers), ("network-snapshot.json", json.dumps(network_summary, indent=2)), ("peer-snapshot.json", peer_text)):
    (EVIDENCE / name).write_text(text.rstrip() + "\n", encoding="utf-8")

pages = {
    "01-installation-versions.html": ("Task 1 - Docker installation and versions", "Current read-only command output; generated " + stamp, [("docker version; docker compose version; docker info", versions)]),
    "03-registry-push-pull.html": ("Task 2 - Docker Hub push and pull", "Saved output from the successful publication on 2026-10-27. This page does not rerun the upload.", [("Saved docker push amj11/tp04-higgs:v1 output", saved("hub-push.log")), ("Saved docker pull amj11/tp04-higgs:v1 output", saved("hub-pull.log"))]),
    "04-three-containers.html": ("Task 3 - Three running containers and mapped ports", "Current docker ps snapshot; generated " + stamp, [("docker ps --format (names, image, status, ports)", containers), ("Previously verified HTTP results from all three host ports", saved("hub-port-checks.json"))]),
    "05-network-connectivity.html": ("Task 3 - Shared network and container DNS/HTTP", "Current network inspection and a real analysis1-to-analysis2 HTTP request; generated " + stamp, [("docker network inspect: selected network and membership fields", json.dumps(network_summary, indent=2)), ("docker compose exec analysis1: GET http://analysis2:8000/result", peer_text)]),
    "07-full-dataset-result.html": ("Task 4 - Full HIGGS dataset result", "Saved successful full run. The 8 GB job was not rerun to create this screenshot.", [("Full result: evidence/summary.json", saved("summary.json")), ("Independent comparison and exit status: evidence/docker-validation.json", saved("docker-validation.json"))]),
    "08-compose-lifecycle.html": ("Task 4 - Compose batch exit and cleanup", "Saved actual output from the full dataset run and cleanup on 2026-10-27.", [("docker compose ps -a after successful batch exit", saved("compose-ps.txt")), ("docker compose down", saved("compose-down.log"))]),
}
VIEWS.mkdir(exist_ok=True)
css = """body{font:16px/1.5 system-ui,sans-serif;background:#eef2f6;color:#142033;margin:0}main{max-width:1320px;margin:32px auto;padding:28px;background:white;border:1px solid #d5dee8;border-radius:10px}h1{font-size:27px;margin:0 0 8px}h2{font-size:17px;margin:26px 0 8px}.note{background:#eaf2ff;padding:12px;border-left:4px solid #326bd4}pre{font:13px/1.55 Consolas,monospace;background:#f5f7fa;border:1px solid #d7dfe8;padding:16px;white-space:pre-wrap;overflow-wrap:anywhere}footer{color:#546278;border-top:1px solid #d7dfe8;padding-top:16px;font-size:13px}"""
for name, (title, note, sections) in pages.items():
    body = "".join("<section><h2>" + html.escape(label) + "</h2><pre>" + html.escape(text.rstrip()) + "</pre></section>" for label, text in sections)
    output = "<!doctype html><meta charset='utf-8'><title>" + html.escape(title) + "</title><style>" + css + "</style><main><h1>" + html.escape(title) + "</h1><p class='note'>" + html.escape(note) + "</p>" + body + "<footer>TP04 | amj11/tp04-higgs:v1 | Browser view of actual command output, not a terminal screenshot. Host-specific paths redacted.</footer></main>"
    (VIEWS / name).write_text(output, encoding="utf-8")
print("Created", len(pages), "labelled evidence views from actual outputs at", stamp)

# Compact, readable views of selected fields; originals remain in evidence/.
def table(headers, rows):
    return "<table style='border-collapse:collapse;width:100%;font-size:14px'><thead><tr>" + "".join("<th style='text-align:left;padding:8px;border-bottom:2px solid #cbd5e1'>" + html.escape(str(h)) + "</th>" for h in headers) + "</tr></thead><tbody>" + "".join("<tr>" + "".join("<td style='padding:7px;border-bottom:1px solid #e2e8f0'>" + html.escape(str(v)) + "</td>" for v in row) + "</tr>" for row in rows) + "</tbody></table>"

def compact(name, title, note, body):
    output = "<!doctype html><meta charset='utf-8'><title>" + html.escape(title) + "</title><style>" + css + "</style><main><h1>" + html.escape(title) + "</h1><p class='note'>" + html.escape(note) + "</p>" + body + "<footer>TP04 | Screenshot of a browser evidence view. Values come from actual command output; complete originals are in evidence/.</footer></main>"
    (VIEWS / name).write_text(output, encoding="utf-8")

port_results = json.loads(saved("hub-port-checks.json"))
compact("04-three-containers.html", "Task 3 - Three healthy containers and host ports", "Actual docker ps snapshot generated " + stamp + ". Port results are saved verification output.",
        "<h2>docker ps - names, image, status and ports</h2><pre>" + html.escape(containers.rstrip()) + "</pre><h2>HTTP results from the three mapped host ports</h2>" + table(["Port", "Status", "Rows", "Columns"], [[v["port"], v["status"], f'{v["rows"]:,}', v["columns"]] for v in port_results]))
peer_value = json.loads(peer)
members = network_summary["Containers"]
compact("05-network-connectivity.html", "Task 3 - Shared network and container DNS/HTTP", "Actual selected network fields and a real peer request, generated " + stamp + ". Full output: network-snapshot.json and peer-snapshot.json.",
        "<h2>docker network inspect</h2>" + table(["Network", "Driver", "Scope"], [[network_summary["Name"], network_summary["Driver"], network_summary["Scope"]]]) +
        "<h2>Network members</h2>" + table(["Container", "Docker network address"], [[v["Name"], v["IPv4Address"]] for v in members.values()]) +
        "<h2>analysis1 requests http://analysis2:8000/result through Docker DNS</h2>" + table(["Status", "Dataset", "Rows", "Columns"], [[peer_value["status"], peer_value["result"]["dataset"], f'{peer_value["result"]["rows"]:,}', peer_value["result"]["columns"]]]))
full = json.loads(saved("summary.json"))
validation = json.loads(saved("docker-validation.json"))
compact("07-full-dataset-result.html", "Task 4 - Full 11,000,000-row HIGGS run", "Selected fields from the actual saved full-run JSON; this screenshot does not rerun the 8 GB job. Complete precision and logs are included in evidence/.",
        table(["Dataset", "Rows", "Columns", "Chunk size", "Runtime (seconds)"], [[full["dataset"], f'{full["rows"]:,}', full["columns"], f'{full["chunksize"]:,}', f'{full["seconds"]:.2f}']]) +
        "<h2>Aggregations over the complete input</h2>" + table(["Metric", "Sum", "Valid values", "Mean"], [[key, v["sum"], f'{v["valid_count"]:,}', v["mean"]] for key, v in full["metrics"].items()]) +
        "<h2>Independent comparison against the TP02 full result</h2>" + table(["Container exit", "OOM killed", "Counts match", "Sums/means match"], [[validation["exit_code"], validation["oom_killed"], validation["all_counts_match"], validation["all_sums_means_match"]]]) +
        "<p>Floating-point comparison: relative tolerance 1e-10; absolute tolerance 1e-8.</p>")
print("Compact selected-field pages rendered with unchanged source values.")
