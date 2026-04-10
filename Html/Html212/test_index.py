import pytest
from bs4 import BeautifulSoup
import os

def get_html(filename):
    if not os.path.exists(filename): return None
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content: return None
        return BeautifulSoup(content, 'html.parser')

def hiba(msg, feladat_szam, oldal=""):
    helyszin = f" [{oldal}]" if oldal else ""
    pytest.fail(f"\n[README {feladat_szam}. PONT HIBA]{helyszin}: {msg}")

# A te fájljaid listája
oldalak = ["index.html", "kultura.html", "megoldas.html"]

# --- 1. FELADAT: Navigáció helye (h1 ELŐTT) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p01_nav_helye(oldal):
    html = get_html(oldal)
    if not html: hiba(f"A fájl nem létezik vagy üres!", 1, oldal)
    h1 = html.find('h1')
    nav = html.find('nav')
    if not h1: hiba("Nincs <h1> cím a fájlban!", 1, oldal)
    if not nav: hiba("Nincs <nav> elem a fájlban!", 1, oldal)
    if nav.find_next('h1') != h1:
        hiba("A <nav> elemnek közvetlenül a <h1> ELŐTT kell lennie!", 1, oldal)

# --- 2. FELADAT: HTML elem (<nav>) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p02_nav_elem(oldal):
    html = get_html(oldal)
    if not html or not html.find('nav'):
        hiba("A navigációhoz szükséges <nav> elem hiányzik!", 2, oldal)

# --- 3. FELADAT: Lista használata (<ul>) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p03_lista_ul(oldal):
    html = get_html(oldal)
    if not html: hiba("Nincs fájl tartalom!", 3, oldal)
    nav = html.find('nav')
    if not nav or not nav.find('ul'):
        hiba("A <nav>-en belül nincs <ul> lista!", 3, oldal)

# --- 4. FELADAT: Hiperhivatkozások száma (3 db) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p04_elemek_szama(oldal):
    html = get_html(oldal)
    if not html: hiba("Nincs fájl tartalom!", 4, oldal)
    links = html.select('nav ul li a')
    if len(links) != 3:
        hiba(f"Pontosan 3 linket vártam a listában, de {len(links)}-t találtam!", 4, oldal)

# --- 5. FELADAT: Célpontok (href) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p05_link_celpontok(oldal):
    html = get_html(oldal)
    if not html: hiba("Nincs fájl tartalom!", 5, oldal)
    links = html.select('nav a')
    hrefs = [a.get('href', '') for a in links]
    elvart = ["index.html", "kultura.html", "megoldas.html"]
    for cel in elvart:
        if cel not in hrefs:
            hiba(f"Hiányzik a link ide: {cel}", 5, oldal)

# --- 6. FELADAT: Szövegek (Főoldal, Kultúra, Megoldás) ---
@pytest.mark.parametrize("oldal", oldalak)
def test_p06_link_szovegek(oldal):
    html = get_html(oldal)
    if not html: hiba("Nincs fájl tartalom!", 6, oldal)
    links = html.select('nav a')
    if not links: hiba("Nincsenek linkek a navigációban!", 6, oldal)
    
    elfogadott = ["főoldal", "kultúra", "kultura", "megoldás", "megoldas"]
    for a in links:
        szoveg = a.text.strip().lower()
        if not szoveg or szoveg not in elfogadott:
            hiba(f"A(z) '{a.text.strip()}' szöveg nem megfelelő navigációs névnek!", 6, oldal)

# --- 7. FELADAT: Forrás URL az index.html oldalon ---
def test_p07_forras_link():
    oldal = "index.html"
    html = get_html(oldal)
    if not html: hiba("Az index.html nem található!", 7, oldal)
    
    forras_url = "https://szit.hu/download/adat/oktatas/web/html/html_212_forras.zip"
    all_links = html.find_all('a')
    nav_links = html.select('nav a')
    
    # Megnézzük, van-e olyan link, ami nem a nav-ban van és a jó URL-re mutat
    talalt_forras = False
    for a in all_links:
        if a not in nav_links and a.get('href') == forras_url:
            talalt_forras = True
            break
            
    if not talalt_forras:
        hiba(f"Az index.html oldalon hiányzik a forrás ZIP link: {forras_url}", 7, oldal)
