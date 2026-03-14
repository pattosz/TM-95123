import json
from collections import Counter
import os

# Ścieżka do pliku z danymi z Automated ID Mining
MINER_FILE = "miner_report.json"
REPORT_FILE = "stability_report.json"

# Próg krytyczny CDI (w procentach)
CDI_THRESHOLD = 50.0

# Wczytanie danych z miner_report.json
if not os.path.exists(MINER_FILE):
    print(f"Nie znaleziono pliku {MINER_FILE}. Najpierw uruchom selector_miner.py")
    exit(1)

with open(MINER_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Zliczanie wystąpień klas UI (przyjmujemy id jako proxy klasy)
# W prawdziwych aplikacjach można też wyciągać tag XML jako typ widoku
class_counts = Counter()
for elem in data:
    # Przyjmujemy, że id może zawierać typ komponentu np. "TextView", "Button"
    # Jeśli brak info, przypiszemy "Unknown"
    if "id" in elem and elem["id"]:
        if "TextView" in elem["id"]:
            class_type = "TextView"
        elif "Button" in elem["id"]:
            class_type = "Button"
        else:
            class_type = "Other"
    else:
        class_type = "Unknown"
    class_counts[class_type] += 1

total = sum(class_counts.values())
report = []

for cls, count in class_counts.items():
    cdi = (count / total) * 100 if total > 0 else 0
    risk = "HIGH" if cdi > CDI_THRESHOLD else "LOW"
    report.append({
        "class": cls,
        "count": count,
        "CDI_percent": round(cdi, 1),
        "risk": risk
    })

# Zapis raportu do pliku
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=4, ensure_ascii=False)

print(f"Stability audit zakończony. Wynik zapisano w {REPORT_FILE}")