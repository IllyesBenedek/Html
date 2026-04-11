import pytest
from bs4 import BeautifulSoup
import os

def get_html():
    if not os.path.exists("szoveg.html"):
        pytest.fail("A szoveg.html fájl nem található!")
    with open("szoveg.html", 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def hiba(msg, feladat_szam):
    pytest.fail(f"\n[FELADAT 0602-{feladat_szam}. HIBA]: {msg}")

# 1. JAVÍTÁS: Szintaxis
def test_javitas_01():
    html = get_html()
    if html.find('olo'): hiba("Hibás tag maradt a kódban: <olo> helyett <ol> kell!", 1)
    with open("szoveg.html", 'r', encoding='utf-8') as f:
        content = f.read()
        if "<l>" in content or "</l>" in content:
            hiba("Hibás tag maradt a kódban: <l> helyett <li> kell!", 1)
        if "tat/li>" in content:
            hiba("Hibás lezáró tag maradt: 'tat/li>' helyett 'tat</li>' kell!", 1)

# 2. JAVÍTÁS: Attribútumok
def test_javitas_02():
    html = get_html()
    if html.find(attrs={"clas": True}):
        hiba("Elírt attribútum maradt: 'clas' helyett 'class' kell!", 2)

# 3. JAVÍTÁS: Struktúra
def test_javitas_03():
    html = get_html()
    ol = html.find('ol')
    if not ol: hiba("A beágyazott rendezett lista (<ol>) hiányzik vagy hibás!", 3)
    # Ellenőrizzük, hogy az ol egy li-n belül van-e (beágyazottság)
    if not ol.find_parent('li'):
        hiba("A rendezett listának (<ol>) egy listaelembe (<li>) beágyazva kell lennie!", 3)
