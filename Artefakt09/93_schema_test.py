import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def test_json_schema():
    print(">>> ZADANIE 9.3: WALIDACJA STRUKTURY JSON (KONTRAKT) <<<")
    
    # Pobieramy dane z endpointu posts/1 (zgodnie z wymaganiami w tekście)
    url = "https://jsonplaceholder.typicode.com/posts/1"
    
    # DEFINICJA SCHEMATU (Nasz "odlew" danych z miniatury)
    # Określamy, że userId i id MUSZĄ być liczbami, a title i body tekstami
    expected_schema = {
        "type": "object",
        "properties": {
            "userId": {"type": "number"},
            "id": {"type": "number"},
            "title": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["userId", "id", "title"]  # Te pola są obowiązkowe
    }
    
    try:
        # Pobranie danych z API
        response = requests.get(url, timeout=5)
        response_data = response.json()
        
        # Walidacja pobranego JSON-a względem przygotowanego schematu
        validate(instance=response_data, schema=expected_schema)
        
        # Jeśli nie rzuciło wyjątku, kontrakt jest poprawny
        print("[SUCCESS] Kontrakt zachowany. Struktura JSON jest poprawna.")
        print(f"[DEBUG] Zweryfikowano pola dla obiektu ID: {response_data.get('id')}")
        
    except ValidationError as e:
        print(f"[FAIL] Błąd walidacji kontraktu (JSON Schema)! Szczegóły:\n{e.message}")
    except Exception as e:
        print(f"[ERROR] Wystąpił inny błąd podczas testu: {e}")

if __name__ == "__main__":
    test_json_schema()