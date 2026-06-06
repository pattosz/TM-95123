# 🗺️ RAPORT Z AUDYTU BEZPIECZEŃSTWA: APIDEMOS

**Data przeprowadzenia:** 06-06-2026  
**Audytor:** [Patryk Cieślik, 95123]  
**Projekt badawczy:** Analiza podatności i szczelności kodu aplikacji mobilnej  

---

## 📊 1. OCENA KOŃCOWA (SECURITY SCORE)

* **WYNIK OGÓLNY:** 0/100
* **STATUS:** 🔴 REJECTED / NEEDS FIX (Kompilacja niedopuszczona do dystrybucji produkcyjnej)

---

## 🛡️ 2. KLUCZOWE OBSZARY RYZYKA

### 🔍 A. Konfiguracja Systemowa (Zadanie 8.1)
* **Problem:** W manifeście aplikacji wykryto aktywną flagę deweloperską `android:debuggable="true"`.
* **Wpływ:** Krytyczny błąd wdrożeniowy. Pozwala napastnikowi na podpięcie zdalnego debuggera do uruchomionego procesu aplikacji, odczyt zawartości pamięci RAM w czasie rzeczywistym oraz drastycznie ułatwia inżynierię wsteczną.

### 🔑 B. Wycieki Danych (Zadanie 8.2)
* **Problem:** W plikach zasobów (`strings.xml`) znaleziono zahardkodowane dane uwierzytelniające (frazy typu *password*) oraz adresy URL z jawnymi danymi kont testowych.
* **Wpływ:** Średni/Wysoki. Potencjalny agresor po dekompilacji pliku APK uzyskuje natychmiastowy dostęp do punktów styku z API oraz kont bazodanowych używanych w fazie developmentu.

### 📦 C. Biblioteki Zewnętrzne (Zadanie 8.3)
* **Problem:** Wykorzystanie przestarzałych komponentów w łańcuchu dostaw, w tym biblioteki `org.apache.commons:1.0.0` obarczonej luką podatności RCE.
* **Wpływ:** Najwyższe zagrożenie. Obecność podatności typu *Remote Code Execution* (CVE-2015-7501) stwarza bezpośrednie ryzyko zdalnego przejęcia kontroli nad urządzeniem lub wykonania nieautoryzowanego kodu po stronie klienta.

---

## 📝 3. MAPA DROGOWA NAPRAWCZA (REMEDIATION)

1. **[PRIORYTET 1]** Całkowite zablokowanie flagi debugowania w pliku `AndroidManifest.xml` (zmiana wartości na `false`) na poziomie konfiguracji buildów produkcyjnych w Gradle.
2. **[PRIORYTET 1]** Natychmiastowa aktualizacja paczki `org.apache.commons` oraz pozostałych bibliotek sieciowych do wersji pozbawionych znanych podatności (SCA mitigation).
3. **[PRIORYTET 2]** Usunięcie wszystkich statycznych haseł i poufnych punktów końcowych URL z zasobów tekstowych i przeniesienie ich do bezpiecznego menedżera sekretów lub zmiennych środowiskowych pobieranych dynamicznie.

---

## 🎓 WNIOSKI KOŃCOWE

Aplikacja w obecnym stanie technologicznym wykazuje kaskadowe błędy bezpieczeństwa. Zgodnie z zasadą naczyń połączonych, wyciek sekretów w połączeniu z otwartym portem debugowania i podatnością RCE w bibliotece zewnętrznej daje gotowy wektor ataku dla cyberprzestępców. Kod wymaga natychmiastowego refaktoryzacji przed jakimkolwiek wdrożeniem do sklepu Google Play.