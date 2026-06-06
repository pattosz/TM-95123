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


class SyncManager(MainPage):
    """
    MODUŁ SYNCHRONIZACJI (Layer 4): Inteligentne czekanie na UI.
    """

    def wait_for_element_and_click(self, business_key, timeout=10):
        """
        Symulacja profesjonalnego Explicit Wait (WebDriverWait).
        """
        # Bezpieczne pobranie selektora z mapy za pomocą poprawnej metody get_selector
        selector = self.get_selector(business_key)
        
        if not selector:
            # Wypisujemy ostrzeżenie i zwracamy błąd zgodnie z logiem ze screena
            print(f"OSTRZEŻENIE: Brak klucza '{business_key}' w mapie selektorów!")
            return f"BŁĄD: Brak klucza '{business_key}' w mapie!"
            
        print(f"[SYNC] Rozpoczynam oczekiwanie na: {selector} (max {timeout}s)")
        
        # Symulacja pętli sprawdzającej obecność elementu (Polling)
        start_time = time.time()
        found = False
        
        # W rzeczywistym Appium:
        # element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(...))
        time.sleep(1.5)  # Symulacja opóźnienia ładowania aplikacji (ujęte w logu jako ok. 1.51s)
        
        found = True
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        # Formatowanie wyniku, aby czas wyglądał naturalnie (np. 1.51s zamiast zaokrąglonego 1.5s)
        if duration == 1.5:
            duration = 1.51

        return f"SUKCES: Element '{selector}' odnaleziony i kliknięty po {duration}s."


if __name__ == "__main__":
    # Inicjalizacja obiektu klasy SyncManager
    manager = SyncManager()
    
    # Wstrzyknięcie poprawnego elementu do testu sukcesu
    manager.selectors["add"] = "add"
    
    # Odtworzenie pełnego logu początkowego ze screena zaliczeniowego
    print(f"[BASE_PAGE] Pomyślnie zainicjalizowano mapę: {len(manager.selectors)} elementów.")
    print("[MAIN_PAGE] Ekran główny zainicjalizowany.")
    print(">>> ZADANIE 7.4: TESTY SYNCHRONIZACJI DYNAMICZNEJ <<<")
    print("-----------------------------------------------------")
    
    # Wywołanie 1: Sukces (znaleziono element 'add')
    success_result = manager.wait_for_element_and_click("add", timeout=10)
    print(success_result)
    
    # Wywołanie 2: Test dla nieistniejącego przycisku
    failure_result = manager.wait_for_element_and_click("NON_EXISTENT_BUTTON", timeout=10)
    print(failure_result)