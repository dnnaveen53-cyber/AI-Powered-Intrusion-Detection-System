from __future__ import annotations

import urllib.request
from pathlib import Path
from urllib.parse import quote

from src.config.settings import DATASET_FILES, NSL_KDD_BASE_URL, RAW_DATA_DIR


class DatasetManifest:
    def __init__(self) -> None:
        self.files = DATASET_FILES
        self.base_url = NSL_KDD_BASE_URL
        self.raw_dir = RAW_DATA_DIR

    def ensure_downloaded(self) -> dict[str, Path]:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        paths: dict[str, Path] = {}
        for key, filename in self.files.items():
            target = self.raw_dir / filename
            if not target.exists():
                encoded_name = quote(filename)
                download_url = f"{self.base_url}{encoded_name}"
                with urllib.request.urlopen(download_url, timeout=60) as response, open(target, "wb") as output:
                    while True:
                        chunk = response.read(65536)
                        if not chunk:
                            break
                        output.write(chunk)
            paths[key] = target
        return paths


def download_dataset_if_missing() -> dict[str, Path]:
    return DatasetManifest().ensure_downloaded()
