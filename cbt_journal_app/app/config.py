"""
Configuration module for the CBT Journal app.

This module defines global paths for data storage (JSONL, CSV, exports),
the Feeling Wheel reference file, and utility functions for ensuring
directory existence and timestamp generation. It also lists the standard
CSV field order used for exporting journal entries.
"""

from pathlib import Path
from datetime import datetime

# === Base Directories ===
BASE_DIR = Path("/content")  # Root project directory (default for Colab/Notebook)
DATA_DIR = BASE_DIR / "data"  # Directory for storing user journal entries
EXPORT_DIR = BASE_DIR / "exports"  # Directory for storing exported snapshots

# === File Paths ===
FEELING_WHEEL_PATH = DATA_DIR / "Feeling_wheel.json"  # JSON file containing emotion hierarchy
JSONL_PATH = DATA_DIR / "journal.jsonl"  # Log file where each entry is stored in JSON Lines format
CSV_PATH   = DATA_DIR / "journal.csv"    # Flat CSV export of all journal entries

def ensure_dirs():
    """
    Ensure that required directories exist.

    Creates the `data/` and `exports/` directories if they do not
    already exist. This is called at app startup to guarantee
    paths are available for saving user files.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def ts() -> str:
    """
    Generate a timestamp string for filenames.

    Returns:
        str: Current datetime formatted as YYYYMMDD_HHMMSS.
             Example: '20250825_154210'
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

# === CSV Schema ===
CSV_FIELDS = [
    "date", "event", "thought",
    "emotion_primary", "emotion_secondary", "emotion_tertiary", "emotion_intensity",
    "cbt_distortion", "reframing", "ai_reflection"
]
"""list[str]: Standard column order for exporting journal entries to CSV."""
