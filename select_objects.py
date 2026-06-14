import json
import random
from collections import defaultdict
from pathlib import Path

INPUT_FILE = "json/all-objects.json"
OUTPUT_FILE = "selected/selected_objects_by_room.json"

OBJECTS_PER_ROOM = 10

Path("selected").mkdir(exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    objects = json.load(f)

grouped = defaultdict(list)

for obj in objects:
    room_number = obj.get("room_number")

    if room_number:
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