import pytest
from bs4 import BeautifulSoup
import os

def get_html(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')

def hiba(msg, feladat_szam):
    pytest.fail(f"\n[README {feladat_szam}. PONT HIBA]: {msg}")

# A te fájljaid listája
oldalak = ["index.html", "kultura.html", "megoldas.html"]

# --- 1. FELADAT: Navigáció helye (h1 ELŐTT) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p01_nav_helye(oldal):
    html = get_html(oldal)
    if not html: hiba(f"A(z) {oldal} fájl nem található!", 1)
    h1 = html.find('h1')
    nav = html.find('nav')
    if not h1 or not nav or nav.find_next('h1') != h1:
        hiba(f"A <nav> elemnek közvetlenül a <h1> ELŐTT kell lennie!", 1)

# --- 2. FELADAT: HTML elem (<nav>) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p02_nav_elem(oldal):
    html = get_html(oldal)
    if not html or not html.find('nav'):
        hiba(f"Nincs <nav> elem a fájlban!", 2)

# --- 3. FELADAT: Lista használata (<ul>) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p03_lista_ul(oldal):
    html = get_html(oldal)
    if not html: return
    nav = html.find('nav')
    if not nav or not nav.find('ul'):
        hiba(f"A <nav>-en belül nincs <ul> lista!", 3)

# --- 4. FELADAT: Hiperhivatkozások száma ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p04_elemek_szama(oldal):
    html = get_html(oldal)
    if not html: return
    links = html.select('nav ul li a')
    if len(links) != 3:
        hiba(f"Pontosan 3 linket vártam a navigációs listában, de {len(links)}-t találtam!", 4)

# --- 5. FELADAT: Célpontok (href) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p05_link_celpontok(oldal):
    html = get_html(oldal)
    if not html: return
    links = html.select('nav a')
    hrefs = [a.get('href') for a in links]
    elvart = ["index.html", "kultura.html", "megoldas.html"]
    for cel in elvart:
        if cel not in hrefs:
            hiba(f"Hiányzik a link ide: {cel}", 5)

# --- 6. FELADAT: Szövegek (Főoldal, Kultúra, Megoldás) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p06_link_szovegek(oldal):
    html = get_html(oldal)
    if not html: return
    links = html.select('nav a')
    elfogadott = ["főoldal", "kultúra", "kultura", "megoldás", "megoldas"]
    
    if not links: hiba("Nincsenek linkek!", 6)
    
    for a in links:
        szoveg = a.text.strip().lower()
        if not szoveg:
            hiba(f"A(z) '{a.get('href')}' linknek nincs szövege!", 6)
        if szoveg not in elfogadott:
            hiba(f"A(z) '{a.text.strip()}' szöveg nem elfogadható!", 6)

# --- 7. FELADAT: Forrás URL az index.html oldalon ---
def test_p07_forras_link():
    html = get_html("index.html")
    if not html: return
    all_links = html.find_all('a')
    nav_links = html.select('nav a')
    
    # Olyan linket keresünk, ami nincs a nav-ban és a feladatban megadott URL
    forras_url = "https://szit.hu/download/adat/oktatas/web/html/html_212_forras.zip"
    
    talalt_forras = False
    for a in all_links:
        if a not in nav_links and a.get('href') == forras_url:
            talalt_forras = True
            break
            
    if not talalt_forras:
        hiba(f"Az index.html oldalon nem található a forráslink: {forras_url}", 7)
