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

def test_01_nyelv_magyar(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv nincs magyarra (hu) állítva! (Jelenleg: {lang})"

def test_02_title_hpux(html_soup):
    assert html_soup.title.text.strip() == "HP-UX", "HIBA: A title nem ' HP-UX'!"
    
def test_03_h1_hpux(html_soup):
    h1 = html_soup.find("h1")
    assert h1 and h1.text.strip() == "HP-UX", "HIBA: A h1 tartalma nem HP-UX!"

def test_04_h2_alcimek(html_soup):
    expected, actual = ["A HP-UX", "Korábbi verziók", "Fájlrendszer"], [h.text.strip() for h in html_soup.find_all("h2")]
    assert len(actual) == 3, f"HIBA: 3 cím kellene, de csak {len(actual)} van! Hiányzik: {set(expected) - set(actual)}"
    for h in html_soup.find_all("h2"):
        c = h.find_previous(string=lambda t: isinstance(t, Comment))
        assert c is not None, f"HIBA: A(z) '{h.text.strip()}' cím előtt nincs megjegyzés!"
        assert h.text.strip() == c.strip(), f"HIBA: A(z) '{h.text.strip()}' nem egyezik az előtte lévő megjegyzéssel!"

def test_05_mark_hewlett_packard(html_soup):
    c = html_soup.find(string=lambda t: isinstance(t, Comment) and "A HP-UX" in t)
    p = c.find_next("p")
    assert p.find("mark", string=re.compile("Hewlett Packard Unix")), "HIBA: A 'Hewlett Packard Unix' nincs kiemelve!"
    assert p.find("abbr", string="HP-UX"), "HIBA: A 'HP-UX' nincs rövidítésként jelölve!"

def test_06_h2_megjegyzes(html_soup):
    for h in html_soup.find_all("h2"):
        c = h.find_previous(string=lambda t: isinstance(t, Comment))
        assert c is not None, f"HIBA: A(z) '{h.text.strip()}' cím előtt nincs megjegyzés!"
        assert h.text.strip() == c.strip(), f"HIBA: A(z) '{h.text.strip()}' nem egyezik az előtte lévő megjegyzéssel!"

def test_07_komment_adatok(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*202[0-9].*-->", content), "HIBA: Hiányzik a neved vagy a dátum!"

def test_08_strong_unix_operacios(html_soup):
    p = html_soup.find(string=lambda t: isinstance(t, Comment) and "A HP-UX" in t).find_next("p")
    assert p.find(["b", "strong"], string=re.compile("Unix operációs")), "HIBA: A 'Unix operációs' nincs félkövérrel jelölve!"

def test_09_em_vxfs(html_soup):
    p = html_soup.find(string=lambda t: isinstance(t, Comment) and "Fájlrendszer" in t).find_next("p")
    assert p.find(["i", "em"], string=re.compile("VxFS")), "HIBA: A 'VxFS' nincs dőlttel jelölve!"
