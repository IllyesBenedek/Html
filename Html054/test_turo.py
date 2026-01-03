import pytest
import os
import re
from bs4 import BeautifulSoup

@pytest.fixture
def html_content():
    """Betölti a turo.html tartalmát"""
    with open('turo.html', 'r', encoding='utf-8') as file:
        return file.read()

@pytest.fixture
def soup(html_content):
    """BeautifulSoup objektum a HTML elemzéshez"""
    return BeautifulSoup(html_content, 'html.parser')

def test_file_exists():
    """Ellenőrzi, hogy a fájl létezik"""
    assert os.path.exists('turo.html'), "A turo.html fájl nem található"

def test_html_structure(soup):
    """Ellenőrzi az alap HTML struktúrát"""
    assert soup.html is not None, "Nincs html elem"
    assert soup.head is not None, "Nincs head elem"
    assert soup.body is not None, "Nincs body elem"

def test_language_attribute(soup):
    """Ellenőrzi, hogy a nyelv magyarra van állítva"""
    html_tag = soup.html
    assert 'lang' in html_tag.attrs, "A html elemnek nincs lang attribútuma"
    assert html_tag['lang'] == 'hu', f"A nyelv nem 'hu', hanem '{html_tag['lang']}'"

def test_character_encoding(soup):
    """Ellenőrzi a karakterkódolást"""
    meta_charset = soup.find('meta', {'charset': True})
    assert meta_charset is not None, "Nincs charset meta tag"
    assert meta_charset['charset'].lower() == 'utf-8', f"A karakterkódolás nem UTF-8, hanem '{meta_charset['charset']}'"

def test_title(soup):
    """Ellenőrzi a cím megfelelőségét"""
    title_tag = soup.find('title')
    assert title_tag is not None, "Nincs title tag"
    assert title_tag.string.strip() == 'Túrószelet', f"A cím nem 'Túrószelet', hanem '{title_tag.string}'"

def test_h1_heading(soup):
    """Ellenőrzi a főcím létezését"""
    h1_tag = soup.find('h1')
    assert h1_tag is not None, "Nincs h1 elem"
    assert h1_tag.string.strip() == 'Túrószelet', f"A h1 nem 'Túrószelet', hanem '{h1_tag.string}'"

def test_h2_headings(soup):
    """Ellenőrzi a másodlagos címsorokat"""
    h2_tags = soup.find_all('h2')
    assert len(h2_tags) >= 2, f"Nincs elég h2 elem. Csak {len(h2_tags)} található"
    
    h2_texts = [h2.get_text(strip=True) for h2 in h2_tags]
    assert 'Hozzávalók' in h2_texts, "'Hozzávalók' h2 elem hiányzik"
    assert 'Elkészítés' in h2_texts, "'Elkészítés' h2 elem hiányzik"

def test_unordered_list(soup):
    """Ellenőrzi a számozatlan listát"""
    ul_tag = soup.find('ul')
    assert ul_tag is not None, "Nincs ul (unordered list) elem"
    
    li_tags = ul_tag.find_all('li')
    assert len(li_tags) == 7, f"Nem 7 li elem van a listában, hanem {len(li_tags)}"
    
    # Ellenőrizzünk néhány tipikus hozzávalót
    li_texts = [li.get_text(strip=True) for li in li_tags]
    expected_items = ['túró', 'burgonya', 'tojás', 'liszt', 'búzadara', 'só', 'zsír']
    
    for expected in expected_items:
        found = any(expected in li_text.lower() for li_text in li_texts)
        assert found, f"'{expected}' hozzávaló hiányzik a listából"

def test_paragraphs(soup):
    """Ellenőrzi a bekezdéseket"""
    p_tags = soup.find_all('p')
    assert len(p_tags) >= 3, f"Nincs elég p elem. Legalább 3 kellene, de csak {len(p_tags)} van"
    
    # Az első két bekezdés az elkészítéshez tartozik
    prep_paragraphs = [p for p in p_tags if 'burgonyát' in p.get_text() or 'Állni' in p.get_text()]
    assert len(prep_paragraphs) >= 2, "Nem találhatók megfelelően az elkészítés bekezdései"

def test_strong_element(soup):
    """Ellenőrzi, hogy a Wikibooks szó kiemelve van"""
    strong_tag = soup.find('strong')
    assert strong_tag is not None, "Nincs strong elem"
    assert strong_tag.string.strip() == 'Wikibooks', f"A strong elem nem 'Wikibooks', hanem '{strong_tag.string}'"

def test_comment_exists(html_content):
    """Ellenőrzi, hogy van megjegyzés a készítőről"""
    # A megjegyzéseket manuálisan keresünk a HTML szövegben
    assert '<!--' in html_content, "Nincsenek megjegyzések a HTML-ben"
    
    # Ellenőrizzük, hogy van-e a készítőre utaló megjegyzés
    # A keresés nem case-sensitive, mert lehet különböző írásmód
    comment_pattern = r'<!--.*?-->'
    comments = re.findall(comment_pattern, html_content, re.DOTALL)
    
    assert len(comments) > 0, "Nincsenek megjegyzések a HTML-ben"
    
    # Nézzük meg, hogy valamelyik megjegyzés tartalmazza-e a készítő nevét vagy dátumot
    has_name_comment = any(
        ('Illyés' in comment or 'Benedek' in comment or '2025' in comment) 
        for comment in comments
    )
    
    assert has_name_comment, "Nincs megjegyzés a készítőről és dátumról"

if __name__ == '__main__':
    pytest.main(['-v', 'test_turo.py'])