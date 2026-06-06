# Dokumentacja audytu bezpieczeństwa uprawnień komponentów

**Obiekt analizy:** Plik źródłowy AndroidManifest.xml aplikacji ApiDemos  
**Plik wynikowy:** RiskyPermission.xml  

---

## 🗒️ 1. Podsumowanie odnalezionych rekordów ryzyka

W trakcie automatycznego skanowania struktury manifestu zidentyfikowano krytyczne punkty podatności:

* **Flaga podatności programistycznej:** Zmienna `Debuggable` ma status `true`. Stanowi to **poważną lukę bezpieczeństwa** — wdrożona w ten sposób aplikacja pozwala na podpięcie zewnętrznego debuggera w środowisku produkcyjnym i ułatwia inżynierię wsteczną.
* **Wykryte uprawnienia systemowe:** Odnaleziono uprawnienia dające szeroki dostęp do kluczowych funkcji urządzenia. Program może bez przeszkód łączyć się z siecią zewnętrzną (`INTERNET`), zapisywać dane lokalnie (`WRITE_EXTERNAL_STORAGE`), a także korzystać z modułów przechwytywania multimediów (`CAMERA`, `RECORD_AUDIO`) i wrażliwych danych użytkownika (`READ_CONTACTS`).

---

## 🧠 2. Wnioski inżynierskie i ocena ryzyka

Najbardziej problematycznym elementem struktury jest pozostawienie aktywnego trybu debugowania. Może to posłużyć osobom nieuprawnionym do podglądania procesów w pamięci RAM urządzenia lub wstrzykiwania złośliwego kodu podczas działania aplikacji (runtime). 

Szeroki wachlarz uprawnień do prywatnych zasobów (kontakty, mikrofon, aparat) w połączeniu z dostępem do sieci stwarza ryzyko nieautoryzowanego wycieku danych z telefonu, jeśli aplikacja zostałaby przejęta.

---

## 🛠️ 3. Sugerowane kroki naprawcze (Mitigacja)

1. **Blokada kompilacji:** Należy bezwzględnie usunąć parametr `android:debuggable="true"` z pliku manifestu lub upewnić się, że skrypty CI/CD (np. GitHub Actions, Jenkins) automatycznie wymuszają zmianę tej wartości na `false` przy generowaniu wersji produkcyjnej (Release).
2. **Zasada minimalnych uprawnień:** Przejrzeć wymagania biznesowe i usunąć z manifestu te uprawnienia, które nie są niezbędne do kluczowego działania programu.

---

**Raport przygotował:** [Twoje Imię, Numer Studenta]  
**Podpis i status weryfikacji:** Audyt zakończony - Wymagane poprawki deweloperskie