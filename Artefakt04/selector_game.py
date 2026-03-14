import json

def generate_xpath(element_id, element_tag):
    xpath_query = f"//{element_tag}[@android:id='{element_id}']"
    return xpath_query


def main():

    try:
        with open("miner_report.json", "r", encoding="utf-8") as f:
            data = json.load(f)

    except FileNotFoundError:
        print("Plik miner_report.json nie został znaleziony!")
        return

    element_id = input("Wpisz dokładnie ID: ")
    element_tag = input("Wpisz dokładnie tag: ")

    xpath = generate_xpath(element_id, element_tag)

    matches = 0

    for item in data:
        if item.get("id") == element_id and item.get("tag") == element_tag:
            print(f"Znaleziono: {item}")
            matches += 1

    if matches == 1:
        result = "STATUS: ZALICZONE! Twój selektor jest unikalny."
    else:
        result = f"STATUS: BŁĄD! Znalazłem {matches} dopasowań."

    print(result)

    # zapis wyniku do pliku dla zadania 4.5
    with open("xpath_verification.txt", "w", encoding="utf-8") as f:
        f.write(result + "\n")
        f.write(f"XPath: {xpath}\n")
        f.write(f"Matches: {matches}\n")

    print("Wynik zapisany do xpath_verification.txt")


if __name__ == "__main__":
    main()