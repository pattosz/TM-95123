import os
import json
import xml.etree.ElementTree as ET

# Ścieżka do manifestu
MANIFEST_PATH = "../Artefakt02/decompiled_apk/AndroidManifest.xml"

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"

def find_main_activity(manifest_path):
    tree = ET.parse(manifest_path)
    root = tree.getroot()

    package_name = root.attrib.get("package")

    for application in root.findall("application"):
        for activity in application.findall("activity"):
            for intent_filter in activity.findall("intent-filter"):

                has_main = False
                has_launcher = False

                for action in intent_filter.findall("action"):
                    name = action.attrib.get(ANDROID_NS + "name")
                    if name == "android.intent.action.MAIN":
                        has_main = True

                for category in intent_filter.findall("category"):
                    name = category.attrib.get(ANDROID_NS + "name")
                    if name == "android.intent.category.LAUNCHER":
                        has_launcher = True

                if has_main and has_launcher:
                    activity_name = activity.attrib.get(ANDROID_NS + "name")
                    return package_name, activity_name

    return None, None


def main():
    if not os.path.exists(MANIFEST_PATH):
        print("❌ Nie znaleziono AndroidManifest.xml")
        return

    package, activity = find_main_activity(MANIFEST_PATH)

    if not package or not activity:
        print("❌ Nie znaleziono MAIN/LAUNCHER activity")
        return

    caps = {
        "platformName": "Android",
        "automationName": "UiAutomator2",
        "appPackage": package,
        "appActivity": activity,
        "deviceName": "emulator-5554",
        "noReset": True
    }

    with open("51_caps.json", "w") as f:
        json.dump(caps, f, indent=4)

    print(f"Sukces! Wykryto: {package} / {activity}")


if __name__ == "__main__":
    main()