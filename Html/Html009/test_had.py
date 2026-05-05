import pytest
from bs4 import BeautifulSoup, Comment
import re
import os

@pytest.fixture
def html_soup():
    path = "had.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_01_had_html_fajl_letezik_e():
    assert os.path.exists("had.html"), "HIBA: A 'had.html' fájl nem létezik!"

def test_02_nyelv_magyar(html_soup):
    assert html_soup.html.get("lang") == "hu", "HIBA: A nyelv nem magyar!"

def test_03_karakter_kodolas(html_soup):
    assert html_soup.find("meta", charset = re.compile(r"utf-8", re.I)), "HIBA: Nincs utf-8 kódolás!"

def test_04_tittle_had(html_soup):
     assert html_soup.title.text.strip() == "Had", "HIBA: A böngészőfül címe nem 'Had'!"
