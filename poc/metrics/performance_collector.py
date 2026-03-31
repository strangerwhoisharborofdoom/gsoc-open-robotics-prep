import csv
import json
import platform
import time
from pathlib import Path

import psutil

BASE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = BASE_DIR / "examples" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH = RESULTS_DIR / "system_metrics.csv"
META_PATH = RESULTS_DIR / "run_metadata.json"


def collect_metrics(interval=1.0, samples=10):
    with CSV_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "cpu_percent", "memory_percent"])

        for _ in range(samples):
            writer.writerow([
                time.time(),
                psutil.cpu_percent(interval=None),
                psutil.virtual_memory().percent,
            ])
            time.sleep(interval)


def write_metadata():
    metadata = {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_count": psutil.cpu_count(logical=True),
        "memory_total_bytes": psutil.virtual_memory().total,
        "collector": "performance_collector.py",
        "purpose": "prototype runtime metrics collection for ROS 2 benchmark analysis",
    }
    META_PATH.write_text(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    collect_metrics()
    write_metadata()
