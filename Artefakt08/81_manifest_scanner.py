import os
import xml.etree.ElementTree as ET

def run_manifest_audit():
    # Ścieżki do plików wejściowych i wyjściowych
    manifest_path = os.path.join("..", "Artefakt02", "decompiled_apk", "AndroidManifest.xml")
    output_xml_path = "RiskyPermission.xml"
    
    print(f">>> URUCHOMIENIE AUDYTU: {manifest_path} <<<")
    
    # Lista kontrolna niebezpiecznych uprawnień (zgodnie z listą ze zdjęcia)
    dangerous_list = [
        'READ_CONTACTS',
        'WRITE_EXTERNAL_STORAGE',
        'ACCESS_FINE_LOCATION',
        'INTERNET',
        'CAMERA',
        'RECORD_AUDIO'
    ]
    
    if not os.path.exists(manifest_path):
        print(f"BŁĄD: Nie znaleziono pliku manifestu pod ścieżką: {manifest_path}")
        return

    # Inicjalizacja parsera XML
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    
    # Definicja przestrzeni nazw Androida
    ns = {'android': 'http://schemas.android.com/apk/res/android'}
    
    # 1. Sprawdzenie flagi debuggable w sekcji <application>
    application_elem = root.find('application')
    debuggable_status = "false"
    if application_elem is not None:
        debuggable_attr = application_elem.get('{http://schemas.android.com/apk/res/android}debuggable')
        if debuggable_attr == "true":
            debuggable_status = "true"
            
    # 2. Szukanie niebezpiecznych uprawnień
    found_permissions = []
    for perm in root.findall('uses-permission'):
        name = perm.get('{http://schemas.android.com/apk/res/android}name')
        if name:
            short_name = name.split('.')[-1]
            if short_name in dangerous_list:
                found_permissions.append(name)
                
    # Wypisanie logów w konsoli (dokładne odzwierciedlenie wyniku ze zlecenia)
    print(f"[SUCCESS] Wygenerowano czytelny raport: {output_xml_path}")
    print(f"[INFO] Znaleziono {len(found_permissions)} podejrzanych uprawnień.")
    if debuggable_status == "true":
        print("[! ]ALERT! Wykryto aktywną flagę DEBUGGABLE!")

    # 3. Budowanie pliku wynikowego RiskyPermission.xml
    security_audit = ET.Element("SecurityAudit", app="ApiDemos_Security_Check", status="ReviewRequired")
    
    flags = ET.SubElement(security_audit, "Flags")
    debuggable_elem = ET.SubElement(flags, "Debuggable")
    debuggable_elem.text = debuggable_status
    
    risky_perms_elem = ET.SubElement(security_audit, "RiskyPermissions")
    for p in found_permissions:
        p_elem = ET.SubElement(risky_perms_elem, "Permission")
        p_elem.text = p
        
    # Zapis do pliku z odpowiednim wcięciem (formatowanie XML)
    ET.indent(tree, space="    ", level=0) # dla estetyki struktury
    raw_xml = ET.tostring(security_audit, encoding='utf-8')
    
    # Ręczne dodanie deklaracji xml na początku oraz sformatowanie wcięć dla czystości zapisu
    from xml.dom import minidom
    pretty_xml = minidom.parseString(raw_xml).toprettyxml(indent="    ", encoding="UTF-8")
    
    with open(output_xml_path, "wb") as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    run_manifest_audit()