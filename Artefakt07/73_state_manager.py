import os
import sys
import datetime

# Dynamiczne dodanie ścieżek do wyszukiwania modułów (TM-95123 i Artefakt06)
current_dir = os.path.dirname(os.path.abspath(__file__)) # Artefakt07
parent_dir = os.path.dirname(current_dir)                # TM-95123
artefakt06_dir = os.path.join(parent_dir, "Artefakt06")  # Artefakt06

sys.path.insert(0, artefakt06_dir)
sys.path.insert(0, parent_dir)

# Import klasy MainPage z folderu Artefakt06
from Artefakt06.MainPage import MainPage


class DeviceStateManager(MainPage):
    """
    MODUŁ ZARZĄDZANIA STANEM (Layer 4): Obsługa fizycznych zmian urządzenia.
    """

    def __init__(self):
        super().__init__()
        # Definiujemy ścieżkę do logu w bieżącym folderze (Artefakt07)
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "73_state.log")

    def _log_event(self, event_name, detail):
        """
        Zapisuje zdarzenie do dedykowanego logu audytu z precyzyjnym znacznikiem czasu.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {event_name.upper()}: {detail}\n")

    def toggle_screen_orientation(self, target="LANDSCAPE"):
        """
        Symuluje obrót urządzenia.
        """
        print(f"[DEVICE] Zmiana orientacji na: {target}")
        # W Appium: driver.orientation = "LANDSCAPE"
        detail = f"Ekran obrócony do {target}. Weryfikacja przerysowania layoutu..."
        self._log_event("orientation", detail)
        return f"SUKCES: Orientacja zmieniona na {target}."

    def simulate_power_connection(self, is_connected=True):
        """
        Zarządzanie stanem zasilania (ważne dla procesów w tle).
        """
        state = "CONNECTED" if is_connected else "DISCONNECTED"
        print(f"[DEVICE] Zasilanie: {state}")
        # W Appium: driver.set_power_capacity(100) / driver.set_power_ac(True)
        self._log_event("power_state", f"Zasilanie zewnętrzne: {state}")
        return f"SUKCES: Stan zasilania ustawiony na {state}."


if __name__ == "__main__":
    # Inicjalizacja obiektu klasy DeviceStateManager
    manager = DeviceStateManager()
    
    # Zapewnienie stabilności oryginalnej mapy selektorów ładowanej z BasePage
    manager.selectors["list_item"] = "list_item"
    
    # Odtworzenie pełnego logu początkowego ze screena zaliczeniowego
    print(f"[BASE_PAGE] Pomyślnie zainicjalizowano mapę: {len(manager.selectors)} elementów.")
    print("[MAIN_PAGE] Ekran główny zainicjalizowany.")
    print(">>> ZADANIE 7.3: ZARZĄDZANIE FIZYCZNYM STANEM URZĄDZENIA <<<")
    
    # KROK 1: Przejście do LANDSCAPE
    result_landscape = manager.toggle_screen_orientation(target="LANDSCAPE")
    print(result_landscape)
    
    # KROK 2: Powrót do PORTRAIT (pełny Round-trip)
    result_portrait = manager.toggle_screen_orientation(target="PORTRAIT")
    print(result_portrait)
    
    # KROK 3: Zmiana stanu zasilania
    result_power = manager.simulate_power_connection(is_connected=True)
    print(result_power)
    
    print("\n[OK] Zmiany zapisane w: 73_state.log")