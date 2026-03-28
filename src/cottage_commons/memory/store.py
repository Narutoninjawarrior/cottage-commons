from __future__ import annotations

import abc
import json
import os
import hashlib
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256_json(data: dict) -> str:
    encoded = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()

@dataclass
class MemoryRecord:
    timestamp: str
    payload_sha256: str
    payload: dict

class MemoryStore(abc.ABC):
    @abc.abstractmethod
    def append(self, payload: dict) -> MemoryRecord:
        pass

class JsonlMemoryStore(MemoryStore):
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

    def append(self, payload: dict) -> MemoryRecord:
        record = MemoryRecord(
            timestamp=utc_now_iso(),
            payload_sha256=sha256_json(payload),
            payload=payload
        )
        
        # Append-only deterministic JSONL storage
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(record), sort_keys=True) + '\n')
            
        return record
