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
    # 1. hpux.txt tartalom ellenőrzése
    body_text = html_soup.body.get_text()
    assert "Hewlett Packard Unix" in body_text

def test_02_nyelv_beallitas(html_soup):
    # 2. Nyelv magyarra állítása
    assert html_soup.html.get("lang") == "hu"

def test_03_title_hpux(html_soup):
    # 3. Böngészőfül címe: HP-UX
    assert html_soup.title.text.strip() == "HP-UX"

def test_04_h1_hpux(html_soup):
    # 4. Egyes szintű fejezetcím: HP-UX
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "HP-UX"

def test_05_bekezdesek_es_vesszo(html_soup):
    # 5. Bekezdések és vesszős tagolás
    ps = html_soup.find_all("p")
    assert len(ps) >= 2
    assert "HP 9000," in ps[1].text and "HP Integral PC" in ps[1].text

def test_06_abbr_hp9000(html_soup):
    # 6. HP 9000 rövidítésként (abbr)
    target = html_soup.find("abbr", string="HP 9000")
    assert target is not None

def test_07_mark_integral(html_soup):
    # 7. HP Integral PC kiemelt (mark)
    target = html_soup.find("mark", string="HP Integral PC")
    assert target is not None

def test_08_h2_tamogatas(html_soup):
    # 8. Kettes szintű fejezetcím: Támogatás
    h2_tags = html_soup.find_all("h2")
    assert len(h2_tags) == 1
    assert h2_tags[0].text.strip() == "Támogatás"

def test_09_komment_adatok(html_soup):
    # 9. Név és dátum a forráskódban
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*\d{4}[-.]\d{2}[-.]\d{2}.*-->", content) is not None

