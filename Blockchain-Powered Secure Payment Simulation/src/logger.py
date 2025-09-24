import json
from pathlib import Path
from datetime import datetime
from web3 import Web3
import numpy as np

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)

TRANSACTIONS_LOG = DATA_DIR / "transactions.json"
ATTACKS_LOG = DATA_DIR / "attacks.json"
OUTPUTS_DIR = DATA_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)

SCAN_LOG = OUTPUTS_DIR / "scan_log.json"


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super(NpEncoder, self).default(obj)


def append_json(path, item):
    arr = []
    if path.exists():
        try:
            arr = json.loads(path.read_text())
        except Exception:
            arr = []
    arr.append(item)
    path.write_text(json.dumps(arr, indent=2, cls=NpEncoder))


def log_transaction(employee_id, timestamp, amount, encrypted_payload, tx_hash=None, channel="real"):

    if hasattr(tx_hash, "hex"):
        tx_hash_str = tx_hash.hex()
    else:
        tx_hash_str = str(tx_hash) if tx_hash is not None else None

    entry = {
        "employee_id": str(employee_id),
        "timestamp": datetime.utcfromtimestamp(float(timestamp)).isoformat() + "Z",
        "amount": float(amount),
        "encrypted_payload": str(encrypted_payload),
        "tx_hash": tx_hash_str,
        "channel": str(channel)
    }
    append_json(TRANSACTIONS_LOG, entry)


def log_scan_event(step, confidence, scan_time, attacks_detected, attacks_cumulative=None):

    entry = {
        "step": int(step),
        "confidence": float(confidence),
        "scan_time": float(scan_time),
        "attacks_detected": int(attacks_detected),
        "attacks_cumulative": int(attacks_cumulative) if attacks_cumulative is not None else None,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    append_json(SCAN_LOG, entry)


def clear_logs():
    if TRANSACTIONS_LOG.exists():
        TRANSACTIONS_LOG.unlink()
    if ATTACKS_LOG.exists():
        ATTACKS_LOG.unlink()
    if SCAN_LOG.exists():
        SCAN_LOG.unlink()
