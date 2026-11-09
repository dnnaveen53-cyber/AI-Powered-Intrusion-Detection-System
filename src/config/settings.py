from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
LOG_DIR = PROJECT_ROOT / "logs"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
API_DIR = PROJECT_ROOT / "api"

NSL_KDD_BASE_URL = "https://raw.githubusercontent.com/Jehuty4949/NSL_KDD/27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9/"
DATASET_FILES = {
    "train": "KDDTrain+.txt",
    "test": "KDDTest+.txt",
    "field_names": "Field Names.csv",
    "attack_types": "Attack Types.csv",
}

CATEGORY_MAPPING = {
    "normal": "Normal",
    "back": "DoS",
    "land": "DoS",
    "neptune": "DoS",
    "pod": "DoS",
    "smurf": "DoS",
    "teardrop": "DoS",
    "mailbomb": "DoS",
    "processtable": "DoS",
    "udpstorm": "DoS",
    "apache2": "DoS",
    "worm": "DoS",
    "ipsweep": "Probe",
    "nmap": "Probe",
    "portsweep": "Probe",
    "satan": "Probe",
    "mscan": "Probe",
    "saint": "Probe",
    "guess_passwd": "R2L",
    "ftp_write": "R2L",
    "imap": "R2L",
    "phf": "R2L",
    "multihop": "R2L",
    "warezmaster": "R2L",
    "warezclient": "R2L",
    "spy": "R2L",
    "xlock": "R2L",
    "xsnoop": "R2L",
    "snmpguess": "R2L",
    "snmpgetattack": "R2L",
    "httptunnel": "R2L",
    "sendmail": "R2L",
    "named": "R2L",
    "buffer_overflow": "U2R",
    "loadmodule": "U2R",
    "perl": "U2R",
    "rootkit": "U2R",
    "ps": "U2R",
    "sqlattack": "U2R",
    "xterm": "U2R",
    "httptunnel": "R2L",
}
CATEGORY_ORDER = ["Normal", "DoS", "Probe", "R2L", "U2R"]

DATASET_SELECTION_NOTE = (
    "Dataset selection decision: the internship requirement explicitly targets the intrusion categories "
    "DoS, Probe, R2L, and U2R, which are the canonical NSL-KDD attack families. We therefore use the "
    "single NSL-KDD dataset instead of combining it with CICIDS2017."
)
