import pytest
from bs4 import BeautifulSoup
import os
import re

@pytest.fixture
def html_soup():
    path = "index.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_01_tartalom(html_soup):
    assert "tisztes matrónának" in html_soup.get_text(), "HIBA: A szöveg hiányzik vagy hibás kódolás!"

def test_02_nyelv(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv '{lang}' a 'hu' helyett!"

def test_03_title(html_soup):
    assert html_soup.title.text.strip() == "Két fűzfa", "HIBA: A böngészőfül címe nem 'Két fűzfa'!"

def test_04_h1(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None, "HIBA: Nincs h1 fejezetcím!"
    assert h1.text.strip() == "Két fűzfa", "HIBA: A h1 tartalma nem 'Két fűzfa'!"

def test_05_bekezdesek(html_soup):
    ps = html_soup.find_all("p")
    assert len(ps) == 3, f"HIBA: 3 bekezdés kell, de {len(ps)} van!"

def test_06_h2_cimek(html_soup):
    exp, act = {"A jövedelem", "A kollégium", "Az orákulum"}, {t.text.strip() for t in html_soup.find_all("h2")}
    hiany = exp - act
    assert not hiany, f"HIBA: Hiányzó alcímek: {', '.join(hiany)}"
    assert len(act) == 3, f"HIBA: 3 helyett {len(act)} alcím van!"

def test_07_kiemelt_szoveg(html_soup):
    p3 = html_soup.find_all("p")[2]
    assert p3.find(["strong", "b"], string=re.compile("bevette magát")), "HIBA: A 'bevette magát' nincs kiemelve a 3. bekezdésben!"

def test_08_dolt_szoveg(html_soup):
    p2 = html_soup.find_all("p")[1]
    assert p2.find(["i", "em"], string=re.compile("időszerint")), "HIBA: Az 'időszerint' nincs dőlttel jelölve!"

def test_09_komment(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        assert re.search(r"<!--.*[a-zA-Záéíóöőúüű].*\d{4}.*-->", f.read()), "HIBA: Név vagy dátum hiányzik a kommentből!"
