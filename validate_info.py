import sys
import re

FILE = "info.yml"

# Read the file
try:
    lines = open(FILE, encoding="utf8").read().splitlines()
except Exception:
    print("❌ Cannot read info.yml")
    sys.exit(1)

# Storage variables
student = None
indeks = None
par_student = None
par_indeks = None

# Very small YAML parser for this specific file
current_section = None

for line in lines:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        continue

    # Detect section "par:"
    if stripped.startswith("par:"):
        current_section = "par"
        continue

    # Key-value lines: key: value
    if ":" in stripped:
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if current_section == "par":
            if key == "student":
                par_student = value
            elif key == "indeks":
                par_indeks = value
        else:
            if key == "student":
                student = value
            elif key == "indeks":
                indeks = value

# -------------------------------
# Validation logic
# -------------------------------

# 1. Main student must not be empty
if not student:
    print("❌ 'student' field must not be empty.")
    sys.exit(1)

# 2. Main indeks must match format
if not indeks or not re.match(r"^(RN|SI|RI) [0-9]{3}/[0-9]{4}$", indeks):
    print("❌ 'indeks' must match RN|SI|RI ###/#### (e.g., RN 123/2025)")
    sys.exit(1)

# 3. Partner logic
par_student = par_student or ""
par_indeks = par_indeks or ""

# Case A: both empty → OK
if par_student == "" and par_indeks == "":
    print("✔ Working alone")
    sys.exit(0)

# Case B: one empty, one filled → invalid
if (par_student == "") != (par_indeks == ""):
    print("❌ If partner is used, BOTH par.student and par.indeks must be filled.")
    sys.exit(1)

# Case C: indexed must be valid
if not re.match(r"^(RN|SI|RI) [0-9]{3}/[0-9]{4}$", par_indeks):
    print("❌ 'par.indeks' must match RN|SI|RI ###/####")
    sys.exit(1)

print("✔ info.yml is valid")
