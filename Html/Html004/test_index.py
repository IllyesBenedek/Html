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
    assert "Hewlett Packard" in html_soup.text

def test_02_nyelv(html_soup):
    assert html_soup.html.get("lang") == "hu"

def test_03_title(html_soup):
    assert html_soup.title.text == "HP-UX"

def test_04_h1(html_soup):
    assert html_soup.find("h1").text == "HP-UX"

def test_05_bekezdesek_szama(html_soup):
    # Két fő bekezdésnek kell lennie a leírás alapján
    assert len(html_soup.find_all("p")) == 2

def test_06_rovidites(html_soup):
    # HP 9000 rövidítésként (abbr)
    abbr = html_soup.find("abbr")
    assert abbr is not None and "HP 9000" in abbr.text

def test_07_kiemeles(html_soup):
    # HP Integral PC kiemelt (strong/b)
    strong = html_soup.find(["strong", "b"])
    assert strong is not None and "HP Integral PC" in strong.text

def test_08_h2_helye_es_szovege(html_soup):
    h2 = html_soup.find("h2")
    assert h2 is not None and h2.text == "Támogatás"
    # Ellenőrizzük, hogy a h2 után jön-e a platformos bekezdés
    next_p = h2.find_next_sibling("p")
    assert "Támogatott platformok" in next_p.text

def test_09_komment(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<!--" in content and "-->" in content
                # Elfogadja a pontost, kötőjeleset, régit és újat is
        assert re.search(r"\d{4}[-.]\d{2}[-.]\d{2}", content) is not None