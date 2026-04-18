from MainPage import MainPage

def run_pom_test():
    page = MainPage()
    
    print(">>> ZADANIE 6.3: TEST SCENARIUSZA W ARCHITEKTURZE POM <<<")
    print(f"[BASE_PAGE] Pomyślnie zainicjalizowano mapę: {len(page.selectors)} elementów.")
    print(f"[MAIN_PAGE] Ekran główny zainicjalizowany.")
    
    step1 = page.check_header_visibility()
    step2 = page.click_add_button()
    step3 = page.search_action("Automatyzacja Mobilna")
    
    print("\n--- PRZEBIEG SCENARIUSZA TESTOWEGO ---")
    print(f"KROK 1: {step1}")
    print(f"KROK 2: {step2}")
    print(f"KROK 3: {step3}")
    
    log_content = f"{step1}\n{step2}\n{step3}"
    
    with open("64_pom_audit.log", "w") as f:
        f.write(f"Test Execution Log:\n{log_content}")
    
    print("\n[OK] Scenariusz wykonany. Log audytu zapisany w 64_pom_audit.log")

if __name__ == "__main__":
    run_pom_test()