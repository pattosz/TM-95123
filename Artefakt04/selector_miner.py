import xml.etree.ElementTree as ET
import glob
import json
import os

def mine_selectors(path):
    result = []

    for file in glob.glob(os.path.join(path, "**", "*.xml"), recursive=True):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            for elem in root.iter():
                # Pobranie wszystkich atrybutów bez namespace
                attribs = {k.split('}')[-1]: v for k, v in elem.attrib.items()}
                
                res_id = attribs.get("id")
                accessibility = attribs.get("contentDescription")

                if res_id or accessibility:
                    element_info = {
                        "file": os.path.basename(file),
                    }
                    if res_id:
                        element_info["id"] = res_id.split("/")[-1]
                    if accessibility:
                        element_info["accessibility"] = accessibility
                    result.append(element_info)
        except ET.ParseError as e:
            print(f"Nie można sparsować pliku {file}: {e}")

    with open("miner_report.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Znaleziono {len(result)} elementów. Wynik zapisany w miner_report.json")

# Wywołanie funkcji
mine_selectors("C:/TestowanieMobilne/TM-95123/Artefakt02/decompiled_apk/res/layout")
# Zmienic sciezke