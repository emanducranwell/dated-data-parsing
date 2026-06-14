import json
from pathlib import Path

INPUT_FILE = "json/all-objects.json"
OUTPUT_FILE = "chunked_json/all-objects-chunked.json"

CORE_FACT_FIELDS = [
    "Object type",
    "Museum number",
    "Title",
    "Culture",
    "Production date",
    "Production place",
    "Find spot",
    "Materials",
    "Ware",
    "Technique",
    "Dimensions",
    "Location",
    "room_number",
    "cultural_location",
    "Dept",
]

DESCRIPTION_FIELDS = [
    "Description",
    "Subjects",
    "Assoc name",
    "Inscription",
    "Condition",
]

CONTEXT_FIELDS = [
    "Curators Comments",
    "Producer name",
    "Authority",
    "Acq name (acq)",
    "Acq name (finding)",
    "Acq name (excavator)",
    "Acq name (previous)",
    "Acq date",
    "Acq notes (acq)",
    "Acq notes (exc)",
    "Exhibition history",
    "Bib references",
]

IMAGE_FIELDS = [
    "Image",
    "image",
    "Image URL",
    "image_url",
]


def clean_value(value):
    if value is None:
        return ""

    value = str(value)
    value = value.replace("\r", " ").replace("\n", " ")
    value = " ".join(value.split())
    value = value.strip(" ;")

    return value


def get_first_available(record, fields):
    for field in fields:
        value = clean_value(record.get(field))
        if value:
            return value
    return ""


def build_text_chunk(record, fields):
    parts = []

    for field in fields:
        value = clean_value(record.get(field))

        if value:
            parts.append(f"{field}: {value}")

    return "\n".join(parts)


def get_object_display_name(record):
    title = clean_value(record.get("Title"))
    object_type = clean_value(record.get("Object type"))
    object_name = clean_value(record.get("object_name"))

    if title:
        return title

    if object_name:
        return object_name

    if object_type:
        return object_type.replace("(object name)", "").strip()

    return "Unknown object"


def create_chunk(record, chunk_type, fields):
    museum_number = clean_value(record.get("Museum number")) or clean_value(record.get("museum_number"))
    object_name = get_object_display_name(record)
    text = build_text_chunk(record, fields)

    if not museum_number or len(text) < 30:
        return None

    return {
        "chunk_id": f"{museum_number}_{chunk_type}",
        "museum_number": museum_number,
        "object_name": object_name,
        "chunk_type": chunk_type,
        "text": text,
        "metadata": {
            "museum_number": museum_number,
            "object_name": object_name,
            "chunk_type": chunk_type,
            "object_type": clean_value(record.get("Object type")),
            "culture": clean_value(record.get("Culture")),
            "cultural_location": clean_value(record.get("cultural_location")),
            "room_number": clean_value(record.get("room_number")),
            "production_date": clean_value(record.get("Production date")),
            "production_place": clean_value(record.get("Production place")),
            "find_spot": clean_value(record.get("Find spot")),
            "materials": clean_value(record.get("Materials")),
            "location": clean_value(record.get("Location")),
            "source_csv": clean_value(record.get("source_csv")),
            "image": get_first_available(record, IMAGE_FIELDS),
        },
    }


def main():
    input_path = Path(INPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"Could not find {INPUT_FILE}")

    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    chunks = []

    for record in data:
        chunk_specs = [
            ("core_facts", CORE_FACT_FIELDS),
            ("description", DESCRIPTION_FIELDS),
            ("context", CONTEXT_FIELDS),
        ]

        for chunk_type, fields in chunk_specs:
            chunk = create_chunk(record, chunk_type, fields)

            if chunk:
                chunks.append(chunk)

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    print(f"Read {len(data)} objects.")
    print(f"Created {len(chunks)} chunks.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()