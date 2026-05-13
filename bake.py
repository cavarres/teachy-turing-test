#!/usr/bin/env python3
"""
bake.py — Reads evaluation_set_with_proposed.csv and injects the data
into index.html, producing evaluator_baked.html (self-contained, no
other files needed at runtime).

Usage:
    python bake.py
"""
import csv
import json
import pathlib
import re
import sys

SRC_CSV  = pathlib.Path("evaluation_set_with_proposed.csv")
SRC_HTML = pathlib.Path("index.html")
OUT_HTML = pathlib.Path("evaluator_baked.html")
SENTINEL = "/* __EVAL_DATA__ */ null"


def load_questions(csv_path: pathlib.Path) -> list[dict]:
    questions = []
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse alternatives JSON if present
            alts_raw = row.get("alternatives", "").strip()
            alternatives = []
            if alts_raw:
                try:
                    # The CSV uses {"opt1","opt2",...} with inner quotes escaped as \\"
                    # Split on the "," boundary between items, then unescape inner quotes.
                    inner = alts_raw[1:-1]  # strip outer { }
                    parts = re.split('","', inner)
                    alternatives = [p.strip('"').replace('\\"', '"') for p in parts]
                except Exception:
                    alternatives = []

            questions.append({
                "presentation_index": int(row["presentation_index"]),
                "question_id":        row["question_id"],
                "description":        row["description"],
                "alternatives":       alternatives,
                "answer":             row["answer"],
                "answer_type":        row["answer_type"],
                "education_level":    row["education_level"],
                "subject_normalized": row["subject_normalized"],
                "subject_raw":        row["subject_raw"],
                "category_raw":       row["category_raw"],
                # Analyst-only — present in exported CSV but never shown in UI
                "current_difficulty":  row["current_difficulty"],
                "proposed_difficulty": row["proposed_difficulty"],
                "row_type":            row["row_type"],
            })

    # Sort by presentation_index (should already be ordered, but be explicit)
    questions.sort(key=lambda q: q["presentation_index"])
    return questions


def main():
    if not SRC_CSV.exists():
        print(f"ERROR: {SRC_CSV} not found.", file=sys.stderr)
        sys.exit(1)
    if not SRC_HTML.exists():
        print(f"ERROR: {SRC_HTML} not found.", file=sys.stderr)
        sys.exit(1)

    questions = load_questions(SRC_CSV)
    print(f"Loaded {len(questions)} questions from {SRC_CSV}")

    html = SRC_HTML.read_text(encoding="utf-8")

    if SENTINEL not in html:
        print(f"ERROR: sentinel '{SENTINEL}' not found in {SRC_HTML}.", file=sys.stderr)
        sys.exit(1)

    data_js = json.dumps(questions, ensure_ascii=False, indent=None)
    html = html.replace(SENTINEL, data_js)

    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Written: {OUT_HTML}  ({len(questions)} questions baked in)")


if __name__ == "__main__":
    main()
