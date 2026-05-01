import pytest
from bs4 import BeautifulSoup
import os

@pytest.fixture
def html_soup():
    path = "szoliman.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_01_tartalom_beillesztes(html_soup):
    """1. Feladat: A szöveg beillesztése megtörtént."""
    body_text = html_soup.body.get_text()
    assert "Szolimán elkomorult" in body_text

def test_02_nyelv_beallitas(html_soup):
    """2. Feladat: Az oldal nyelve magyar (lang='hu')."""
    html_tag = html_soup.find("html")
    assert html_tag.get("lang") == "hu", "A nyelvi attribútum nem 'hu'."

def test_03_bongeszo_cim(html_soup):
    """3. Feladat: A title elem tartalma 'Szoliman'."""
    assert html_soup.title.text == "Szoliman", "A title nem megfelelő."

def test_04_fo_fejezetcim(html_soup):
    """4. Feladat: h1 fejezetcím 'Szoliman' tartalommal."""
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text == "Szoliman"

def test_05_bekezdesek_szama(html_soup):
    """5. Feladat: Pontosan három bekezdés (p) van a kódban."""
    paragraphs = html_soup.find_all("p")
    assert len(paragraphs) == 3

def test_06_alcimek_ellenorzese(html_soup):
    """6. Feladat: h2 alcímek szövegeinek ellenőrzése."""
    expected = ["A szemrehányás", "A szentkönyv", "A leborulás"]
    h2_tags = html_soup.find_all("h2")
    assert len(h2_tags) == 3
    for i, tag in enumerate(h2_tags):
        assert tag.text.strip() == expected[i]

def test_07_dolt_formazas(html_soup):
    """7. Feladat: 'tekintete azalatt' dőlt betűs az első bekezdésben."""
    p1 = html_soup.find_all("p")[0]
    italic = p1.find("i") or p1.find("em")
    assert italic is not None and "tekintete azalatt" in italic.text

def test_08_szigorany_dupla_kiemeles(html_soup):
    """8. Feladat: Csak akkor sikerül, ha PONTOSAN 2 darab 'A szultán' kiemelés van."""
    p3 = html_soup.find_all("p")[2]
    highlights = p3.find_all(["strong", "b"])
    count = sum(1 for tag in highlights if "A szultán" in tag.text)
    assert count == 2, f"HIBA: {count} kiemelést találtam a 2 helyett!"

def test_09_komment(html_soup):
    """9. Feladat: Megjegyzés megléte névvel és dátummal."""
    with open("szoliman.html", "r", encoding="utf-8") as f:
        content = f.read()
        # Csak akkor megy át, ha a kommentben ott a név és a dátum is
        assert "<!--" in content and "-->" in content
        assert "Benedek" in content
        assert "2026.05.01" in content