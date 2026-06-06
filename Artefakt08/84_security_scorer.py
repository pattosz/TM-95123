import os
import json
import xml.etree.ElementTree as ET

def calculate_security_score():
    xml_path = "RiskyPermission.xml"
    json_path = "83_vulnerabilities.json"
    output_txt_path = "84_risk_score.txt"
    
    print(">>> ZADANIE 8.4: OBLICZANIE SECURITY SCORE (ALGORITHM V1) <<<")
    
    # Stan początkowy punktacji systemu
    score = 100
    deductions = []

    # 1. ANALIZA FLAG Z MANIFESTU XML (Zadanie 8.1)
    if os.path.exists(xml_path):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            debuggable_elem = root.find(".//Debuggable")
            if debuggable_elem is not None and debuggable_elem.text == "true":
                score -= 30
                deductions.append("[-30] Flaga Debuggable jest AKTYWNA (High Risk)")
        except Exception as e:
            print(f"[WARN] Błąd parsowania pliku XML: {e}")
    else:
        print(f"[WARN] Brak pliku {xml_path}. Pomijam krok 1.")

    # 2. ANALIZA PODATNOŚCI Z PLIKU JSON (Zadanie 8.3)
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Obsługa struktury wygenerowanej w kroku 8.3 (lista 'issues' w słowniku)
            issues = data.get("issues", [])
            for v in issues:
                severity = v.get("severity", "").upper()
                lib_name = v.get("library", "unknown")
                
                if severity == "CRITICAL":
                    score -= 40
                    deductions.append(f"[-40] Krytyczna luka w {lib_name} (Critical)")
                elif severity == "HIGH":
                    score -= 20
                    deductions.append(f"[-20] Poważna luka w {lib_name} (High)")
                elif severity == "MEDIUM":
                    score -= 10
                    deductions.append(f"[-10] Średnia luka w {lib_name} (Medium)")
                elif severity == "LOW":
                    score -= 5
                    deductions.append(f"[-5] Niska podatność w {lib_name} (Low)")
        except Exception as e:
            print(f"[WARN] Błąd ładowania pliku JSON: {e}")
    else:
        print(f"[WARN] Brak pliku {json_path}. Pomijam krok 2.")

    # Zapewnienie, że punktacja nie spadnie poniżej zera
    if score < 0:
        score = 0

    # Określenie statusu końcowego na bazie wyniku
    if score >= 70:
        status_line = "📊 STATUS: PASSED (Aplikacja bezpieczna)"
        console_status = "[🏆] STATUS: PASSED (Aplikacja bezpieczna)"
    else:
        status_line = "[X] STATUS: REJECTED (Aplikacja niebezpieczna)"
        console_status = "[❌] STATUS: REJECTED (Aplikacja niebezpieczna)"

    # Formatowanie wyświetlania w terminalu pod zrzut ekranu
    print(f"\n[📊] WYNIK KOŃCOWY: {score}/100")
    print(console_status)

    # Przygotowanie zestawienia tekstowego do zapisu
    report_lines = [
        "=======================================\n",
        "     RAPORT AUTOMATYCZNEGO RYZYKA      \n",
        "=======================================\n",
        f"KOŃCOWY SECURITY SCORE: {score}/100\n",
        f"{status_line}\n\n",
        "Zidentyfikowane potrącenia punktowe:\n"
    ]
    
    if deductions:
        for item in deductions:
            report_lines.append(f" * {item}\n")
    else:
        report_lines.append(" * Brak uwag. Brak zarejestrowanych podatności.\n")

    # Zapis raportu do pliku tekstowego
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.writelines(report_lines)

if __name__ == "__main__":
    calculate_security_score()