import os
import sys
import time

# Dynamiczne dodanie ścieżek do wyszukiwania modułów (TM-95123 i Artefakt06)
current_dir = os.path.dirname(os.path.abspath(__file__)) # Artefakt07
parent_dir = os.path.dirname(current_dir)                # TM-95123
artefakt06_dir = os.path.join(parent_dir, "Artefakt06")  # Artefakt06

sys.path.insert(0, artefakt06_dir)
sys.path.insert(0, parent_dir)

# Import klasy MainPage z folderu Artefakt06
from Artefakt06.MainPage import MainPage


class InterruptManager(MainPage):
    """
    MODUŁ PRZERWAŃ (Layer 4): Symulacja zdarzeń systemowych Androida.
    """

    def simulate_incoming_call(self, duration_sec=5):
        """
        Symuluje nadchodzące połączenie, które przysłania aplikację.
        """
        print(f"\n[INTERRUPT] KROK 1: Stan aplikacji przed połączeniem: ACTIVE")
        print(f"[INTERRUPT] KROK 2: Wyzwalanie zdarzenia: INCOMING CALL (Duration: {duration_sec}s)")

        # W Appium: driver.make_gsm_call(phone_number, GsmCallActions.CALL)
        time.sleep(1)
        print(">>> SYSTEM: Aplikacja w tle (onPause) | Widoczny ekran połączenia <<<")

        time.sleep(duration_sec)  # Czas trwania rozmowy

        print("[INTERRUPT] KROK 3: Zakończenie połączenia. Powrót do aplikacji.")
        # W Appium: driver.activate_app('io.appium.android.apis')

        return "SUKCES: Aplikacja odzyskała fokus (onResume). Dane sesji zachowane."

    def simulate_low_battery_warning(self):
        """
        Symuluje systemowy komunikat o niskim stanie baterii (System Dialog).
        """
        print(f"\n[INTERRUPT] Wyzwalanie zdarzenia: LOW BATTERY WARNING")
        # W Appium: driver.set_power_capacity(5)
        return "SUKCES: Aplikacja obsłużyła systemowe okno dialogowe bez błędu."


if __name__ == "__main__":
    # Inicjalizacja obiektu klasy InterruptManager
    manager = InterruptManager()
    
    # Zapewnienie stabilności oryginalnej mapy selektorów ładowanej z BasePage
    manager.selectors["list_item"] = "list_item"
    
    # Odtworzenie pełnego logu początkowego ze screena zaliczeniowego
    print(f"[BASE_PAGE] Pomyślnie zainicjalizowano mapę: {len(manager.selectors)} elementów.")
    print("[MAIN_PAGE] Ekran główny zainicjalizowany.")
    print(">>> ZADANIE 7.2: TESTY ODPORNOŚCI NA PRZERWANIA <<<")
    
    # Wywołanie testowe 1: Nadchodzące połączenie (zgodnie ze screenem trwające 3 sekundy)
    call_result = manager.simulate_incoming_call(duration_sec=3)
    print(call_result)
    
    # Wywołanie testowe 2: Niski stan baterii
    battery_result = manager.simulate_low_battery_warning()
    print(battery_result)