import pytest
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime

@pytest.fixture
def html_content():
    """Betölti az autok.html tartalmát"""
    with open('autok.html', 'r', encoding='utf-8') as file:
        return file.read()

@pytest.fixture
def soup(html_content):
    """BeautifulSoup objektum a HTML elemzéshez"""
    return BeautifulSoup(html_content, 'html.parser')

def test_file_exists():
    """Ellenőrzi, hogy a fájl létezik"""
    assert os.path.exists('autok.html'), "Az autok.html fájl nem található"

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
    assert title_tag.string.strip() == 'Autók', f"A cím nem 'Autók', hanem '{title_tag.string}'"

def test_h1_heading(soup):
    """Ellenőrzi a főcím létezését"""
    h1_tag = soup.find('h1')
    assert h1_tag is not None, "Nincs h1 elem"
    assert h1_tag.string.strip() == 'Autók', f"A h1 nem 'Autók', hanem '{h1_tag.string}'"

def test_h2_heading(soup):
    """Ellenőrzi a másodlagos címsort"""
    h2_tag = soup.find('h2')
    assert h2_tag is not None, "Nincs h2 elem"
    assert h2_tag.string.strip() == 'Márkák', f"A h2 nem 'Márkák', hanem '{h2_tag.string}'"

def test_unordered_list(soup):
    """Ellenőrzi a számozatlan listát"""
    ul_tag = soup.find('ul')
    assert ul_tag is not None, "Nincs ul (unordered list) elem"
    
    li_tags = ul_tag.find_all('li')
    assert len(li_tags) == 8, f"Nem 8 li elem van a listában, hanem {len(li_tags)}"
    
    # Ellenőrizzük az összes kért márkát
    li_texts = [li.get_text(strip=True) for li in li_tags]
    expected_items = ['Lada', 'Ford', 'Opel', 'Citroen', 'Fiat', 'Mazda', 'Porsche', 'Peugeot']
    
    for expected in expected_items:
        # Opel-t kiemeltként kell ellenőrizni
        if expected == 'Opel':
            opel_li = li_tags[li_texts.index('Opel')]
            strong_tag = opel_li.find('strong')
            assert strong_tag is not None, "'Opel' nincs kiemelve strong tag-ben"
            assert strong_tag.string.strip() == 'Opel', f"A strong elem nem 'Opel', hanem '{strong_tag.string}'"
        else:
            assert expected in li_texts, f"'{expected}' márka hiányzik a listából"

def test_opel_emphasized(soup):
    """Külön teszt az Opel kiemelésére"""
    ul_tag = soup.find('ul')
    li_tags = ul_tag.find_all('li')
    
    opel_found = False
    for li in li_tags:
        if 'Opel' in li.get_text():
            opel_found = True
            strong_tag = li.find('strong')
            assert strong_tag is not None, "'Opel' nincs kiemelve strong tag-ben"
            assert strong_tag.string.strip() == 'Opel', f"A strong elem nem 'Opel', hanem '{strong_tag.string}'"
            break
    
    assert opel_found, "'Opel' márka nem található a listában"

def test_comment_exists(html_content):
    """Ellenőrzi, hogy van megjegyzés a készítőről, csoportról és dátumról"""
    # A megjegyzéseket manuálisan keresünk a HTML szövegben
    assert '<!--' in html_content, "Nincsenek megjegyzések a HTML-ben"
    
    # Ellenőrizzük, hogy van-e a készítőre utaló megjegyzés
    comment_pattern = r'<!--.*?-->'
    comments = re.findall(comment_pattern, html_content, re.DOTALL)
    
    assert len(comments) > 0, "Nincsenek megjegyzések a HTML-ben"
    
    # Nézzük meg, hogy valamelyik megjegyzés tartalmazza-e a készítő adatait
    has_info_comment = any(
        ('Illyés' in comment or 'Benedek' in comment or 'Csoport' in comment or 'Html054' in comment or '2025' in comment) 
        for comment in comments
    )
    
    assert has_info_comment, "Nincs megjegyzés a készítőről, csoportról és dátumról"

def test_list_order_and_completeness(soup):
    """Ellenőrzi, hogy a lista teljes és a megfelelő sorrendben van"""
    ul_tag = soup.find('ul')
    li_tags = ul_tag.find_all('li')
    
    # A lista szöveges tartalmának megszerzése (Opel esetén a strong tag tartalmát)
    li_contents = []
    for li in li_tags:
        # Ha van strong tag, annak tartalmát vesszük
        strong = li.find('strong')
        if strong:
            li_contents.append(strong.get_text(strip=True))
        else:
            li_contents.append(li.get_text(strip=True))
    
    # Ellenőrizzük az elvárt sorrendet
    expected_order = ['Lada', 'Ford', 'Opel', 'Citroen', 'Fiat', 'Mazda', 'Porsche', 'Peugeot']
    
    assert li_contents == expected_order, f"A lista nem a megfelelő sorrendben van: {li_contents}"

if __name__ == '__main__':
    pytest.main(['-v', 'test_autok.py'])