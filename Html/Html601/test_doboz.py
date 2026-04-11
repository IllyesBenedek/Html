import pytest
from bs4 import BeautifulSoup
import os

def get_html():
    if not os.path.exists("doboz.html"):
        pytest.fail("A doboz.html fájl nem található!")
    with open("doboz.html", 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def hiba(msg, feladat_szam):
    pytest.fail(f"\n[FELADAT 0601-{feladat_szam}. HIBA]: {msg}")

# 1. JAVÍTÁS: HTML/HEAD/META
def test_javitas_01():
    html = get_html()
    if not html.find('html'): hiba("A <html> tag elírása vagy hiánya!", 1)
    if not html.find('head'): hiba("A <head> tag elírása vagy hiánya!", 1)
    meta = html.find('meta')
    if not meta or not meta.has_attr('charset'):
        hiba("A meta charset attribútum hiányzik vagy hibás!", 1)

# 2. JAVÍTÁS: BODY/DIV
def test_javitas_02():
    html = get_html()
    if not html.find('body'): hiba("A <body> tag hiányzik!", 2)
    # Ellenőrizzük, hogy maradt-e "di" a kódban
    with open("doboz.html", 'r', encoding='utf-8') as f:
        if "di>" in f.read():
            hiba("Még maradt 'di' tag a kódban, javítsd 'div'-re!", 2)

# 3. JAVÍTÁS: DOBOZOK SZÁMA
def test_javitas_03():
    html = get_html()
    dobozok = html.find_all('div', class_='doboz')
    if len(dobozok) != 5:
        hiba(f"5 darab 'doboz' osztályú div-et vártam, de {len(dobozok)}-t találtam.", 3)

# 4. JAVÍTÁS: ID-K (d1-d5)
def test_javitas_04():
    html = get_html()
    for i in range(1, 6):
        azonosito = f"d{i}"
        if not html.find('div', id=azonosito):
            hiba(f"A {azonosito} id-val rendelkező doboz hiányzik!", 4)