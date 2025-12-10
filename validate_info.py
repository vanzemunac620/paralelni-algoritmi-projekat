import sys
import re
import yaml

index_pattern = r"^(RN|SI|RI) [0-9]{3}/[0-9]{4}$"

DEFAULT_INDEX = "RN 000/2025"

# -----------------------------------------------
# 1. Load YAML with proper error distinction
# -----------------------------------------------
try:
    with open("info.yml", "r", encoding="utf8") as f:
        content = f.read()
except FileNotFoundError:
    print("❌ info.yml is missing.")
    sys.exit(1)

try:
    data = yaml.safe_load(content)
except yaml.YAMLError:
    print("❌ info.yml exists but contains invalid YAML format.")
    sys.exit(1)
except Exception:
    print("❌ Unknown error while reading info.yml.")
    sys.exit(1)

if not isinstance(data, dict):
    print("❌ info.yml is present but does not contain a valid YAML mapping.")
    sys.exit(1)

# -----------------------------------------------
# 2. Extract main fields
# -----------------------------------------------
student = (data.get("student") or "").strip()
indeks = (data.get("indeks") or "").strip()

# -----------------------------------------------
# 3. Validate main student
# -----------------------------------------------
if not student:
    print("❌ 'student' field must not be empty.")
    sys.exit(1)

# (NO default-name rejection — student may be Petar Petrović)

# -----------------------------------------------
# 4. Validate main indeks
# -----------------------------------------------
if not re.match(index_pattern, indeks):
    print("❌ 'indeks' must match RN|SI|RI ###/#### (e.g., RN 123/2025)")
    sys.exit(1)

# Reject the template placeholder
if indeks == DEFAULT_INDEX:
    print("❌ Indeks is still the default value. Have you updated info.yml?")
    sys.exit(1)

# -----------------------------------------------
# 5. Extract partner block
# -----------------------------------------------
par = data.get("par") or {}
par_student = (par.get("student") or "").strip()
par_index = (par.get("indeks") or "").strip()

# -----------------------------------------------
# Partner logic (strict)
# Allowed:
#   A) both empty
#   B) student non-empty + valid index
# Not allowed:
#   - index non-empty but student empty
#   - student non-empty but index invalid
# -----------------------------------------------

# Case A: both empty → OK
if par_student == "" and par_index == "":
    print("✔ Working alone")
    sys.exit(0)

# Case B: student non-empty + valid index
if par_student != "":
    if re.match(index_pattern, par_index):
        print("✔ Partner info valid")
        sys.exit(0)
    else:
        print("❌ par.indeks must match RN|SI|RI ###/#### when par.student is provided.")
        sys.exit(1)

# Case C: index provided but student empty → invalid
print("❌ par.indeks provided but par.student is empty.")
sys.exit(1)

