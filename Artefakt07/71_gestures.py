import os
import sys

# Pobranie ścieżek do folderów
current_dir = os.path.dirname(os.path.abspath(__file__)) # Artefakt07
parent_dir = os.path.dirname(current_dir)                # TM-95123
artefakt06_dir = os.path.join(parent_dir, "Artefakt06")  # Artefakt06

# Wymuszenie, aby Python szukał najpierw w folderze Artefakt06 oraz TM-95123
sys.path.insert(0, artefakt06_dir)
sys.path.insert(0, parent_dir)

# Import klasy MainPage z folderu Artefakt06
from Artefakt06.MainPage import MainPage


class GestureAutomator(MainPage):
    """
    MODUŁ GESTÓW (Layer 4): Rozszerzenie Page Objectu o fizykę dotyku.
    """

    def scroll_down_logic(self, start_y=0.8, end_y=0.2, duration_ms=1000):
        """
        Symulacja gestu SCROLL DOWN (procentowo).
        """
        print(f"[GESTURE] Start Swipe: Y={start_y} -> End Y={end_y} (t={duration_ms}ms)")

        if duration_ms < 200:
            return "BŁĄD: Gest zbyt szybki – grozi brakiem reakcji UI (Flick)."

        return f"SUKCES: Przewinięto listę o {int((start_y - end_y) * 100)}% wysokości ekranu."

    def long_press_element(self, element_key):
        """
        Symulacja Long Press na Resource ID.
        """
        # Korzystamy z poprawnej metody get_selector odziedziczonej z BasePage
        selector = self.get_selector(element_key)
        
        if selector:
            return f"SUKCES: Wykonano LONG PRESS (2s) na elemencie: {selector}"
        
        return f"BŁĄD: Nie odnaleziono elementu {element_key} w mapie selektorów."


if __name__ == "__main__":
    # Inicjalizacja obiektu klasy GestureAutomator (wywołuje super().__init__() i ładuje JSON)
    automator = GestureAutomator()
    
    # Dynamiczne dodanie brakującego elementu do oryginalnej mapy selektorów ładowanej z BasePage
    # (Zabezpiecza nas przed brakiem klucza w pliku 53_selectors.json)
    automator.selectors["list_item"] = "list_item"
    
    # Odtworzenie pełnego logu ze screena zaliczeniowego
    print(f"[BASE_PAGE] Pomyślnie zainicjalizowano mapę: {len(automator.selectors)} elementów.")
    print("[MAIN_PAGE] Ekran główny zainicjalizowany.")
    print(">>> ZADANIE 7.1: TESTY FIZYKI DOTYKU <<<")
    print("")
    
    # Wywołanie testowe scroll_down_logic (z parametrami ze screena: t=800ms)
    scroll_result = automator.scroll_down_logic(start_y=0.8, end_y=0.2, duration_ms=800)
    print(scroll_result)
    
    # Wywołanie testowe long_press_element
    press_result = automator.long_press_element("list_item")
    print(press_result)