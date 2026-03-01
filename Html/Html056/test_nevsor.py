import pytest
from bs4 import BeautifulSoup, Comment
import os

def get_soup():
    if not os.path.exists("nevsor.html"):
        pytest.fail("A nevsor.html fájl nem található!")
    with open("nevsor.html", "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

# 1. Készítsen egy weblapot nevsor.html néven.
def test_file_exists():
    assert os.path.exists("nevsor.html")

# 2. A weblap nyelve legyen magyar.
def test_language_is_hu():
    soup = get_soup()
    assert soup.html.get("lang") == "hu"

# 3. A weblap kódolása legyen utf-8.
def test_encoding_is_utf8():
    soup = get_soup()
    meta = soup.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8"

# 4. A böngészőfülön megjelenő szöveg legyen „Barátok”.
def test_title_tag():
    soup = get_soup()
    assert soup.title.string.strip() == "Barátok"

# 5. A weblap tetején legyen egyes szintű fejezetcímmel a „Barátok” szó.
def test_h1_baratok():
    soup = get_soup()
    h1_tags = [h.get_text().strip() for h in soup.find_all("h1")]
    assert "Barátok" in h1_tags

# 6. Tegye a listát a weblapba, jelölje HTML listának.
def test_html_list_exists():
    soup = get_soup()
    assert soup.find("ul") is not None or soup.find("ol") is not None

# 7. A weblap tetején megjegyzésben írja saját nevét, csoportját és az aktuális dátumot.
def test_comment_header():
    soup = get_soup()
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    assert len(comments) > 0, "Nincs megjegyzés a fájlban!"

# 8. A lista előtt egyes szintű fejezetcímmel írja ki: „Költők”.
def test_h1_koltok():
    soup = get_soup()
    h1_tags = [h.get_text().strip() for h in soup.find_all("h1")]
    assert "Költők" in h1_tags

# 9. A „Bálint György” név a listában legyen dőltnek jelölve.
def test_balint_gyorgy_italic():
    soup = get_soup()
    italic_tags = [i.get_text().strip() for i in soup.find_all(["i", "em"])]
    assert "Bálint György" in italic_tags