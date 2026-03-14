import xml.etree.ElementTree as ET
import glob
import os
import json

# Funkcja do wydobywania ID i tagu z layoutów
def mine_selectors(path):
    selectors = []  # Lista do przechowywania wyników

    # Przechodzimy przez wszystkie pliki XML w katalogu (rekursywnie)
    for file in glob.glob(path + "/**/*.xml", recursive=True):
        try:
            # Parsowanie pliku XML
            tree = ET.parse(file)
            root = tree.getroot()

            # Iteracja po elementach XML
            for elem in root.iter():
                # Wyszukiwanie atrybutu 'id' w elemencie
                res_id = elem.get('{http://schemas.android.com/apk/res/android}id')
                res_tag = elem.tag  # Pobranie tagu elementu

                if res_id:  # Jeśli istnieje 'id', dodajemy dane do listy
                    selectors.append({
                        'file': os.path.basename(file),  # Zapisujemy tylko nazwę pliku
                        'id': res_id.split('/')[-1],  # Pobieramy nazwę ID, nie pełną ścieżkę
                        'tag': res_tag
                    })
        except ET.ParseError:
            print(f"Błąd przy parsowaniu pliku: {file}")

    return selectors

# Funkcja do zapisania wyników w formacie JSON
def save_selectors(selectors, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(selectors, f, indent=4, ensure_ascii=False)

# Główna funkcja
def main():
    path = "../Artefakt02/decompiled_apk/res/layout"  # Ścieżka do folderu z plikami XML
    output_file = "miner_report.json"  # Nazwa pliku wynikowego

    # Wywołanie funkcji do parsowania layoutów
    selectors = mine_selectors(path)

    # Jeśli znaleziono jakiekolwiek selektory, zapisujemy je do pliku
    if selectors:
        save_selectors(selectors, output_file)
        print(f"Znaleziono {len(selectors)} selektorów. Wynik zapisano w {output_file}")
    else:
        print("Brak selektorów w podanym katalogu.")

if __name__ == "__main__":
    main()