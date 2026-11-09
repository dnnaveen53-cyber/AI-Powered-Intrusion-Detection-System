from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def load_sample_attack() -> dict:
    import pandas as pd

    field_names = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "Field Names.csv", header=None).iloc[:, 0].tolist()
    train_df = pd.read_csv(PROJECT_ROOT / "data" / "raw" / "KDDTrain+.txt", header=None)
    row = train_df.iloc[0].tolist()[:41]
    record = {field_names[i]: int(row[i]) if isinstance(row[i], (int, float)) and float(row[i]).is_integer() else float(row[i]) if isinstance(row[i], float) else str(row[i]) for i in range(41)}
    return record


if __name__ == "__main__":
    payload = {"source_ip": "10.0.0.25", "record": load_sample_attack()}
    response = requests.post("http://127.0.0.1:8010/predict", json=payload, timeout=60)
    print(json.dumps(response.json(), indent=2))
