import pytest
import os
from bs4 import BeautifulSoup

def test_file_exists():
    """Ellenőrzi, hogy létezik-e az index.html fájl"""
    assert os.path.exists('index.html'), "Az index.html fájl nem található"

def test_html_structure():
    """Ellenőrzi az alapvető HTML struktúrát"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # DOCTYPE ellenőrzés
    assert html_content.strip().startswith('<!DOCTYPE html>'), "Hiányzik a DOCTYPE"
    
    # HTML tag ellenőrzés
    assert soup.html is not None, "Hiányzik az <html> tag"
    assert soup.html.get('lang') == 'hu', "A nyelv nincs beállítva magyarra (lang='hu')"

def test_head_section():
    """Ellenőrzi a head szekciót"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Meta charset ellenőrzés
    meta_charset = soup.find('meta', charset=True)
    assert meta_charset is not None, "Hiányzik a charset meta tag"
    assert meta_charset.get('charset', '').lower() == 'utf-8', "A charset nem utf-8"
    
    # Title ellenőrzés
    assert soup.title is not None, "Hiányzik a <title> tag"
    assert soup.title.string.strip() == 'MIPS', "A cím nem 'MIPS'"

def test_h1_header():
    """Ellenőrzi a főcímet"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    h1 = soup.find('h1')
    assert h1 is not None, "Hiányzik az <h1> fejléc"
    assert h1.get_text(strip=True) == 'MIPS', "Az <h1> tartalma nem 'MIPS'"

def test_h2_headers_count():
    """Ellenőrzi, hogy pontosan 4 h2 fejléc van-e"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    h2_headers = soup.find_all('h2')
    assert len(h2_headers) == 4, f"Pontosan 4 <h2> fejlécnek kell lennie, de {len(h2_headers)} van"

def test_paragraphs_count():
    """Ellenőrzi a bekezdéseket"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    paragraphs = soup.find_all('p')
    assert len(paragraphs) >= 4, f"Legalább 4 bekezdésnek kell lennie, de csak {len(paragraphs)} van"

def test_bold_text():
    """Ellenőrzi, hogy a 'RISC utasításkészletű' félkövér-e"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    strong_text = soup.find('strong')
    assert strong_text is not None, "Hiányzik a <strong> tag"
    assert 'RISC utasításkészletű' in strong_text.get_text(), "A 'RISC utasításkészletű' szöveg nem félkövér"

def test_unordered_lists():
    """Ellenőrzi a számozatlan listákat"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    ul_elements = soup.find_all('ul')
    assert len(ul_elements) == 2, f"Pontosan 2 számozatlan listának kell lennie, de {len(ul_elements)} van"
    
    # Ellenőrzi, hogy nincsenek csillagok
    for ul in ul_elements:
        for li in ul.find_all('li'):
            assert '*' not in li.get_text(), "Csillag található a listában"

def test_hungarian_characters():
    """Ellenőrzi, hogy magyar ékezetes karakterek jól vannak-e kódolva"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Ellenőriz néhány magyar karaktert
    hungarian_chars = ['á', 'é', 'í', 'ó', 'ö', 'ő', 'ú', 'ü', 'ű']
    found = False
    for char in hungarian_chars:
        if char in html_content:
            found = True
            break
    assert found, "Nem található magyar ékezetes karakter a dokumentumban"

def test_comment_in_source():
    """Ellenőrzi, hogy van-e megjegyzés a forráskódban névvel és dátummal"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Egyszerű ellenőrzés - van-e komment Illyés névvel
    assert '<!--' in html_content, "Nincs HTML megjegyzés"
    assert 'Illyés' in html_content, "Nincs 'Illyés' név a forráskódban"
    assert '2026' in html_content, "Nincs '2026' dátum a forráskódban"

def test_body_structure():
    """Ellenőrzi a testreszabott struktúrát - EGYSZERŰSÍTVETT"""
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Csak ellenőrizzük, hogy a body tartalmazza a megjegyzést
    body_text = str(soup.body)
    assert '<!--' in body_text and '-->' in body_text, "Nincs HTML megjegyzés a body-ban"
    assert 'Illyés' in body_text, "Nincs 'Illyés' név a body-ban"