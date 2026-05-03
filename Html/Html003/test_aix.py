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

def test_01_tartalom_beillesztes(html_soup):
    # 1. aix.txt tartalmának ellenőrzése
    body_text = html_soup.body.get_text()
    assert "operációs rendszer" in body_text

def test_02_nyelv_beallitas(html_soup):
    # 2. Nyelv magyarra (hu) állítása
    assert html_soup.html.get("lang") == "hu"

def test_03_title_aix(html_soup):
    # 3. Böngészőfül címe: AIX
    assert html_soup.title.text.strip() == "AIX"

def test_04_h1_aix(html_soup):
    # 4. Egyes szintű fejezetcím: AIX
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "AIX"

def test_05_bekezdesek_szama(html_soup):
    # 5. Három bekezdés (<p>) megléte
    ps = html_soup.find_all("p")
    assert len(ps) == 3

def test_06_h2_alcimek(html_soup):
    # 6. Kettes szintű fejezetcímek ellenőrzése
    expected = ["Egy", "Kettő", "Három"]
    h2_tags = html_soup.find_all("h2")
    assert len(h2_tags) == 3 
    for i, tag in enumerate(h2_tags):
        assert tag.text.strip() == expected[i]

def test_07_felkovér_szavak(html_soup):
    # 7. Advanced Interactive eXecutive félkövér (strong)
    target = html_soup.find("strong", string=re.compile("Advanced Interactive eXecutive"))
    assert target is not None

def test_08_kiemelt_aix(html_soup):
    # 8. AIX szó kiemelve (mark)
    marks = html_soup.find_all("mark", string="AIX")
    assert len(marks) >= 2

def test_09_komment_adatok(html_soup):
    # 9. Név és dátum megjegyzésben
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*\d{4}[-.]\d{2}[-.]\d{2}.*-->", content) is not None

