import os
import xml.etree.ElementTree as ET
from MainPage import MainPage

def run_integrity_test():
    print(">>> ZADANIE 6.5: INTEGRITY AUDIT - FINAL CHECK <<<")
    
    results = []
    
    try:
        page = MainPage()
        results.append(("POM_Initialization", "PASSED", "Klasy BasePage i MainPage dzialaja poprawnie."))
    except Exception as e:
        results.append(("POM_Initialization", "FAILED", str(e)))

    if os.path.exists("64_audit_report.md"):
        results.append(("Documentation_Check", "PASSED", "Raport inzynierski MD zostal odnaleziony."))
    else:
        results.append(("Documentation_Check", "FAILED", "Brak pliku 64_audit_report.md!"))

    try:
        count = len(page.selectors)
        if count > 0:
            results.append(("Data_Layer_Connection", "PASSED", f"Wczytano {count} selektorow z Bloku 5."))
        else:
            results.append(("Data_Layer_Connection", "FAILED", "Mapa selektorow jest pusta!"))
    except:
        results.append(("Data_Layer_Connection", "FAILED", "Nie udalo sie policzyc selektorow."))

    print("\n--- WYNIKI AUDYTU ARCHITEKTURY ---")
    root = ET.Element("testsuite", name="FrameworkIntegrityCheck")
    
    for name, status, msg in results:
        print(f"[{status}] {name}: {msg}")
        testcase = ET.SubElement(root, "testcase", name=name)
        if status == "FAILED":
            ET.SubElement(testcase, "failure").text = msg
        else:
            testcase.set("status", "passed")

    tree = ET.ElementTree(root)
    tree.write("65_final_report.xml")
    
    print(f"\n[ZAKONCZONO] Blok 6 zweryfikowany. Raport: 65_final_report.xml")

if __name__ == "__main__":
    run_integrity_test()