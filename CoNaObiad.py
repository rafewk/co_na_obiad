import random
from bs4 import BeautifulSoup
import requests
import PySimpleGUI as sg


def find_dish(szukana: str) -> str:
    url = "https://www.przepisy.pl/przepisy/szukaj/" + szukana.strip().lower().replace(" ", "-")
    r = requests.get(url).content
    soup = BeautifulSoup(r, "lxml")
    links = soup.select("a.recipe-box__title")

    if len(links) == 0:
        return "Nie znaleziono"

    else:
        dish_link_endpoint = links[random.randint(0, len(links)-1)].attrs['href']
        dish_link = "https://www.przepisy.pl" + dish_link_endpoint
        return dish_link


def dish_page(dish_link: str):
    r2 = requests.get(dish_link).content
    soup = BeautifulSoup(r2, "lxml")

    nazwa_dania = soup.select_one("div.recipe-desc h1").text.upper()

    ingredients_locator = soup.select("p.ingredient-name span.text-bg-white")
    quantity_locator = soup.select("p.quantity span.text-bg-white")
    steps_locator = soup.select("div.step-info p.step-info-description")

    window["nazwa_dania"].update(nazwa_dania)

    ingredients = []
    quantity = []

    for el in ingredients_locator:
        ingredients.append(el.text.strip())
    for q in quantity_locator:
        quantity.append(q.text)

    ingredients_with_quantity = dict(zip(ingredients, quantity))

    for key, value in ingredients_with_quantity.items():
        window["skladniki"].print("=> " + key.upper() + " :" + value)

    for step in steps_locator:
        window["steps"].print("=> " + step.text + "\n")


font = ("Roboto", "14")
font2 = ("Roboto", "14", "bold")
font3 = ("Roboto", "12", "bold")
font4 = ("Roboto", "10")

layout = [
        [sg.Text("Podaj składniki albo nazwę dania:", font=font)],
        [sg.Input(key="szukana", do_not_clear=False), sg.Button("Szukaj", key="szukaj", size=(15, 1))],
        [sg.HorizontalSeparator()],
        [sg.HorizontalSeparator()],
        [sg.Column([[sg.Text(key="nazwa_dania", font=font2)]], justification="center")],
        [sg.HorizontalSeparator()],
        [sg.HorizontalSeparator()],
        [sg.Text("SKŁADNIKI:", font=font3, size=(48, 1)), sg.Text("SPOSÓB PRZYGOTOWANIA:", font=font3)],
        [sg.MLine(key="skladniki", font=font4, size=(60, 15), do_not_clear=False), sg.VerticalSeparator(), sg.VerticalSeparator(), sg.MLine(key="steps", font=font4, size=(60, 15), do_not_clear=False)]
    ]
window = sg.Window("CO NA OBIAD?", layout)


if __name__ == "__main__":

    while True:
        events, values = window.read()
        if events == sg.WINDOW_CLOSED:
            break

        if events == "szukaj":
            dish = find_dish(values["szukana"])
            if dish == "Nie znaleziono":
                window["nazwa_dania"].update(value="NIE ZNALEZIONO")
                window["skladniki"].update(value="BRAK")
                window["steps"].update(value="BRAK")
            else:
                dish_page(dish)
                window["skladniki"].set_vscroll_position(0.0)
                window["steps"].set_vscroll_position(0.0)
