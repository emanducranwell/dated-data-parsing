import fs from "fs";
import { parse } from "csv-parse/sync";

const INPUT_FILE = "cleaned/all-objects-cleaned.csv";
const OUTPUT_FILE = "json/all-objects.json";

const raw = fs.readFileSync(INPUT_FILE, "utf8");

const records = parse(raw, {
  columns: true,
  skip_empty_lines: true,
  trim: true,
});

const objects = records.map((row) => ({
  ...row,

  museum_number: row["Museum number"] || null,

  object_name:
    row["Title"] ||
    row["Object type"] ||
    "Unknown Object",
}));

fs.writeFileSync(
  OUTPUT_FILE,
  JSON.stringify(objects, null, 2)
);

console.log(`Saved ${objects.length} objects.`);
console.log(`Output: ${OUTPUT_FILE}`);