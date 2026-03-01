import pytest
from bs4 import BeautifulSoup
import os

@pytest.fixture
def soup():
    fajl = "index.html"
    if not os.path.exists(fajl):
        pytest.fail(f"A {fajl} nem található!")
    with open(fajl, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def test_01_kodolas_utf8(soup):
    meta = soup.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8"

def test_02_bongeszo_ful_title(soup):
    assert soup.title and soup.title.string == "Roborálás"

def test_03_egyes_szintu_fejezetcim(soup):
    h1 = soup.find("h1")
    assert h1 and h1.get_text().strip() == "Roboráló gyügynövények"

def test_04_bekezdesek_beallitasa(soup):
    p_tags = soup.find_all("p")
    # Legalább 3 bekezdés: 1 (adatok) + 2 (leírások)
    assert len(p_tags) >= 3

def test_05_h2_letrehozasa(soup):
    h2_tags = soup.find_all("h2")
    # Csipkebogyó, Csalán és Forrás = 3 db h2
    assert len(h2_tags) >= 3

def test_05a_h2_tartalma(soup):
    h2_texts = [h2.get_text().strip() for h2 in soup.find_all("h2")]
    assert "Csipkebogyó" in h2_texts
    assert "Csalán" in h2_texts

def test_06_magyar_nyelv(soup):
    assert soup.html.get("lang") == "hu"

def test_07_szamozatlan_lista(soup):
    ul = soup.find("ul")
    assert ul is not None
    li_count = len(ul.find_all("li"))
    assert li_count == 4

def test_08_forras_h2(soup):
    h2_texts = [h2.get_text().strip() for h2 in soup.find_all("h2")]
    assert "Forrás" in h2_texts

def test_09_roboralo_kiemelt(soup):
    # Kiemelés keresése a szövegben
    mark = soup.find("mark")
    assert mark and "Roboráló" in mark.get_text()