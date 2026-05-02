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
    assert "tisztes matrónának" in html_soup.text

def test_02_nyelv(html_soup):
    assert html_soup.html.get("lang") == "hu"

def test_03_title(html_soup):
    assert html_soup.title.text == "Két fűzfa"

def test_04_h1(html_soup):
    assert html_soup.find("h1").text == "Két fűzfa"

def test_05_bekezdesek(html_soup):
    assert len(html_soup.find_all("p")) == 3

def test_06_h2_cimek(html_soup):
    expected = ["A jövedelem", "A kollégium", "Az orákulum"]
    h2_tags = html_soup.find_all("h2")
    for i, tag in enumerate(h2_tags):
        assert tag.text.strip() == expected[i]

def test_07_kiemelt_szoveg(html_soup):
    p3 = html_soup.find_all("p")[2]
    strong = p3.find(["strong", "b"])
    assert strong is not None and strong.text == "bevette magát"

def test_08_dolt_szoveg(html_soup):
    p2 = html_soup.find_all("p")[1]
    italic = p2.find(["i", "em"])
    assert italic is not None and italic.text == "időszerint"

def test_09_komment(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<!--" in content and "-->" in content
        assert "Illyés Benedek" in content
                # Elfogadja a pontost, kötőjeleset, régit és újat is
        assert re.search(r"\d{4}[-.]\d{2}[-.]\d{2}", content) is not None