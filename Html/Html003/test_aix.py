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
    body_text = html_soup.body.get_text()
    assert "kereskedelmi Unix operációs rendszer" in body_text, "HIBA: Az aix.txt tartalma nincs (megfelelően) beillesztve!"

def test_02_nyelv_beallitas(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv nincs magyarra (hu) állítva! Jelenleg: {lang}"

def test_03_title_aix(html_soup):
    assert html_soup.title.text.strip() == "AIX", "HIBA: A böngészőfül címe (title) nem 'AIX'!"

def test_04_h1_aix(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None, "HIBA: Hiányzik a h1 elem!"
    assert h1.text.strip() == "AIX", "HIBA: A h1 tartalma nem 'AIX'!"

def test_05_bekezdesek_szama(html_soup):
    ps = html_soup.find_all("p")
    assert len(ps) == 3, f"HIBA: Pontosan 3 bekezdés (p) kell, de {len(ps)} van!"

def test_06_h2_alcimek(html_soup):
    expected = {"Egy", "Kettő", "Három"}
    actual = {tag.text.strip() for tag in html_soup.find_all("h2")}
    hianyzo = expected - actual
    assert not hianyzo, f"Hiba! Ez hiányzik: {', '.join(hianyzo)}"
    assert len(actual) == 3, f"Hiba: {len(actual)} alcím van a 3 helyett!"

def test_07_felkovér_szavak(html_soup):
    target = html_soup.find(lambda tag: tag.name in ["strong", "b"] and "Advanced Interactive eXecutive" in tag.text)
    assert target is not None, "HIBA: Az 'Advanced Interactive eXecutive' nincs félkövérrel jelölve!"

def test_08_kiemelt_aix(html_soup):
    marks = [m for m in html_soup.find_all("mark") if m.text.strip() == "AIX"]
    mark_szama = len(marks)
    assert mark_szama == 3, f"HIBA: Pontosan 3 db AIX kiemelés kell, de {mark_szama} található!"

def test_09_komment_adatok(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        minta = r"<!--.*[a-zA-Záéíóöőúüű].*\d{4}[-.]\d{2}[-.]\d{2}.*-->"
        assert re.search(minta, content) is not None, "HIBA: Hiányzik a név vagy a dátum a kommentből!"
