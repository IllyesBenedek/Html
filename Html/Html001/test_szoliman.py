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
    # 1. Tartalom ellenőrzése a törzsben
    body_text = html_soup.body.get_text()
    assert "Szolimán elkomorult" in body_text

def test_02_nyelv_beallitas(html_soup):
    # 2. Nyelv magyarra (hu) állítása
    assert html_soup.html.get("lang") == "hu"

def test_03_title_szoliman(html_soup):
    # 3. Böngészőfül címe: Szolimán
    assert html_soup.title.text.strip() == "Szoliman"

def test_04_h1_szoliman(html_soup):
    # 4. Egyes szintű fejezetcím: Szolimán
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "Szoliman"

def test_05_bekezdesek_szama(html_soup):
    # 5. Három bekezdés (<p>) megléte
    ps = html_soup.find_all("p")
    assert len(ps) >= 3

def test_06_h2_alcimek(html_soup):
    # 6. Kettes szintű fejezetcímek ellenőrzése
    expected = {"A szemrehányás", "A szentkönyv", "A leborulás"}
    actual = {tag.text.strip() for tag in html_soup.find_all("h2")}
    hianyzo = expected - actual
    assert not hianyzo, f"Hiba! Ezek az alcímek hiányoznak: {hianyzo}. Jelenleg ezeket találtam: {actual}"
    assert len(actual) == 3, f"Hiba: {len(actual)} alcím van a 3 helyett!"

def test_07_dolt_tekintete(html_soup):
    # 7. "tekintete azalatt" dőlt (i vagy em)
    target = html_soup.find(["i", "em"], string=re.compile("tekintete azalatt"))
    assert target is not None

def test_08_strong_szultan(html_soup):
    # 8. "A szultán" kiemelt (strong) 2-szer a harmadik bekezdésben
    targets = html_soup.find_all("strong", string=re.compile("A szultán"))
    assert len(targets) == 2 

def test_09_komment_adatok(html_soup):
    # 9. Név és dátum a forráskódban
    with open("szoliman.html", "r", encoding="utf-8") as f:
        content = f.read()
        # Dátum formátum: YYYY.MM.DD vagy YYYY-MM-DD
        assert re.search(r"<!--.*\d{4}[-.]\d{2}[-.]\d{2}.*-->", content) is not None
