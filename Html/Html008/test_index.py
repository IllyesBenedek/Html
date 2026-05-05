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
    assert "viszálykodás a kalászvágás"  in html_soup.get_text(), "HIBA: A forrásszöveg hiányzik az oldalról!"

def test_02_nyelv_magyar(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv nincs magyarra (hu) állítva! (Jelenleg: {lang})"

def test_03_karakter_kodolas(html_soup):
    meta = html_soup.find("meta", charset=re.compile(r"utf-8", re.I))
    assert meta is not None, "Hiba: Hiányzik az UTF-8 kódolás beállítása!"

def test_04_title_Ősz(html_soup):
    assert html_soup.title.text.strip() == "Ősz", "Hiba: A <title> nem 'Ősz'!"

def test_05_h1_Ősz(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "Ősz", "Hiba: Nincs <h1> 'Ősz' tartalommal!"
    
def test_06_h2_megjegyzes(html_soup):
    h2s = html_soup.find_all("h2")
    exp, act = {"Gyümölcsszedés", "Érés", "Szőlőszedés"}, {h.text.strip() for h in h2s}
    hiany = exp - act
    
    assert not hiany, f"HIBA: {len(hiany)} hiányzik: {hiany}. Megvan: {len(act)}/3"
    assert len(h2s) == 3, f"HIBA: Pontosan 3 db h2 kell, de {len(h2s)} van!"
    
    for h in h2s:
        c = h.find_next_sibling(string=lambda t: isinstance(t, Comment))
        assert c and h.text.strip() == c.strip(), f"HIBA: Nincs megfelelő komment a(z) '{h.text.strip()}' h2 UTÁN!"

def test_07_kalászvágás_dölt(html_soup):
    p = html_soup.find(string=lambda t: isinstance(t, Comment) and "Gyümölcsszedés" in t).find_next("p")
    assert p.find(["i", "em"], string="kalászvágás"), "HIBA: Csak a 'kalászvágás' szó dőlt a bekezdésben!"
    
def   test_08_gyümölcsérés_ideje_kiemelt(html_soup):
    p = html_soup.find(string=lambda t: isinstance(t, Comment) and "Érés" in t).find_next("p")
    assert p.find("mark", string="gyümölcsérés ideje"), "HIBA: A 'gyümölcsérés ideje' nincs mark-kal kiemelve az Érésnél!"

def test_09_szoloszedes_erősen_megjelölt(html_soup):
    p = html_soup.find(string=lambda t: isinstance(t, Comment) and "Szőlőszedés" in t).find_next("p")
    assert p.find("strong", string="hagyják kiforrni"), "HIBA: A 'hagyják kiforrni' nincs strong-gal jelölve a Szőlőszedésnél!"
