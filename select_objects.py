import json
import random
from collections import defaultdict
from pathlib import Path

INPUT_FILE = "json/all-objects.json"
OUTPUT_FILE = "selected/random_30_selected_objects_by_room.json"

OBJECTS_PER_ROOM = 30

VALID_ROOMS = {
    "1", "2", "2a", "3", "4",
    "6", "7", "8", "9", "10",
    "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "30",
    "33", "33a", "33b", "35", "38", "39",
    "40", "41", "42", "43", "43a",
    "46", "47", "48", "49", "50", "51", "52", "53", "54",
    "55", "56", "57", "58", "59",
    "61", "62", "63", "64", "65", "66", "67", "68",
    "69", "70", "71", "72", "73",
    "90", "90a", "92", "93", "94", "95"
}

Path("selected").mkdir(exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    objects = json.load(f)

grouped = defaultdict(list)

for obj in objects:
    room_number = str(obj.get("room_number", "")).lower().strip()

    if room_number in VALID_ROOMS:
        grouped[room_number].append(obj)

selected = []

for room_number, records in sorted(grouped.items()):
    count = min(OBJECTS_PER_ROOM, len(records))
    chosen = random.sample(records, count)

    selected.extend(chosen)

    print(
        f"Room {room_number}: "
        f"{count} selected from {len(records)} objects"
    )

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)

print()
print(f"Saved {len(selected)} objects")
print(f"Output: {OUTPUT_FILE}")