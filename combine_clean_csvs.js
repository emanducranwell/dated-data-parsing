import fs from "fs";
import path from "path";
import { parse } from "csv-parse/sync";
import { stringify } from "csv-stringify/sync";

const INPUT_DIR = "csv";
const OUTPUT_FILE = "cleaned/all-objects-cleaned.csv";

const ROOM_TO_CULTURAL_LOCATION = {
  1: "Enlightenment",
  2: "Themes",
  "2a": "Themes",
  3: "Exhibitions",
  4: "Ancient Egypt",
  6: "Ancient Greece and Rome",
  7: "Middle East",
  8: "Middle East",
  9: "Middle East",
  10: "Middle East",
  12: "Ancient Greece and Rome",
  13: "Ancient Greece and Rome",
  14: "Ancient Greece and Rome",
  15: "Ancient Greece and Rome",
  16: "Ancient Greece and Rome",
  17: "Ancient Greece and Rome",
  18: "Ancient Greece and Rome",
  19: "Ancient Greece and Rome",
  20: "Ancient Greece and Rome",
  21: "Ancient Greece and Rome",
  22: "Ancient Greece and Rome",
  23: "Ancient Greece and Rome",
  24: "Themes",
  25: "Africa",
  26: "Americas",
  27: "Americas",
  30: "Exhibitions",
  33: "Asia",
  "33a": "Asia",
  "33b": "Asia",
  35: "Exhibitions",
  38: "Themes",
  39: "Themes",
  40: "Europe",
  41: "Europe",
  42: "Middle East",
  43: "Middle East",
  "43a": "Exhibitions",
  46: "Europe",
  47: "Europe",
  48: "Europe",
  49: "Europe",
  50: "Europe",
  51: "Europe",
  52: "Middle East",
  53: "Middle East",
  54: "Middle East",
  55: "Middle East",
  56: "Middle East",
  57: "Middle East",
  58: "Middle East",
  59: "Middle East",
  61: "Ancient Egypt",
  62: "Ancient Egypt",
  63: "Ancient Egypt",
  64: "Ancient Egypt",
  65: "Ancient Egypt",
  66: "Ancient Egypt",
  67: "Asia",
  68: "Themed Rooms",
  69: "Ancient Greece and Rome",
  70: "Ancient Greece and Rome",
  71: "Ancient Greece and Rome",
  72: "Ancient Greece and Rome",
  73: "Ancient Greece and Rome",
  90: "Exhibitions",
  "90a": "Exhibitions",
  92: "Asia",
  93: "Asia",
  94: "Asia",
  95: "Asia",
};

function cleanMuseumNumber(value) {
  if (!value) return null;

  return value
    .replace("No: Optional[", "")
    .replace("]", "")
    .trim();
}

function extractRoomNumber(location) {
  if (!location) return null;

  const text = String(location);

  const match = text.match(/(?:Room|Rooms|G)?\s*(\d+[a-z]?)/i);

  if (!match) return null;

  return match[1].toLowerCase();
}

function getCulturalLocation(roomNumber) {
  if (!roomNumber) return null;

  return ROOM_TO_CULTURAL_LOCATION[roomNumber] || null;
}

function cleanValue(value) {
  if (value === undefined || value === null || value === "") return null;

  return String(value)
    .replace(/\r/g, " ")
    .replace(/\n/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

const allRows = [];

const files = fs
  .readdirSync(INPUT_DIR)
  .filter((file) => file.endsWith(".csv"));

for (const file of files) {
  const filePath = path.join(INPUT_DIR, file);
  const raw = fs.readFileSync(filePath, "utf8");

  const records = parse(raw, {
    columns: true,
    skip_empty_lines: true,
    trim: true,
    relax_column_count: true,
  });

  for (const row of records) {
    const cleanedRow = {};

    for (const key in row) {
      cleanedRow[key] = cleanValue(row[key]);
    }

    cleanedRow["Museum number"] = cleanMuseumNumber(row["Museum number"]);

    const roomNumber = extractRoomNumber(row["Location"]);
    cleanedRow["room_number"] = roomNumber;
    cleanedRow["cultural_location"] = getCulturalLocation(roomNumber);
    cleanedRow["source_csv"] = file;

    allRows.push(cleanedRow);
  }
}

const csvOutput = stringify(allRows, {
  header: true,
});

fs.writeFileSync(OUTPUT_FILE, csvOutput);

console.log(`Combined ${files.length} CSV files.`);
console.log(`Saved ${allRows.length} objects to ${OUTPUT_FILE}`);