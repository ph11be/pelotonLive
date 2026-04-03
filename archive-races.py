#!/usr/bin/env python3
"""Archive races.json for the current day and reset it for a new day."""

import json
import shutil
from pathlib import Path

BASE = Path(__file__).parent
RACES_FILE = BASE / "races.json"
ARCHIVE_DIR = BASE / "races-archive"
INDEX_FILE = BASE / "archive-index.json"

BLANK_RACES = {
    "generated_at": "",
    "date": "",
    "calendar_source": "",
    "races": []
}


def main():
    # Read current races.json to get the date
    with open(RACES_FILE) as f:
        races = json.load(f)

    date = races.get("date")
    if not date:
        print("Error: races.json has no 'date' field.")
        return

    # Archive the file
    archive_path = ARCHIVE_DIR / f"races-{date}.json"
    if archive_path.exists():
        print(f"Warning: {archive_path.name} already exists — overwriting.")
    shutil.copy2(RACES_FILE, archive_path)
    print(f"Archived -> races-archive/races-{date}.json")

    # Update archive-index.json
    with open(INDEX_FILE) as f:
        index = json.load(f)

    if date not in index:
        index.append(date)
        index.sort()
        with open(INDEX_FILE, "w") as f:
            json.dump(index, f, separators=(", ", ": "))
            f.write("\n")
        print(f"Updated archive-index.json with {date}")
    else:
        print(f"Note: {date} already in archive-index.json")

    # Reset races.json
    with open(RACES_FILE, "w") as f:
        json.dump(BLANK_RACES, f, indent=2)
        f.write("\n")
    print("Reset races.json to blank template")


if __name__ == "__main__":
    main()
