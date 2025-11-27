import json
from pathlib import Path

MEM_FILE = Path(__file__).parent / "memory.json"


def load_memory():
    if MEM_FILE.exists():
        try:
            return json.loads(MEM_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_memory(history):
    try:
        MEM_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass