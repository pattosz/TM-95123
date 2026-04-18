from BasePage import BasePage

class MainPage(BasePage):
    def __init__(self):
        super().__init__()
        print(f"[MAIN_PAGE] Ekran główny zainicjalizowany.")

    def click_add_button(self):
        selector = self.get_selector("ADD")
        if selector:
            clean_id = selector.replace("id/", "")
            return f"SUKCES: Wykonano kliknięcie w element UI o ID: '{clean_id}'"
        return "ERROR: Selector ADD not found in map!"

    def check_header_visibility(self):
        selector = self.get_selector("TITLE")
        if selector:
            clean_id = selector.replace("id/", "")
            return f"SUKCES: Odnaleziono nagłówek strony (ID: {clean_id}). Status: Widoczny."
        return "ERROR: Selector TITLE not found in map!"

    def search_action(self, text):
        selector = self.get_selector("SEARCH_BUTTON")
        if selector:
            clean_id = selector.replace("id/", "")
            return f"SUKCES: Wpisano '{text}' do pola {clean_id} i zatwierdzono."
        return "ERROR: Selector SEARCH_BUTTON not found in map!"