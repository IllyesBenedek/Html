git init
git remote add origin https://github.com/IllyesBenedek/Html.gitimport pytest
from bs4 import BeautifulSoup, Comment
import os

# Segédfüggvény a fájl betöltéséhez
def load_soup():
    path = "index.html"
    if not os.path.exists(path):
        pytest.fail("Az index.html fájl nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

# 1. Az oldal nyelve magyar
def test_language_hu():
    soup = load_soup()
    html = soup.find("html")
    assert html is not None and html.get("lang") == "hu", "A <html lang='hu'> hiányzik vagy hibás!"

# 2. UTF-8 kódolás beállítása
def test_charset_utf8():
    soup = load_soup()
    meta = soup.find("meta", charset=lambda x: x and x.lower() == "utf-8")
    assert meta is not None, "A <meta charset='utf-8'> hiányzik!"

# 3. Böngésző fül szövege: „Kovász”
def test_title_kovasz():
    soup = load_soup()
    assert soup.title is not None and soup.title.string.strip() == "Kovász", "A <title> szövege nem 'Kovász'!"

# 4. „Kovászos kenyér” <h1> fejezetcím
def test_h1_kovaszos_kenyer():
    soup = load_soup()
    h1 = soup.find("h1")
    assert h1 is not None and "Kovászos kenyér" in h1.text, "A 'Kovászos kenyér' nem <h1> fejezetcím!"

# 5. & 6. „Tartalom” és „Glutén” h2 és bekezdések
@pytest.mark.parametrize("header_text", ["Tartalom", "Glutén"])
def test_headers_and_paragraphs(header_text):
    soup = load_soup()
    h2 = soup.find("h2", string=lambda s: s and header_text in s)
    assert h2 is not None, f"A '{header_text}' nem <h2> szintű fejezetcím!"
    
    # Ellenőrizzük, hogy van-e utána bekezdés (p)
    p = h2.find_next_sibling("p")
    assert p is not None, f"A '{header_text}' fejezetcím után nincs bekezdés (<p>)!"

# 7. „Előnyök” számozatlan lista (ul)
def test_benefits_list():
    soup = load_soup()
    # Megkeressük a szöveget, ami után a listának lennie kell
    benefits_text = soup.find(string=lambda s: "Előnyök" in s if s else False)
    assert benefits_text is not None, "Az 'Előnyök' szöveg nem található!"
    
    # Megkeressük a legközelebbi ul-t
    ul = soup.find("ul")
    assert ul is not None, "Hiányzik a számozatlan lista (<ul>)!"
    assert len(ul.find_all("li")) >= 4, "A listának legalább 4 elemet (<li>) kell tartalmaznia!"

# 8. „Forrás” szöveg megjegyzésben (comment)
def test_source_comment():
    soup = load_soup()
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    assert any("Forrás" in c for c in comments), "A 'Forrás' szövegnek HTML megjegyzésben () kell lennie!"

# 9. „niacint” szó dőlt betűvel
def test_italic_niacin():
    soup = load_soup()
    # Megnézzük az <i> vagy <em> tageket
    italics = soup.find_all(["i", "em"])
    found = any("niacint" in tag.text.lower() for tag in italics)
    assert found, "A 'niacint' szó nincs dőltnek (<i> vagy <em>) jelölve!"