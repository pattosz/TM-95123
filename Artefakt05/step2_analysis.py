import os
import xml.etree.ElementTree as ET

MANIFEST_PATH = "../Artefakt02/decompiled_apk/AndroidManifest.xml"
LOG_FILE = "52_inspection.log"

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


def parse_manifest(path):
    tree = ET.parse(path)
    root = tree.getroot()

    package = root.attrib.get("package")

    # Permissions
    permissions = []
    for perm in root.findall("uses-permission"):
        name = perm.attrib.get(ANDROID_NS + "name")
        if name:
            permissions.append(name)

    # Activities
    activities = []
    for app in root.findall("application"):
        for activity in app.findall("activity"):
            name = activity.attrib.get(ANDROID_NS + "name")
            if name:
                activities.append(name)

    return package, permissions, activities


def generate_report(package, permissions, activities):
    report = []
    report.append("=== ARTEFAKT 5.2: RAPORT ANALIZY SYSTEMOWEJ ===\n")
    report.append(f"Pakiet główny: {package}")
    report.append(f"Liczba Activity: {len(activities)}\n")

    report.append("Kluczowe Uprawnienia (Co aplikacja chce robić):")
    for p in permissions:
        report.append(f"- {p}")

    return "\n".join(report)


def main():
    if not os.path.exists(MANIFEST_PATH):
        print("❌ Nie znaleziono AndroidManifest.xml")
        return

    package, permissions, activities = parse_manifest(MANIFEST_PATH)

    report = generate_report(package, permissions, activities)

    # print do terminala
    print(report)

    # zapis do pliku
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n[OK] Sukces! Artefakt zapisany jako: {LOG_FILE}")


if __name__ == "__main__":
    main()