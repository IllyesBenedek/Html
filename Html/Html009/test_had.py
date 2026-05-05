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

def test_05_tartalom(html_soup):
    assert "indigótelepítvényt" in html_soup.get_text(), "HIBA: A forrásszöveg hiányzik!"

def test_06_h2_p(html_soup):
    h2_szama = len(html_soup.find_all("h2"))
    expected_h2 = ["Telep", "Szomszédok", "Hadcsapat"]
    actual_h2 = [h.text.strip() for h in html_soup.find_all("h2")]    
    assert h2_szama == 3, f"HIBA: 3 db h2 cím kellene, de {h2_szama} van!"
    assert actual_h2 == expected_h2, f"HIBA: A címek szövege nem stimmel! Várt: {expected_h2}, Kapott: {actual_h2}"

def test_07_h1_focim(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None, "HIBA: Hiányzik az h1 fejezetcím!"
    assert h1.text.strip() == "A láthatatlan csillag", "HIBA: A főcím szövege nem 'A láthatatlan csillag.'!"

def test_08_bekezdesek_sorrendje(html_soup):
    for h in html_soup.find_all("h2"):
        kovetkezo = h.find_next_sibling()
        assert kovetkezo is not None and kovetkezo.name == "p", f"HIBA: A(z) '{h.text.strip()}' cím után nem bekezdés (p) van!"

def test_09_megjegyzes(html_content):
     minta = r"[a-zA-Záéíóöőúüű].*\d{4}"
     assert re.search(minta, str(html_soup)), "HIBA: A név vagy a dátum hiányzik vagy nem egyezik!"
