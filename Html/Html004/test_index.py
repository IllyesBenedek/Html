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
    assert "Hewlett Packard Unix" in html_soup.get_text(), "HIBA: A forrásszöveg hiányzik!"

def test_02_nyelv_beallitas(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv nincs magyarra (hu) állítva! (Jelenleg: {lang})"

def test_03_title_hpux(html_soup):
    assert html_soup.title.text.strip() == "HP-UX", "HIBA: A title nem 'HP-UX'!"

def test_04_h1_hpux(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "HP-UX", "HIBA: A h1 nem 'HP-UX'!"

def test_05_bekezdesek_es_vesszo(html_soup):
    ps = html_soup.find_all("p")
    assert len(ps) >= 2, "HIBA: Legalább 2 bekezdésnek kell lennie!"
    assert ps[1].find(string=re.compile("HP 9000,")), "HIBA: Hiányzik a vessző a 'HP 9000' után!"
    
def test_06_abbr_hp9000(html_soup):
    assert html_soup.find("abbr", string=re.compile("HP 9000")), "HIBA: A 'HP 9000' nincs abbr-ben!"

def test_07_mark_integral(html_soup):
    assert html_soup.find("mark", string=re.compile("HP Integral PC")), "HIBA: A 'HP Integral PC' nincs kiemelve!"
    
def test_08_h2_tamogatas(html_soup):
    h2 = html_soup.find("h2")
    assert h2 and h2.text.strip() == "Támogatás", "HIBA: A h2 nem 'Támogatás'!"
    
def test_09_komment_adatok(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        assert re.search(r"<!--.*[a-zA-Záéíóöőúüű].*\d{4}.*-->", f.read()), "HIBA: Név vagy dátum hiányzik!"
