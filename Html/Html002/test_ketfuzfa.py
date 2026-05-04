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
    body_text = html_soup.body.get_text()
    assert "tisztes matrónának" in html_soup.text, "HIBA: A szöveg nincs beillesztve vagy hibás kódolás!"

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
    expected = {"A jövedelem", "A kollégium", "Az orákulum"}
    actual = {tag.text.strip() for tag in html_soup.find_all("h2")}
    hianyzo = expected - actual
    assert not hianyzo, f"HIBA: Hiányzó alcímek: {', '.join(hianyzo)}"

def test_07_kiemelt_szoveg(html_soup):
    p3 = html_soup.find_all("p")[2]
    target = p3.find(lambda tag: tag.name in ["strong", "b"] and "bevette magát" in tag.text)
    assert target is not None, "HIBA: A 'bevette magát' nincs kiemelve a 3. bekezdésben!"

def test_08_dolt_szoveg(html_soup):
    # 8. "időszerint" dőlt (i vagy em) a második bekezdésben
    p2 = html_soup.find_all("p")[1]
    italic = p2.find(lambda tag: tag.name in ["i", "em"] and "időszerint" in tag.text)
    assert italic is not None, "HIBA: Az 'időszerint' nincs dőlttel jelölve a 2. bekezdésben!"

def test_09_komment(html_soup):
    # 8. "időszerint" dőlt (i vagy em) a második bekezdésben
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        minta = r"<!--.*[a-zA-Záéíóöőúüű].*\d{4}[-.]\d{2}[-.]\d{2}.*-->"
        assert re.search(minta, content) is not None, "HIBA: A kommentből hiányzik a név vagy a dátum!"
