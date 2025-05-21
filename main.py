import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.ss.lv/lv/transport/cars/jaguar/",
}

url = "https://www.ss.lv/lv/transport/cars/"
base_url = "https://www.ss.lv"
manufacturers = []
filters = {
    "Ražotājs": None,
    "Minimālā cena": None,
    "Maksimālā cena": None,
    "Minimālais gads": None,
    "Maksimālais gads": None,
}


def run_program():
    global filters
    list_filters()
    print("Lūdzu, izvēlieties darbību:")
    print("[1] Izvēlēties ražotāju (obligāti, ja nav izvēlēts)")
    print("[2] Izvēlēties minimālo cenu")
    print("[3] Izvēlēties maksimālo cenu")
    print("[4] Izvēlēties minimālo gadu")
    print("[5] Izvēlēties maksimālo gadu")
    print("[6] Notīrīt visus filtrus")
    if any(v is not None for v in filters.values()):
        print("[7] Izvilkt neskatītus sludinājumus pēc pašreizējiem filtriem")
    print("[0] Iziet\n")

    choice = input("Jūsu izvēle: ")
    if choice == "1":
        request_manufacturers_data()
    elif choice == "2":
        request_min_price()
    elif choice == "3":
        request_max_price()
    elif choice == "4":
        request_min_year()
    elif choice == "5":
        request_max_year()
    elif choice == "6":
        clear_filters()
    elif choice == "7":
        if filters["Ražotājs"] is None:
            print("Lūdzu, izvēlieties ražotāju pirms izvilkšanas.")
            run_program()
        else:
            extract_unseen_ads()
    elif choice == "0":
        print("Iziet no programmas.")
    else:
        print("Nederīga izvēle.")
        run_program()


def request_min_price():
    global filters
    min_price = input("Lūdzu, ievadiet minimālo cenu: ").strip()
    if min_price.isdigit() and int(min_price) > 0:
        filters["Minimālā cena"] = min_price
        run_program()
    else:
        print("Nederīga cena (nepieciešams skaitlis, lielāks par 0).")
        request_min_price()


def request_max_price():
    global filters
    max_price = input("Lūdzu, ievadiet maksimālo cenu: ").strip()
    if (
        max_price.isdigit()
        and int(max_price) > 0
        and int(max_price) >= int(filters["Minimālā cena"])
    ):
        filters["Maksimālā cena"] = max_price
        run_program()
    else:
        print(
            "Nederīga cena (nepieciešams skaitlis, lielāks par 0 un lielāks par minimālo cenu)."
        )
        request_max_price()


def request_min_year():
    global filters
    min_year = input("Lūdzu, ievadiet minimālo gadu: ").strip()
    if min_year.isdigit() and int(min_year) > 0:
        filters["Minimālais gads"] = min_year
        run_program()
    else:
        print("Nederīgs gads (nepieciešams skaitlis, lielāks par 0).")
        request_min_year()


def request_max_year():
    global filters
    max_year = input("Lūdzu, ievadiet maksimālo gadu: ").strip()
    if (
        max_year.isdigit()
        and int(max_year) > 0
        and int(max_year) >= int(filters["Minimālais gads"])
    ):
        filters["Maksimālais gads"] = max_year
        run_program()
    else:
        print(
            "Nederīgs gads (nepieciešams skaitlis, lielāks par 0 un lielāks par minimālo gadu)."
        )
        request_max_year()


def clear_filters():
    global filters
    filters = {
        "Ražotājs": None,
        "Minimālā cena": None,
        "Maksimālā cena": None,
        "Minimālais gads": None,
        "Maksimālais gads": None,
    }
    print("Visi filtri ir notīrīti.")
    run_program()


