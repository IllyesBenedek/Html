import pytest
from bs4 import BeautifulSoup
import os

@pytest.fixture
def soup():
    path = "index.html"
    if not os.path.exists(path):
        pytest.fail(f"Hiba: Az {path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def test_1_magyar_nyelv(soup):
    """1. Feladat: Állítsa be az oldal nyelvét magyarra."""
    assert soup.html.get("lang") == "hu", "Hiba: A lang='hu' hiányzik a html tag-ből!"

def test_2_cim_a_fulon(soup):
    """2. Feladat: A böngésző fülön a Haarlem felirat jelenjen meg."""
    assert soup.title and soup.title.string == "Haarlem", "Hiba: A <title> nem 'Haarlem'!"

def test_3_elso_cim_h1(soup):
    """3. Feladat: Az első cím (Cornelis van Haarlem) egyes szintű fejezetcím."""
    h1 = soup.find("h1")
    assert h1 and "Cornelis van Haarlem" in h1.string, "Hiba: Hiányzik az <h1> cím!"

def test_4_elso_bekezdes(soup):
    """4. Feladat: Az első címet követő bekezdés HTML bekezdés legyen."""
    h1 = soup.find("h1")
    p1 = h1.find_next_sibling("p")
    assert p1 and "Frans Hals" in p1.text, "Hiba: Hiányzik az első <p> szakasz!"

def test_5_masodik_cim_h2(soup):
    """5. Feladat: A második cím (Életpályája) kettes szintű fejezetcím."""
    h2_cimek = soup.find_all("h2")
    assert len(h2_cimek) >= 1 and "Életpályája" in h2_cimek[0].text, "Hiba: Hiányzik az <h2>Életpályája</h2>!"

def test_6_masodik_bekezdes(soup):
    """6. Feladat: A második cím utáni bekezdés HTML bekezdés legyen."""
    h2_1 = soup.find("h2", string=lambda x: x and "Életpályája" in x)
    p2 = h2_1.find_next_sibling("p")
    assert p2 and "Antwerpenben tanult" in p2.text, "Hiba: Hiányzik a második <p> szakasz!"

def test_7_harmadik_cim_h2(soup):
    """7. Feladat: A harmadik cím (Forrás) kettes szintű fejezetcím."""
    h2_cimek = soup.find_all("h2")
    assert len(h2_cimek) >= 2 and "Forrás" in h2_cimek[1].text, "Hiba: Hiányzik az <h2>Forrás</h2>!"

def test_8_url_bekezdes(soup):
    """8. Feladat: Az URL is bekezdésnek (p) legyen jelölve."""
    p_tags = soup.find_all("p")
    assert any("wikipedia" in p.text for p in p_tags), "Hiba: Az URL nincs <p> tag-ben!"

def test_9_div_beagyazas(soup):
    """9. Feladat: Az egész weblapot tegye egy div elembe."""
    # A body-ban csak egyetlen div lehet, ami mindent tartalmaz
    children = [c for c in soup.body.children if c.name is not None]
    assert len(children) == 1 and children[0].name == "div", "Hiba: Mindennek egy <div>-en belül kell lennie!"