from __future__ import annotations

import argparse
import hashlib
import os
from dataclasses import dataclass
from typing import List

from cottage_commons.memory import JsonlMemoryStore

def get_file_excerpt(filepath: str, lines_count: int = 15) -> str:
    """Returns a deterministic bounded excerpt to preserve the shape of the document securely."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if len(lines) <= lines_count * 2:
            return "".join(lines)
            
        first_chunk = "".join(lines[:lines_count])
        last_chunk = "".join(lines[-lines_count:])
        return f"{first_chunk}\n... [TRUNCATED {len(lines) - (lines_count*2)} LINES] ...\n{last_chunk}"
    except Exception as e:
        return f"[ERROR READING FILE: {str(e)}]"

def file_sha256(filepath: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def scan_artifacts(roots: List[str]) -> dict:
    artifacts = {}
    for root in roots:
        if not os.path.exists(root):
            continue
            
        for dirpath, _, filenames in os.walk(root):
            # Sort for absolute determinism required by audit
            for filename in sorted(filenames):
                # Target explicit text file types
                if not filename.endswith(('.md', '.json', '.py', '.txt', '.yml')):
                    continue
                    
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, start=os.getcwd())
                
                artifacts[rel_path] = {
                    "size_bytes": os.path.getsize(filepath),
                    "content_sha256": file_sha256(filepath),
                    "excerpt": get_file_excerpt(filepath)
                }
    return artifacts

def main():
    parser = argparse.ArgumentParser(description="The Scribe Agent: Deterministic Artifact Summarization.")
    parser.add_argument("--roots", nargs="+", default=["data", "docs"], help="Directories to scan")
    parser.add_argument("--store", default="data/scribe_memory.jsonl", help="Path to the JSONL memory store")
    args = parser.parse_args()

    print("Scribe Agent initiated. Scanning roots:", args.roots)
    artifacts = scan_artifacts(args.roots)
    
    payload = {
        "agent": "Scribe",
        "action": "directory_summary",
        "artifacts_scanned": len(artifacts),
        "artifacts": artifacts
    }
    
    store = JsonlMemoryStore(args.store)
    record = store.append(payload)
    
    print(f"Scribe summary complete. Payload appended to {args.store}")
    print(f"Record SHA-256: {record.payload_sha256}")

if __name__ == "__main__":
    main()
