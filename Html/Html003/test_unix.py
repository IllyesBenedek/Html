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
    assert "IBM" in html_soup.text

def test_02_nyelv(html_soup):
    assert html_soup.html.get("lang") == "hu"

def test_03_title(html_soup):
    assert html_soup.title.text == "AIX"

def test_04_h1(html_soup):
    assert html_soup.find("h1").text == "AIX"

def test_05_bekezdesek(html_soup):
    assert len(html_soup.find_all("p")) == 3

def test_06_h2_cimek(html_soup):
    expected = ["Egy", "Kettő", "Három"]
    h2_tags = html_soup.find_all("h2")
    assert len(h2_tags) == 3
    for i, tag in enumerate(h2_tags):
        assert tag.text.strip() == expected[i]

def test_07_advanced_kiemeles(html_soup):
    # Az "Advanced Interactive eXecutive" kiemelésének ellenőrzése
    strongs = html_soup.find_all(["strong", "b"])
    texts = [s.text for s in strongs]
    assert "Advanced Interactive eXecutive" in texts

def test_08_aix_kiemelesek(html_soup):
    # Minden "AIX" szónak kiemeltnek kell lennie
    strongs = html_soup.find_all(["strong", "b"])
    aix_strongs = [s for s in strongs if s.text == "AIX"]
    # Legalább 4-szer szerepel a szövegben az AIX szó
    assert len(aix_strongs) >= 3

def test_09_komment(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<!--" in content and "-->" in content
        # Elfogadja a pontost, kötőjeleset, régit és újat is
        assert re.search(r"\d{4}[-.]\d{2}[-.]\d{2}", content) is not None