import pytest
from bs4 import BeautifulSoup, Comment

@pytest.fixture
def soup():
    # Győződj meg róla, hogy az index.html a megfelelő helyen van
    with open("index.html", "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def test_1_language_is_hungarian(soup):
    assert soup.html.get("lang") == "hu", "1. hiba: A nyelv nincs beállítva magyarnak (lang='hu')."

def test_2_charset_is_utf8(soup):
    meta = soup.find("meta", charset=True)
    assert meta and meta.get("charset").lower() == "utf-8", "2. hiba: Az oldal kódolása nem utf-8."

def test_3_title_is_tru64(soup):
    assert soup.title and soup.title.string == "Tru64", "3. hiba: A böngésző fülön a cím nem 'Tru64'."

def test_4_h1_header(soup):
    h1 = soup.find("h1")
    assert h1 and h1.get_text().strip() == "Tru64 UNIX", "4. hiba: A 'Tru64 UNIX' nincs h1 címsorként megjelölve."

def test_5_paragraph_exists(soup):
    assert soup.find("p"), "5. hiba: Nincs bekezdés (p tag) a fájlban."

def test_6_paragraph_strong_formatting(soup):
    p = soup.find("p")
    strong = p.find("strong")
    assert strong and "Tru64 UNIX" in strong.text, "6. hiba: A 'Tru64 UNIX' szöveg nincs kiemelve (strong tag) a bekezdésben."

def test_7_table_row_added(soup):
    table = soup.find("table")
    rows = table.find_all("tr")
    # Fejléc + 3 adat sor = 4 sor összesen
    assert len(rows) == 4, f"7. hiba: A táblázat nem tartalmazza az új sort. Jelenlegi sorok száma: {len(rows)}"

def test_8_hp_formatting(soup):
    p = soup.find("p")
    strongs = p.find_all("strong")
    hp_found = any("Hewlett-Packard" in s.text for s in strongs)
    assert hp_found, "8. hiba: A 'Hewlett-Packard' szöveg nincs kiemelve (strong tag)."

def test_9_comment_present(soup):
    # Megkeressük a megjegyzést a body elemen belül
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    assert len(comments) > 0, "9. hiba: Nem található megjegyzés a fájlban a névvel és dátummal."