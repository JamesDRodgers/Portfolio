"""
Storage utilities for the CBT Journal app.

This module provides functions to:
- Save journal entries in JSONL format (append-only log).
- Load journal entries from the JSONL file.
- Export all entries into a CSV file.
- Create timestamped export snapshots.
- Overwrite the JSONL file with a new list of entries.

All paths and field definitions are taken from `app.config`.
"""

import json, csv
from pathlib import Path
from typing import List
from app.config import JSONL_PATH, CSV_PATH, EXPORT_DIR, ts, CSV_FIELDS
from app.data_models.journal import JournalEntry

def save_entry_jsonl(entry: JournalEntry, path: Path = JSONL_PATH) -> None:
    """
    Append a journal entry to the JSONL file.

    Args:
        entry (JournalEntry): The entry to save.
        path (Path, optional): File path for JSONL storage.
                               Defaults to `JSONL_PATH`.
    """
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")

def load_entries_jsonl(path: Path = JSONL_PATH) -> List[JournalEntry]:
    """
    Load all journal entries from the JSONL file.

    Args:
        path (Path, optional): File path for JSONL storage.
                               Defaults to `JSONL_PATH`.

    Returns:
        List[JournalEntry]: A list of JournalEntry objects.
                            Returns an empty list if the file does not exist.
    """
    entries: List[JournalEntry] = []
    if not path.exists():
        return entries
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            entries.append(JournalEntry.from_dict(data))
    return entries

def export_entries_csv(entries: List[JournalEntry], path: Path = CSV_PATH) -> None:
    """
    Export a list of journal entries to a CSV file.

    Args:
        entries (List[JournalEntry]): The entries to export.
        path (Path, optional): Destination CSV path.
                               Defaults to `CSV_PATH`.
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry.to_dict())

def export_snapshot(entries: List[JournalEntry]):
    """
    Create a timestamped CSV snapshot of all entries.

    Args:
        entries (List[JournalEntry]): The entries to export.

    Returns:
        Path: Path to the newly created CSV snapshot file.
              Named as `journal_export_<timestamp>.csv`.
    """
    snapshot_path = EXPORT_DIR / f"journal_export_{ts()}.csv"
    export_entries_csv(entries, snapshot_path)
    return snapshot_path

def overwrite_jsonl(entries: List[JournalEntry], path: Path = JSONL_PATH) -> None:
    """
    Overwrite the JSONL file with a fresh list of entries.

    Args:
        entries (List[JournalEntry]): The entries to write.
        path (Path, optional): File path for JSONL storage.
                               Defaults to `JSONL_PATH`.
    """
    with open(path, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry.to_dict(), ensure_ascii=False) + "\n")
