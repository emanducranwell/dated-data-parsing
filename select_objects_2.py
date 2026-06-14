import json
import random
from collections import defaultdict
from pathlib import Path

FULL_OBJECTS_FILE = "json/all-objects.json"
FULL_CHUNKS_FILE = "chunked_json/all-objects-chunked.json"

SELECTED_OBJECTS_FILE = "selected/random_20_selected_objects_by_room.json"
SELECTED_CHUNKS_FILE = "selected/random_20_selected_objects_by_room_chunked.json"

OBJECTS_PER_ROOM = 20

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

with open(FULL_OBJECTS_FILE, "r", encoding="utf-8") as f:
    objects = json.load(f)

with open(FULL_CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

grouped = defaultdict(list)

for obj in objects:
    room_number = str(obj.get("room_number", "")).lower().strip()

    if room_number in VALID_ROOMS:
        grouped[room_number].append(obj)

selected_objects = []

for room_number, records in sorted(grouped.items()):
    count = min(OBJECTS_PER_ROOM, len(records))
    chosen = random.sample(records, count)

    selected_objects.extend(chosen)

    print(f"Room {room_number}: {count} selected from {len(records)} objects")

selected_museum_numbers = {
    obj.get("museum_number") or obj.get("Museum number")
    for obj in selected_objects
}

selected_museum_numbers = {
    number for number in selected_museum_numbers if number
}

selected_chunks = [
    chunk for chunk in chunks
    if chunk.get("museum_number") in selected_museum_numbers
    or chunk.get("metadata", {}).get("museum_number") in selected_museum_numbers
]

with open(SELECTED_OBJECTS_FILE, "w", encoding="utf-8") as f:
    json.dump(selected_objects, f, ensure_ascii=False, indent=2)

with open(SELECTED_CHUNKS_FILE, "w", encoding="utf-8") as f:
    json.dump(selected_chunks, f, ensure_ascii=False, indent=2)

print()
print(f"Saved {len(selected_objects)} selected objects")
print(f"Output: {SELECTED_OBJECTS_FILE}")
print()
print(f"Saved {len(selected_chunks)} selected chunks")
print(f"Output: {SELECTED_CHUNKS_FILE}")