from bs4 import BeautifulSoup
import os

HTML_FILE = "hajo.html"  # A vizsgált fájl neve
# Ide írd be a feladatban kért pontos URL-t!
ELVART_URL = "https://hu.wikipedia.org/wiki/Motorcsónak" 

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")

# --- ALAPBEÁLLÍTÁSOK ---

def test_1_file_exists():
    assert os.path.exists(HTML_FILE), f"FAIL: 1. feladat – A '{HTML_FILE}' fájl nem található!"

def test_2_utf8_kodolas():
    html = load_html().lower()
    assert '<meta charset="utf-8">' in html or '<meta charset="utf-8"/>' in html, \
        "FAIL: 2. feladat – A karakterkódolás nem UTF-8 vagy hiányzik a meta tag."

def test_3_magyar_nyelv():
    s = soup()
    html_tag = s.find("html")
    assert html_tag and html_tag.get("lang") == "hu", \
        "FAIL: 3. feladat – A weboldal nyelve nincs magyarra állítva (<html lang=\"hu\">)."

# --- 203. FELADAT SPECIFIKUS TESZTEK ---

def test_4_motorcsanak_link():
    s = soup()
    # Megkeressük a 'motorcsónaknak' szót tartalmazó linket
    link = s.find("a", string=lambda t: t and "motorcsónaknak" in t.lower())
    assert link is not None, "FAIL: 4. feladat – A 'motorcsónaknak' szó nincs linkké (<a>) alakítva."
    assert link.get("href") == ELVART_URL, f"FAIL: 4. feladat – A link URL-je hibás! (Várt: {ELVART_URL})"

def test_5_muszaki_adatok_ellenorzese():
    html = load_html()
    # A képen szereplő pontos értékek keresése
    hibak = []
    if "4 kW-nál nagyobb" not in html:
        hibak.append("'4 kW-nál nagyobb'")
    if "30-40 lábnál hosszabb" not in html:
        hibak.append("'30-40 lábnál hosszabb'")
    
    assert not hibak, f"FAIL: 5. feladat – Hiányzó vagy elírt adatok: {', '.join(hibak)}"

def test_6_jacht_elnevezes():
    html = load_html().lower()
    assert "jachtnak nevezzük" in html, "FAIL: 6. feladat – A 'jachtnak nevezzük' szövegrész hiányzik vagy hibás."
    