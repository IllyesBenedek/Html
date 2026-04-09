import pytest
from bs4 import BeautifulSoup
import os

def get_html(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def hiba(msg, feladat_szam):
    pytest.fail(f"\n[README {feladat_szam}. PONT HIBA]: {msg}")

oldalak = ["index.html", "termekek.html", "partnerek.html"]

# --- 1. FELADAT: Navigáció helye ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p01_nav_helye(oldal):
    html = get_html(oldal)
    h1 = html.find('h1')
    nav = html.find('nav')
    if not h1 or not nav or h1.find_next('nav') != nav:
        hiba(f"A <nav> elemnek közvetlenül a <h1> után kell lennie!", 1)

# --- 2. FELADAT: HTML elem (<nav>) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p02_nav_elem(oldal):
    html = get_html(oldal)
    if not html.find('nav'):
        hiba(f"Nincs <nav> elem a fájlban!", 2)

# --- 3. FELADAT: Lista használata (<ul>) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p03_lista_ul(oldal):
    html = get_html(oldal)
    nav = html.find('nav')
    if not nav or not nav.find('ul'):
        hiba(f"A <nav>-en belül nincs <ul> lista!", 3)

# --- 4. FELADAT: Hiperhivatkozások száma ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p04_elemek_szama(oldal):
    html = get_html(oldal)
    links = html.select('nav ul li a')
    if len(links) != 3:
        hiba(f"Pontosan 3 linket vártam a listában, de {len(links)}-t találtam!", 4)

# --- 5. FELADAT: Célpontok (href) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p05_link_celpontok(oldal):
    html = get_html(oldal)
    links = html.select('nav a')
    hrefs = [a.get('href') for a in links]
    elvart = ["index.html", "termekek.html", "partnerek.html"]
    if not hrefs: hiba("Nem találtam linkeket!", 5)
    for cel in elvart:
        if cel not in hrefs:
            hiba(f"Hiányzik a link ide: {cel}", 5)

# --- 6. FELADAT: Szövegek ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p06_link_szovegek(oldal):
    html = get_html(oldal)
    links = html.select('nav a')
    
    if not links: 
        hiba("Nincsenek linkek, amiknek lehetne szövege!", 6)
    
    # Csak ezeket a szövegeket fogadjuk el
    elfogadott = ["főoldal", "termékek", "partnerek"]
    
    for a in links:
        szoveg = a.text.strip().lower() # Kisbetűssé alakítjuk az összehasonlításhoz
        
        # Ellenőrizzük, hogy üres-e
        if not szoveg:
            hiba(f"A(z) '{a.get('href')}' linknek nincs szövege!", 6)

        # Ellenőrizzük, hogy a megadott három szó egyike-e
        if szoveg not in elfogadott:
            hiba(f"A(z) '{a.text.strip()}' szöveg nem megfelelő! Csak a 'Főoldal', 'Termékek' vagy 'Partnerek' szavakat használd!", 6)

    # Ellenőrizzük, hogy mind a három különböző szó szerepel-e (ne legyen 3db "Főoldal")
    talalt_szovegek = [a.text.strip().lower() for a in links]
    if len(set(talalt_szovegek)) < 3:
        hiba("A navigációban mind a három menüpontnak (Főoldal, Termékek, Partnerek) szerepelnie kell!", 6)
