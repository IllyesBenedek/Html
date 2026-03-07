import pytest
from bs4 import BeautifulSoup
import os

@pytest.fixture
def soup():
    fajl_nev = "index.html"
    assert os.path.exists(fajl_nev), "A fájl nem található!"
    with open(fajl_nev, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def test_1_nyelv(soup):
    assert soup.html.get("lang") == "hu", "Hiba: Az oldal nyelve nem magyar (hu)."

def test_2_cim(soup):
    assert soup.title.string == "Csengő", "Hiba: A böngészőfül címe nem 'Csengő'."

def test_3_header_kep(soup):
    img = soup.find("header").find("img")
    assert img is not None, "Hiba: A headerben nem található kép."
    # Módosítottuk az elvárt értéket:
    assert img.get("src") == "images/csengo.png", "Hiba: A header képe nem images/csengo.png."

def test_4_header_alt(soup):
    img = soup.find("header").find("img")
    assert img.get("alt") == "Csengő", "Hiba: A header kép alt szövege nem 'Csengő'."

def test_5_h1_cim(soup):
    assert soup.h1.string == "Csengő iroda", "Hiba: A főcím nem 'Csengő iroda'."

def test_6_masodik_bekezdes_kep(soup):
    p_tags = soup.find_all("p")
    img = p_tags[1].find("img")
    assert img is not None, "Hiba: A 2. bekezdésben nem található a halozat.png kép."
    assert "halozat.png" in img.get("src"), f"Hiba: A 2. bekezdés képe nem halozat.png, hanem: {img.get('src')}"

def test_7_halozat_alt(soup):
    p_tags = soup.find_all("p")
    img = p_tags[1].find("img")
    assert img.get("alt") == "Hálózat", "Hiba: A hálózat kép alt szövege nem 'Hálózat'."

def test_8_felkover_cim(soup):
    p_tags = soup.find_all("p")
    assert p_tags[2].find("b") is not None, "Hiba: A 3. bekezdésben nincs félkövér (b) jelölés."

def test_9_lista(soup):
    assert soup.find("ul") is not None, "Hiba: A végponti eszközök listája nem számozatlan lista (ul)."