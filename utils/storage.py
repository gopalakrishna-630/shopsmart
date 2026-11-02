import json
import os
import shutil
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
BACKUP_DIR = Path(__file__).parent.parent / "backups"

def load_data(filename: str) -> dict | list:
    """Load JSON data from a file."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return {} if filename == "budget.json" else []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if data else ({} if filename == "budget.json" else [])
    except (json.JSONDecodeError, IOError):
        return {} if filename == "budget.json" else []

def save_data(filename: str, data: dict | list) -> bool:
    """Save JSON data to a file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / filename
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except IOError:
        return False

def create_backup() -> str | None:
    """Create a backup of all JSON data files."""
    try:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_folder = BACKUP_DIR / f"backup_{timestamp}"
        backup_folder.mkdir(parents=True, exist_ok=True)
        
        for file in ["products.json", "purchases.json", "budget.json"]:
            src = DATA_DIR / file
            if src.exists():
                shutil.copy2(src, backup_folder / file)
        return str(backup_folder.name)
    except Exception:
        return None

def list_backups() -> list[str]:
    """List available backups."""
    if not BACKUP_DIR.exists():
        return []
    return sorted([d.name for d in BACKUP_DIR.iterdir() if d.is_dir()])

def restore_backup(backup_name: str) -> bool:
    """Restore a backup by name."""
    backup_folder = BACKUP_DIR / backup_name
    if not backup_folder.exists():
        return False
        
    # Safety backup before restore
    create_backup()
    
    try:
        for file in ["products.json", "purchases.json", "budget.json"]:
            src = backup_folder / file
            if src.exists():
                shutil.copy2(src, DATA_DIR / file)
        return True
    except Exception:
        return False