def extract_unseen_ads():
    global filters, headers
    mfg_elem = filters["Ražotājs"]
    mfg_name = mfg_elem.text.strip() if hasattr(mfg_elem, "text") else str(mfg_elem)
    seen_file = f"{mfg_name}.txt"
    seen = set()
    if os.path.exists(seen_file):
        with open(seen_file, "r", encoding="utf-8") as f:
            for line in f:
                seen.add(line.split(" | ")[-1].strip())

    print("========================================")
    print("Neskatītie sludinājumi:")
    print("========================================\n")
    adrese = base_url + filters["Ražotājs"]["href"]
    url = adrese + "filter/"
    params = {
        "topt[8][min]": filters["Minimālā cena"],
        "topt[8][max]": filters["Maksimālā cena"],
        "topt[18][min]": filters["Minimālais gads"],
        "topt[18][max]": filters["Maksimālais gads"],
    }
    # remove unset filters
    params = {k: v for k, v in params.items() if v is not None}

    session.post(url, data=params, headers=headers)
    page_number = 1
    while True:
        if page_number == 1:
            page_url = url
        else:
            page_url = f"{url}page{page_number}.html"

        resp = session.get(page_url, headers=headers)
        if resp.status_code != 200:
            print(
                f"Failed to fetch page {page_number}. Status code: {resp.status_code}"
            )
            break

        lapas_saturs = BeautifulSoup(resp.content, "html.parser")
        tr_elements = lapas_saturs.find_all("tr", id=re.compile(r"^tr_"))
        if not tr_elements:
            break

        for tr in tr_elements:
            td_elements = tr.find_all("td")[2:]  # skipping checkbox and image
            td_texts = []
            index = 0
            first_a_tag = None
            for td in td_elements:
                a_tag = td.find("a")
                if a_tag:
                    lines = [
                        line.strip()
                        for line in a_tag.get_text().splitlines()
                        if line.strip()
                    ]
                    if lines:
                        first_line = lines[0]
                        if index == 0:
                            first_a_tag = a_tag
                            td_texts.append(first_line + "...")
                        else:
                            td_texts.append(first_line)
                    else:
                        td_texts.append("")
                    index += 1
                else:
                    td_texts.append(td.get_text(strip=True))

                index += 1
            if first_a_tag:
                full_url = base_url + first_a_tag["href"]
            else:
                continue
            if full_url in seen:
                continue
            td_texts.append(full_url)
            line = " | ".join(td_texts)

            print(line)
            print()

            timestamp = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
            entry = f"{timestamp} | {line}"
            with open(seen_file, "a", encoding="utf-8") as f:
                f.write(entry + "\n")

            seen.add(full_url)

        page_number += 1
    run_program()


def list_filters():
    print("========================================")
    if any(v is not None for v in filters.values()):
        print("Pašreizējie filtri:\n")
        for key, value in filters.items():
            if value is not None:
                print(
                    f"{key}: {value.text.strip() if hasattr(value, 'text') else value}"
                )
    else:
        print("Nav izvēlēts neviens filtrs.")
    print("========================================\n")


def request_manufacturers_data():
    global manufacturers
    lapa = requests.get(url)

    if lapa.status_code == 200:
        lapas_saturs = BeautifulSoup(lapa.content, "html.parser")
        # select 2nd top-level table on the page
        body = lapas_saturs.body
        lvl0_table = body.find("table")
        lvl1_table = lvl0_table.find("table")
        lvl2_tables = lvl1_table.find_all("table")
        second = lvl2_tables[2]

        third = second.find("table") if second else None
        target = third

        if target:
            manufacturers = target.find_all(class_="a_category")
            request_manufacturers_choice()
        else:
            print("Netika atrasta neviens auto ražotājs.")


def request_manufacturers_choice():
    global filters
    print("Lūdzu, izvēlieties ražotāju, ievadot atbilstošo ciparu:")
    index = 1
    for manufacturer in manufacturers:
        print(f"[{index}] {manufacturer.text.strip()}")
        index += 1

    choice = input("Jūsu izvēle: ")
    if choice.isdigit() and 1 <= int(choice) <= len(manufacturers):
        filters["Ražotājs"] = manufacturers[int(choice) - 1]
        run_program()
    else:
        print("Nederīga izvēle.")
        request_manufacturers_choice()


if __name__ == "__main__":
    print("========================================")
    print("SS.LV neskatītu sludinājumu izvilkšana")
    print("========================================\n")
    run_program()
