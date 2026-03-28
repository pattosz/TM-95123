import os
import json
import xml.etree.ElementTree as ET

LAYOUT_DIR = "../Artefakt02/decompiled_apk/res/layout/"
OUTPUT_FILE = "53_selectors.json"

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def extract_ids_from_file(filepath):
    ids = set()

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        for elem in root.iter():
            attr = elem.attrib.get(ANDROID_NS + "id")
            if attr:
                # np. @+id/btn_login → btn_login
                clean_id = attr.split("/")[-1]
                ids.add(clean_id)

    except Exception:
        pass  # ignorujemy uszkodzone XML

    return ids


def scan_layouts(directory):
    all_ids = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                path = os.path.join(root, file)
                ids = extract_ids_from_file(path)
                all_ids.update(ids)

    return all_ids


def build_selector_map(ids):
    selectors = {}

    for _id in ids:
        # prosty mapping biznesowy (możesz rozbudować)
        key = _id.upper()
        selectors[key] = f"id/{_id}"

    return selectors


def main():
    if not os.path.exists(LAYOUT_DIR):
        print("❌ Folder layout nie istnieje")
        return

    ids = scan_layouts(LAYOUT_DIR)

    selectors = build_selector_map(ids)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(selectors, f, indent=4)

    print(f"[OK] Zmapowano {len(ids)} unikalnych elementów UI.")
    print(f"Artefakt zapisany: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()