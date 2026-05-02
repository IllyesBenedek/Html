import pytest
from bs4 import BeautifulSoup
import os
import re

@pytest.fixture
def html_soup():
    path = "szoliman.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_01_tartalom(html_soup):
    assert "Szolimán elkomorult" in html_soup.text

def test_02_nyelv(html_soup):
    assert html_soup.html.get("lang") == "hu"

def test_03_title(html_soup):
    assert html_soup.title.text == "Szoliman"

def test_04_h1(html_soup):
    assert html_soup.find("h1").text == "Szoliman"

def test_05_bekezdesek(html_soup):
    assert len(html_soup.find_all("p")) == 3

def test_06_h2_cimek(html_soup):
    expected = ["A szemrehányás", "A szentkönyv", "A leborulás"]
    h2_tags = html_soup.find_all("h2")
    assert len(h2_tags) == 3
    for i, tag in enumerate(h2_tags):
        assert tag.text.strip() == expected[i]

def test_07_dolt_szoveg(html_soup):
    p1 = html_soup.find_all("p")[0]
    italic = p1.find(["i", "em"])
    assert italic is not None and "tekintete azalatt" in italic.text

def test_08_szultan_kiemeles(html_soup):
    p3 = html_soup.find_all("p")[2]
    # Megszámoljuk, hányszor van kiemelve a szultán a 3. bekezdésben
    highlights = p3.find_all(["strong", "b"])
    count = sum(1 for tag in highlights if "A szultán" in tag.text)
    assert count == 2

def test_09_komment(html_soup):
    with open("szoliman.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<!--" in content and "-->" in content
        # Elfogadja a pontost, kötőjeleset, régit és újat is
        assert re.search(r"\d{4}[-.]\d{2}[-.]\d{2}", content) is not None