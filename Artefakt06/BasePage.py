import json
import os

class BasePage:
    def __init__(self, selectors_filename="53_selectors.json"):
        current_dir = os.path.dirname(__file__)
        selectors_path = os.path.join(current_dir, "..", "Artefakt05", selectors_filename)
        self.final_path = os.path.abspath(selectors_path)

        with open(self.final_path, "r") as f:
            self.selectors = json.load(f)

    def get_selector(self, business_name):
        return self.selectors.get(business_name, None)

if __name__ == "__main__":
    try:
        bp = BasePage()
        print(f"[BASE_PAGE] Pomyślnie zainicjalizowano mapę: {len(bp.selectors)} elementów.")
        
        key_to_check = 'ADD'
        result = bp.get_selector(key_to_check)
        print(f"Weryfikacja klucza '{key_to_check}': {result}")
        
    except FileNotFoundError:
        print(f"BŁĄD: Nie odnaleziono pliku pod ścieżką: {selectors_path}")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")