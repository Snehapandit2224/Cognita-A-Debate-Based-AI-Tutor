import json
import sys
from collections import defaultdict

# ----------------------------
# FILE PATHS (AS UPLOADED)
# ----------------------------
GROUNDED_PATH = "all_concepts.json"
MISCONCEPTIONS_PATH = "all_concepts_misconceptions.json"

# ----------------------------
# ALLOWED CONTENT TYPES
# ----------------------------
ALLOWED_CONTENT_TYPES = {
    "intuitive",
    "formal",
    "example",
    "misconception",
    "correction"
}

errors = []

# ----------------------------
# LOAD DATA
# ----------------------------
with open(GROUNDED_PATH, "r", encoding="utf-8") as f:
    grounded = json.load(f)

with open(MISCONCEPTIONS_PATH, "r", encoding="utf-8") as f:
    pedagogy = json.load(f)

all_entries = grounded + pedagogy

# ----------------------------
# 1. DUPLICATE ID CHECK
# ----------------------------
seen_ids = set()
for entry in all_entries:
    eid = entry.get("id")
    if not eid:
        errors.append("[MISSING ID]")
    elif eid in seen_ids:
        errors.append(f"[DUPLICATE ID] {eid}")
    seen_ids.add(eid)

# ----------------------------
# 2. EMPTY TEXT CHECK
# ----------------------------
for entry in all_entries:
    text = entry.get("text", "").strip()
    if not text:
        errors.append(f"[EMPTY TEXT] ID={entry.get('id')}")

# ----------------------------
# 3. CONTENT TYPE VALIDATION
# ----------------------------
for entry in all_entries:
    ctype = entry.get("content_type")
    if ctype not in ALLOWED_CONTENT_TYPES:
        errors.append(
            f"[INVALID CONTENT TYPE] ID={entry.get('id')} → {ctype}"
        )

# ----------------------------
# 4. MISCONCEPTION ↔ CORRECTION PAIRING
# ----------------------------
pairs = defaultdict(lambda: {"mis": [], "corr": []})

for entry in pedagogy:
    key = (
        entry.get("concept"),
        entry.get("subconcept")
    )
    if entry["content_type"] == "misconception":
        pairs[key]["mis"].append(entry["id"])
    elif entry["content_type"] == "correction":
        pairs[key]["corr"].append(entry["id"])

for key, group in pairs.items():
    if len(group["mis"]) != len(group["corr"]):
        errors.append(
            f"[PAIR MISMATCH] {key} → "
            f"{len(group['mis'])} misconception(s), "
            f"{len(group['corr'])} correction(s)"
        )

# ----------------------------
# 5. CROSS-CONCEPT SAFETY
# ----------------------------
for entry in pedagogy:
    if entry["content_type"] in {"misconception", "correction"}:
        if not entry.get("concept") or not entry.get("subconcept"):
            errors.append(
                f"[MISSING CONCEPT INFO] ID={entry.get('id')}"
            )

# ----------------------------
# FINAL REPORT
# ----------------------------
if errors:
    print("\n❌ FULL DATASET VALIDATION FAILED\n")
    for err in errors:
        print(" -", err)
    sys.exit(1)

print("\n✅ FULL DATASET VALIDATION PASSED")
print("Dataset is internally consistent and production-grade.")
