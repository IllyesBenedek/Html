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
    assert h1 is not None, "HIBA: Hiányzik a h1 elem!"
    assert h1.text.strip() == "HP-UX", "HIBA: A h1 tartalma nem HP-UX!"

def test_04_h2_alcimek(html_soup):
   expected = ["A HP-UX", "Korábbi verziók", "Fájlrendszer"]
   actual = [h2.text.strip() for h2 in html_soup.find_all("h2")]
   assert len(actual) == 3, f"HIBA: 3 cím kellene, de csak {len(actual)} van! Hiányzik: {set(expected) - set(actual)}"
   for h2 in html_soup.find_all("h2"):
       comment = h2.find_previous(string=lambda t: isinstance(t, Comment))
       assert comment is not None and h2.text.strip() == comment.strip(), f"HIBA: A(z) '{h2.text}' nem egyezik az előtte lévő megjegyzéssel!"

def test_05_mark_hewlett_packard(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "A HP-UX" in t)
    assert comment is not None, "HIBA: Nem található a 'A HP-UX' megjegyzés!"
    target_p = comment.find_next("p")
    assert target_p is not None, "HIBA: Nincs bekezdés a megjegyzés után!"
    assert target_p.find("mark", string=re.compile("Hewlett Packard Unix")), \
        "HIBA: A 'Hewlett Packard Unix' szöveg nincs kiemelve taggel!"
    assert target_p.find("abbr", string="HP-UX"), \
        "HIBA: A 'HP-UX' szöveg nincs rövidítésként jelölve!"

def test_06_h2_megjegyzes(html_soup):
    h2_tags = html_soup.find_all("h2")
    for h2 in h2_tags:
        comment = h2.find_previous(string=lambda t: isinstance(t, Comment))
        assert comment is not None, f"HIBA: A(z) '{h2.text.strip()}' cím előtt nincs megjegyzés!"
        assert h2.text.strip() == comment.strip(), \
            f"HIBA: A cím ('{h2.text.strip()}') nem azonos a megjegyzéssel ('{comment.strip()}')!"

def test_07_komment_adatok(html_soup):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*202[0-9].*-->", content), \
            "HIBA: Hiányzik a neved vagy a dátum a HTML forráskódból (kommentként)!"

def test_08_strong_unix_operacios(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "A HP-UX" in t)
    target_p = comment.find_next("p")
    bold_tag = target_p.find(["b", "strong"], string=re.compile("Unix operációs"))
    assert bold_tag is not None, \
        "HIBA: A 'Unix operációs' szöveg nincs félkövérrel (<b> vagy <strong>) jelölve!"

def test_09_em_vxfs(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "Fájlrendszer" in t)
    assert comment is not None, "HIBA: Nem található a 'Fájlrendszer' megjegyzés!"
    target_p = comment.find_next("p")
    assert target_p is not None, "HIBA: Nincs bekezdés a 'Fájlrendszer' cím után!"
    italic_tag = target_p.find(["i", "em"], string=re.compile("VxFS"))
    assert italic_tag is not None, \
        "HIBA: A 'VxFS' szöveg nincs dőlttel jelölve!"
