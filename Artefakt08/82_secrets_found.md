# Dokumentacja weryfikacji wycieków danych i sekretów (Secrets Audit)

**Laboratorium badawcze:** Blok 8 - Analiza kodu źródłowego  
**Specjalista ds. QA:** [Patryk Cieślik, 95123]  
**Data wygenerowania:** [06-06-2026]

---

## 🔥 1. Najpoważniejsze incydenty bezpieczeństwa (Wysokie Ryzyko)

Poniższe znaleziska automatyczne zostały zakwalifikowane jako realne podatności i wymagają natychmiastowej zmiany w repozytorium:

1. `[URL_Endpoint] -> http://www.example.com/lala/foobar@example.com`
   * **Analiza zagrożenia:** Ciąg zawiera zakodowany bezpośrednio adres e-mail wewnątrz ścieżki URL. Może to być pozostałość po testowych kontach programistów lub aktywny punkt uwierzytelniania, co ułatwia przeprowadzenie ukierunkowanego ataku.
2. `[Potential_Secret] -> password`
   * **Analiza zagrożenia:** Słowo kluczowe wykryte w pliku konfiguracyjnym zasobów sugeruje, że aplikacja przechowuje statyczne, domyślne hasło dostępowe (np. do lokalnej bazy danych lub konta testowego).
3. `[Potential_Secret] -> reset_password_warning`
   * **Analiza zagrożenia:** Element powiązany logicznie z mechanizmami odzyskiwania dostępu. Bezpośrednie umieszczenie go w plikach zasobów pozwala na analizę i potencjalne manipulowanie przepływem resetowania haseł.

---

## 🟢 2. Znaleziska zaklasyfikowane jako fałszywy alarm (False Positive)

Te wpisy wywołały alert skanera ze względu na dopasowanie reguł Regex, jednak ręczna weryfikacja wykazała, że stanowią one bezpieczne elementy interfejsu:

1. `[URL_Endpoint] -> http://www.google.com`
   * **Powód odrzucenia:** Jest to standardowy adres URL wyszukiwarki sieciowej, wykorzystywany prawdopodobnie do zwykłego testu łączności internetowej lub przekierowania użytkownika do pomocy. Brak znamion wycieku.
2. `[API_Key_Format] -> remote_service_stopped`
   * **Powód odrzucenia:** Wyrażenie regularne wychwyciło długi ciąg znaków z podkreśleniami, ale w rzeczywistości jest to zwykły identyfikator tekstowy (String ID) informujący o zatrzymaniu usługi systemowej.
3. `[API_Key_Format] -> secure_view_step4_heading`
   * **Powód odrzucenia:** Klasyczny identyfikator zasobu UI odpowiedzialny za nagłówek czwartego kroku samouczka. Skaner potraktował go podejrzliwie wyłącznie ze względu na długość i strukturę frazy.

---

## 🧠 Wnioski i podsumowanie techniczne

Automatyczne skanowanie oparte na wyrażeniach regularnych (RegEx) to potężne narzędzie, które generuje jednak bardzo dużą ilość szumu informacyjnego. Rola inżyniera testów automatycznych (SDET) polega na krytycznej ocenie wyników, aby deweloperzy otrzymywali wyłącznie potwierdzone zgłoszenia błędów, zamiast setek niegroźnych nazw zasobów widoku.

**Status weryfikacji:** Wymagana selektywna czystka kodu (korekta haseł i urli testowych).