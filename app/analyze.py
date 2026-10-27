"""Stream the headerless TP2 HIGGS CSV; optionally expose status over HTTP."""
import argparse
import json
import math
import os
from pathlib import Path
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np
import pandas as pd

COLUMNS = ["label", "lepton_pt", "lepton_eta", "lepton_phi",
    "missing_energy_magnitude", "missing_energy_phi",
    "jet_1_pt", "jet_1_eta", "jet_1_phi", "jet_1_b_tag",
    "jet_2_pt", "jet_2_eta", "jet_2_phi", "jet_2_b_tag",
    "jet_3_pt", "jet_3_eta", "jet_3_phi", "jet_3_b_tag",
    "jet_4_pt", "jet_4_eta", "jet_4_phi", "jet_4_b_tag",
    "m_jj", "m_jjj", "m_lv", "m_jlv", "m_bb", "m_wbb", "m_wwbb"]
METRICS = ["label", "lepton_pt", "m_jj", "m_wwbb"]

def analyze(path, chunksize=50000):
    if chunksize < 1:
        raise ValueError("chunksize must be positive")
    start = time.perf_counter()
    rows = 0
    counts = {key: 0 for key in METRICS}
    totals = {key: [] for key in METRICS}
    # Validate each record's column count rather than silently truncate extra fields.
    with Path(path).open("rb", buffering=8 * 1024 * 1024) as stream:
        for number, line in enumerate(stream, 1):
            if line.count(b",") != 28:
                raise ValueError(f"Expected 29 fields at line {number}")
    for frame in pd.read_csv(path, header=None, names=COLUMNS, dtype="float64",
                             chunksize=chunksize, on_bad_lines="error"):
        if np.isinf(frame.to_numpy()).any():
            raise ValueError("Infinite values are not supported")
        rows += len(frame)
        for key in METRICS:
            counts[key] += int(frame[key].count())
            totals[key].append(float(frame[key].sum()))
    if not rows:
        raise ValueError("Dataset contains no records")
    metrics = {}
    for key in METRICS:
        total = math.fsum(totals[key])
        count = counts[key]
        metrics[key] = {"sum": total, "valid_count": count,
                        "missing_count": rows - count,
                        "mean": total / count if count else None}
    return {"dataset": Path(path).name, "rows": rows, "columns": len(COLUMNS),
            "chunksize": chunksize, "seconds": time.perf_counter() - start,
            "metrics": metrics}

def make_server(state, port):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path not in ("/health", "/result"):
                self.send_error(404)
                return
            payload = state.copy()
            body = json.dumps(payload, allow_nan=False).encode()
            self.send_response(200 if self.path == "/health" or payload["status"] == "complete" else 202)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *_):
            pass
    return ThreadingHTTPServer(("0.0.0.0", port), Handler)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=os.getenv("DATA_FILE", "/app/data/raw/HIGGS.csv"))
    parser.add_argument("--output", default=os.getenv("OUTPUT_FILE"))
    parser.add_argument("--chunksize", type=int, default=50000)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    state = {"status": "processing"}
    server = make_server(state, args.port) if args.serve else None
    if server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        result = analyze(args.input, args.chunksize)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
        state.update(status="complete", result=result)
        print(json.dumps(result, indent=2, allow_nan=False), flush=True)
        if server:
            while True:
                time.sleep(1)
    finally:
        if server:
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    main()
