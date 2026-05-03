import pytest
from bs4 import BeautifulSoup, Comment
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
    # 1. A szöveg tartalmának ellenőrzése a törzsben
    body_text = html_soup.body.get_text()
    assert "tisztes matrónának" in html_soup.text

def test_02_nyelv(html_soup):
    # 2. Nyelv beállítása magyarra (hu)
    assert html_soup.html.get("lang") == "hu"

def test_03_title(html_soup):
    # 3. Böngészőfül címe: Két fűzfa
    assert html_soup.title.text == "Két fűzfa"

def test_04_h1(html_soup):
    # 4. Egyes szintű fejezetcím (h1): Két fűzfa
    h1 = html_soup.find("h1")
    assert html_soup.find("h1").text == "Két fűzfa"

def test_05_bekezdesek(html_soup):
    # 5. Három bekezdés (p) meglétének ellenőrzése
    assert len(html_soup.find_all("p")) == 3

def test_06_h2_cimek(html_soup):
    # 6. Kettes szintű fejezetcímek (h2) szövegének ellenőrzése
    expected = {"A jövedelem", "A kollégium", "Az orákulum"}
    actual = {tag.text.strip() for tag in html_soup.find_all("h2")}
    hianyzo = expected - actual
    assert not hianyzo, f"Hiba! Ez hiányzik: {', '.join(hianyzo)}"
    assert len(actual) == 3, f"Hiba: {len(actual)} alcím van a 3 helyett!"


def test_07_kiemelt_szoveg(html_soup):
    # 7. "bevette magát" kiemelt (strong) a harmadik bekezdésben
    p3 = html_soup.find_all("p")[2]
    strong = p3.find(["strong", "b"])
    assert strong is not None and strong.text == "bevette magát"

def test_08_dolt_szoveg(html_soup):
    # 8. "időszerint" dőlt (i vagy em) a második bekezdésben
    p2 = html_soup.find_all("p")[1]
    italic = p2.find(["i", "em"])
    assert italic is not None and italic.text == "időszerint"

def test_09_komment(html_soup):
    # 8. "időszerint" dőlt (i vagy em) a második bekezdésben
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<!--" in content and "-->" in content
        # Dátum formátum keresése a kommentben: YYYY.MM.DD vagy YYYY-MM-DD
        assert re.search(r"\d{4}[-.]\d{2}[-.]\d{2}", content) is not None