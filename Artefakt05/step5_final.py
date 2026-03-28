import json
import xml.etree.ElementTree as ET
import os

CAPS_FILE = "51_caps.json"
SELECTORS_FILE = "53_selectors.json"
OUTPUT_XML = "55_result.xml"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_cap(caps, key):
    return caps.get(key) or caps.get(f"appium:{key}")


def run_consistency_test():
    caps = load_json(CAPS_FILE)
    ui_map = load_json(SELECTORS_FILE)

    feedback_report = []

    current_pkg = get_cap(caps, "appPackage")

    # --- 1. Weryfikacja Pakietu ---
    if current_pkg == "io.appium.android.apis":
        feedback_report.append({
            "feature": "Identyfikacja Aplikacji",
            "status": "ZGODNY",
            "message": f"Pakiet {current_pkg} poprawnie zmapowany."
        })
    else:
        feedback_report.append({
            "feature": "Identyfikacja Aplikacji",
            "status": "DO POPRAWY",
            "message": f"Niezgodność pakietu. Wykryto {current_pkg}, sprawdź konfigurację manifestu."
        })

    # --- 2. Weryfikacja UI ---
    target_element = "ACCESSIBILITY"

    # obsługa obu formatów JSON (dict lub {"selectors": {...}})
    selectors = ui_map.get("selectors") if isinstance(ui_map, dict) and "selectors" in ui_map else ui_map

    if target_element in selectors:
        feedback_report.append({
            "feature": "Dostępność UI",
            "status": "ZGODNY",
            "message": f"Element {target_element} jest dostępny w layoutach."
        })
    else:
        suggestions = list(selectors.keys())[:3]
        feedback_report.append({
            "feature": "Dostępność UI",
            "status": "INFORMACJA",
            "message": f"Nie odnaleziono ID '{target_element}'. Sugestia: Zweryfikuj czy element nie zmienił nazwy na jedną z dostępnych: {suggestions}."
        })

    return feedback_report


def generate_junit_xml(feedback):
    testsuite = ET.Element("testsuite")
    testsuite.set("name", "FinalConsistencySuite")
    testsuite.set("tests", str(len(feedback)))

    failures = 0

    for item in feedback:
        testcase = ET.SubElement(testsuite, "testcase")
        testcase.set("name", item["feature"])

        if item["status"] == "DO POPRAWY":
            failures += 1
            failure = ET.SubElement(testcase, "failure")
            failure.text = item["message"]

    testsuite.set("failures", str(failures))

    tree = ET.ElementTree(testsuite)
    tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)


def print_feedback(feedback):
    print(">>> ZADANIE 5.5: GENEROWANIE RAPORTU FEEDBACKU DLA DEWELOPERA <<<\n")
    print("--- FEEDBACK DLA TWÓRCÓW APLIKACJI ---")

    for item in feedback:
        print(f"[{item['status']}] {item['feature']}: {item['message']}")

    print(f"\n[INFO] Blok 5 zakończony. Raport opisowy gotowy: {OUTPUT_XML}")


def main():
    if not os.path.exists(CAPS_FILE) or not os.path.exists(SELECTORS_FILE):
        print("❌ Brak wymaganych plików JSON")
        return

    feedback = run_consistency_test()
    generate_junit_xml(feedback)
    print_feedback(feedback)


if __name__ == "__main__":
    main()