import xml.etree.ElementTree as ET
import glob
import os
import json

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def check_accessibility(path):
    issues = []

    for file in glob.glob(path + "/**/*.xml", recursive=True):
        try:
            tree = ET.parse(file)
            root = tree.getroot()

            for elem in root.iter():

                text = elem.get(ANDROID_NS + "text")
                content_desc = elem.get(ANDROID_NS + "contentDescription")
                elem_id = elem.get(ANDROID_NS + "id")

                # element ma tekst ale brak contentDescription
                if text and not content_desc:
                    issues.append({
                        "file": os.path.basename(file),
                        "tag": elem.tag,
                        "id": elem_id.split("/")[-1] if elem_id else None,
                        "text": text
                    })

        except ET.ParseError:
            print(f"Błąd parsowania: {file}")

    return issues


def save_report(data):
    with open("a11y_report.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    layout_path = "../Artefakt02/decompiled_apk/res/layout"

    issues = check_accessibility(layout_path)

    save_report(issues)

    print(f"Znaleziono {len(issues)} potencjalnych luk dostępności.")
    print("Raport zapisano w a11y_report.json")


if __name__ == "__main__":
    main()