import pytest
from bs4 import BeautifulSoup
import os

# Beállítások
HTML_FILE = "tehergepkocsi.html"
URL_WIKI = "https://hu.wikipedia.org/wiki/Tehergepkocsi"

def load_html():
    """Segédfüggvény a HTML fájl beolvasásához UTF-8 kódolással."""
    if not os.path.exists(HTML_FILE):
        return None
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()

def get_soup():
    """Segédfüggvény a BeautifulSoup objektum létrehozásához."""
    content = load_html()
    if content:
        return BeautifulSoup(content, "html.parser")
    return None

# --- TESZTEK ---

def test_1_file_exists():
    """Ellenőrzi, hogy létezik-e a fájl."""
    assert os.path.exists(HTML_FILE), f"Hiba: A {HTML_FILE} fájl nem található!"

def test_2_utf8_encoding():
    """Ellenőrzi az UTF-8 karakterkódolást."""
    html = load_html()
    assert html is not None
    assert 'charset="utf-8"' in html.lower(), "FAIL: Hiányzik vagy hibás a karakterkódolás (<meta charset='utf-8'>)!"

def test_3_language_hu():
    """Ellenőrzi a magyar nyelv beállítását."""
    soup = get_soup()
    html_tag = soup.find("html")
    assert html_tag is not None and html_tag.get("lang") == "hu", "FAIL: A nyelv nincs magyarra állítva (<html lang='hu'>)!"

def test_4_title_and_h1():
    """Ellenőrzi az oldal címét és a főcímet."""
    soup = get_soup()
    # Főcím (h1) ellenőrzése
    h1 = soup.find("h1")
    assert h1 is not None and "Tehergépkocsi" in h1.text, "FAIL: A főcím (h1) hiányzik vagy nem 'Tehergépkocsi'!"

def test_5_paragraph_text():
    """Ellenőrzi a bekezdés meglétét és tartalmát."""
    soup = get_soup()
    p = soup.find("p")
    assert p is not None, "FAIL: A szöveg nincs bekezdésbe (<p>) téve!"
    assert "Nicolas-Joseph Cugnot" in p.text, "FAIL: A szöveg tartalma pontatlan!"

def test_6_inline_link():
    """Ellenőrzi a szövegben lévő linket (tehergépjárműnek)."""
    soup = get_soup()
    p = soup.find("p")
    a_link = p.find("a")
    assert a_link is not None, "FAIL: Nincs link a bekezdésben!"
    assert "tehergépjárműnek" in a_link.text, "FAIL: A link szövege nem 'tehergépjárműnek'!"
    assert a_link["href"] == URL_WIKI, f"FAIL: A link URL-je hibás! (Várt: {URL_WIKI})"

def test_7_h2_forras():
    """Ellenőrzi a kettes szintű fejezetcímet."""
    soup = get_soup()
    h2 = soup.find("h2")
    assert h2 is not None and "Forrás" in h2.text, "FAIL: Hiányzik a kettes szintű 'Forrás' fejezetcím (h2)!"

def test_8_source_list():
    """Ellenőrzi a forrás listát és az abban lévő linket."""
    soup = get_soup()
    ul = soup.find("ul")
    assert ul is not None, "FAIL: A forrás nincs listába (<ul>) téve!"
    li = ul.find("li")
    assert li is not None, "FAIL: A listában nincs elem (<li>)!"
    a_link = li.find("a")
    assert a_link is not None and a_link["href"] == URL_WIKI, "FAIL: A listában lévő URL hibás vagy hiányzik!"
