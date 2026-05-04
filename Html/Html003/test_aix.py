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
    assert "kereskedelmi Unix operációs rendszer" in html_soup.get_text(), "HIBA: A szöveg hiányzik vagy hibás ékezet!"

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
    exp = {"Egy", "Kettő", "Három"}
    act = {t.text.strip() for t in html_soup.find_all("h2")}
    hiany = exp - act
    
    msg = f"HIBA: {len(hiany)} hiányzik ({', '.join(hiany)}). Megvan: {len(act)}/3"
    assert not hiany, msg

def test_07_felkovér_szavak(html_soup):
    assert html_soup.find(["strong", "b"], string=re.compile("Advanced Interactive eXecutive")), "HIBA: Az 'Advanced Interactive eXecutive' nem félkövér!"

def test_08_kiemelt_aix(html_soup):
   marks = [m for m in html_soup.find_all("mark") if m.text.strip() == "AIX"]
   assert len(marks) == 3, f"HIBA: 3 db AIX kiemelés kell, de {len(marks)} van!"

def test_09_komment_adatok(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        assert re.search(r"<!--.*[a-zA-Záéíóöőúüű].*\d{4}.*-->", f.read()), "HIBA: Név vagy dátum hiányzik a kommentből!"
