import pytest
from bs4 import BeautifulSoup
import os

# Segédfüggvény a fájl beolvasásához
def get_soup():
    # 1. Ellenőrzés: Létezik-e a fájl
    assert os.path.exists("index.html"), "Az index.html fájl nem található!"
    with open("index.html", "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def get_raw_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

def test_1_html_lang():
    # Magyar nyelv beállítása
    soup = get_soup()
    assert soup.html.get("lang") == "hu", "A HTML oldal nyelve nem magyar (lang='hu')!"

def test_2_utf8():
    # UTF-8 kódolás
    soup = get_soup()
    meta = soup.find("meta", charset=True)
    assert meta and meta.get("charset").lower() == "utf-8", "Az oldal kódolása nem utf-8!"

def test_3_browser_title():
    # Böngésző fül szövege: Verseny
    soup = get_soup()
    assert soup.title and soup.title.string == "Verseny", "A böngésző fülön megjelenő szöveg nem 'Verseny'!"

def test_4_table_exists():
    # Táblázat megléte
    soup = get_soup()
    assert soup.find("table") is not None, "A táblázat hiányzik az oldalról!"

def test_5_colspan():
    # Oszlopnyúlás ellenőrzése
    soup = get_soup()
    th = soup.find("th")
    assert th and th.get("colspan") == "3", "A táblázatban nincs beállítva a megfelelő oszlopnyúlás (colspan='3')!"

def test_6_rowspan():
    # Sornyúlás ellenőrzése
    soup = get_soup()
    td = soup.find("td")
    assert td and td.get("rowspan") == "7", "A táblázatban nincs beállítva a megfelelő sornyúlás (rowspan='7')!"

def test_7_h1_header():
    # H1 címsor: Verseny
    soup = get_soup()
    h1 = soup.find("h1")
    assert h1 and h1.string == "Verseny", "A táblázat előtt nincs egyes szintű címsor 'Verseny' szöveggel!"

def test_8_footer_with_data():
    # Lábléc: név, dátum
    soup = get_soup()
    footer = soup.find("footer") # vagy div, ha általános blokk elem
    assert footer is not None, "A weblap alján hiányzik a lábléc (blokk elem)!"
    text = footer.get_text()

def test_9_comment_metadata():
    # Megjegyzés a fájl tetején: név és dátum + 152. feladat
    raw = get_raw_html()
    assert "" in raw, "Hiányzik a HTML megjegyzés a fájl tetejéről!"