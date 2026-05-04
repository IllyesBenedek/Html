import pytest
from bs4 import BeautifulSoup
import os
import re

@pytest.fixture
def html_soup():
    path = "szoliman.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_01_tartalom_beillesztes(html_soup):
    assert "Szolimán elkomorult" in html_soup.body.get_text(), "HIBA: A szöveg hiányzik vagy hibás ékezet!"

def test_02_nyelv_beallitas(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv nincs magyarra (hu) állítva! (Jelenleg: {lang})"

def test_03_title_szoliman(html_soup):
    assert html_soup.title.text.strip() == "Szoliman", "HIBA: A title nem 'Szoliman'!"

def test_04_h1_szoliman(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None, "HIBA: Nincs h1 cím!"
    assert h1.text.strip() == "Szoliman", "HIBA: A h1 nem 'Szoliman'!"

def test_05_bekezdesek_szama(html_soup):
    ps = html_soup.find_all("p")
    assert len(ps) == 3, f"HIBA: Pontosan 3 bekezdés kell, de {len(ps)} van!"

def test_06_h2_alcimek(html_soup):
    expected = ["A szemrehányás", "A szentkönyv", "A leborulás"]
    actual = [h.text.strip() for h in html_soup.find_all("h2")]
    hianyzo = [item for item in expected if item not in actual]
    assert len(actual) == 3, f"HIBA: 3 cím kellene, de csak {len(actual)} van! Hiányzik: {hianyzo}"
    
def test_07_dolt_tekintete(html_soup):
    p1 = html_soup.find_all("p")[0]
    assert p1.find(["i", "em"], string=re.compile("tekintete azalatt")), "HIBA: A 'tekintete azalatt' nem dőlt!"
    
def test_08_strong_szultan(html_soup):
    p3 = html_soup.find_all("p")[2]
    targets = [t for t in p3.find_all(["strong", "b"]) if "A szultán" in t.text]
    assert len(targets) == 2, f"HIBA: A 3. bekezdésben 2 'A szultán' kiemelés kell, de {len(targets)} van!"

def test_09_komment_adatok(html_soup):
    with open("szoliman.html", "r", encoding="utf-8") as f:
        assert re.search(r"<!--.*[a-zA-Záéíóöőúüű].*\d{4}.*-->", f.read()), "HIBA: Név vagy dátum hiányzik!"
