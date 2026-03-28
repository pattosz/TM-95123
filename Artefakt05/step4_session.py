import json
import os
from datetime import datetime

CAPS_FILE = "51_caps.json"
SELECTORS_FILE = "53_selectors.json"
LOG_FILE = "54_session.log"


def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Brak pliku: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_cap(caps, key):
    # obsługa appium: i bez prefixu
    return caps.get(key) or caps.get(f"appium:{key}")


def build_report(caps, selectors):
    app_pkg = get_cap(caps, "appPackage")
    app_act = get_cap(caps, "appActivity")
    dev_name = get_cap(caps, "deviceName")

    ui_count = len(selectors)

    if not app_pkg or not app_act:
        status = "FAILED: Missing appPackage or appActivity!"
    else:
        status = "READY TO CONNECT"

    report = []
    report.append(">>> ZADANIE 5.4: INTEGRACJA ARTEFAKTÓW (STABLE BUILD) <<<\n")
    report.append("=== ARTEFAKT 5.4: SESSION READINESS REPORT ===")
    report.append(f"Target App     : {app_pkg}")
    report.append(f"Main Activity  : {app_act}")
    report.append(f"Device         : {dev_name}")
    report.append(f"UI Elements    : {ui_count} loaded")
    report.append(f"Status         : {status}")

    return "\n".join(report), status


def save_log(report):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"{datetime.now()}\n")
        f.write(report)


def main():
    try:
        caps = load_json(CAPS_FILE)
        selectors = load_json(SELECTORS_FILE)

        report, status = build_report(caps, selectors)

        print(report)
        save_log(report)

        print(f"\n[OK] Log zapisany: {LOG_FILE}")

        # (opcjonalnie) przygotowanie Options – bez fizycznego łączenia
        try:
            from appium.options.android import UiAutomator2Options

            options = UiAutomator2Options().load_capabilities(caps)
            print("[INFO] Obiekt Appium Options przygotowany poprawnie")

        except Exception:
            print("[WARN] Appium nie jest zainstalowane – pominięto tworzenie Options")

    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()