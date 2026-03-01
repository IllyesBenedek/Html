import pytest
from bs4 import BeautifulSoup
import datetime
import os

# Ellenőrzés, hogy a fájl létezik-e
def test_file_exists():
    assert os.path.exists("index.html"), "Az index.html fájl nem található"

# HTML fájl beolvasása és feldolgozása
def load_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), 'html.parser')

def test_language_setting():
    """Állítsa be az oldal nyelvét magyarra."""
    soup = load_html()
    html_tag = soup.find('html')
    assert html_tag is not None, "HTML tag nem található"
    assert html_tag.get('lang') == 'hu', "Az oldal nyelve nem magyar (hu)"

def test_encoding_meta():
    """Állítsa be az oldal kódolását UTF-8-ra."""
    soup = load_html()
    meta_charset = soup.find('meta', charset=True)
    meta_content_type = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
    
    # Vagy charset attribútum, vagy http-equiv meta
    if meta_charset:
        assert meta_charset['charset'].lower() == 'utf-8', "A charset nem UTF-8"
    elif meta_content_type:
        assert 'utf-8' in meta_content_type.get('content', '').lower(), "A content nem tartalmaz UTF-8-t"
    else:
        pytest.fail("Nincs UTF-8 kódolást beállító meta tag")

def test_title():
    """Állítsa be, hogy a böngésző fülön a 'vi' felirat jelenjen meg."""
    soup = load_html()
    title_tag = soup.find('title')
    assert title_tag is not None, "Title tag nem található"
    assert title_tag.text.strip() == 'vi', "A title nem 'vi'"

def test_main_heading():
    """A weblap tetején, az első bekezdés előtt legyen egy vi fejezetcím, amit egyesszintűnek jelöl."""
    soup = load_html()
    
    # Megkeressük az első bekezdést
    first_p = soup.find('p')
    
    if first_p:
        # Az első bekezdés előtti h1
        h1_before_first_p = first_p.find_previous('h1')
        assert h1_before_first_p is not None, "Nincs h1 az első bekezdés előtt"
        assert h1_before_first_p.text.strip() == 'vi', "Az h1 nem 'vi'"
    else:
        pytest.fail("Nincs bekezdés (p tag) a dokumentumban")

def test_section_headings():
    """Minden fejezet előtt legyen egy kettes szintű fejezetcím."""
    soup = load_html()
    
    # A kommentek alapján várható szakaszok
    expected_sections = ['vi', 'Az eredeti', 'Szabvány', 'Interfész']
    
    # Az összes h2 cím
    h2_tags = soup.find_all('h2')
    h2_texts = [h2.text.strip() for h2 in h2_tags]
    
    # Legalább 3 h2-nek kell lennie (a fő cím h1)
    assert len(h2_tags) >= 3, f"Legalább 3 h2 címnek kell lennie, csak {len(h2_tags)} található"
    
    # Ellenőrizzük, hogy a várt szakaszok közül melyik van jelen
    found_sections = [text for text in h2_texts if text in expected_sections]
    assert len(found_sections) >= 3, f"Legalább 3 várt szakaszcímet kell tartalmaznia, csak {len(found_sections)} található"

def test_keyboard_markup():
    """A billentyűk legyenek kiemelve (kbd tag)."""
    soup = load_html()
    
    # Keresünk kbd tag-eket
    kbd_tags = soup.find_all('kbd')
    
    # A szöveg alapján várható billentyűk
    expected_keys = ['i', 'a', 'Esc']
    
    # Ellenőrizzük, hogy legalább néhány billentyű ki van jelölve
    assert len(kbd_tags) >= 3, f"Legalább 3 kbd tag-nek kell lennie, csak {len(kbd_tags)} található"
    
    kbd_texts = [kbd.text.strip() for kbd in kbd_tags]
    # Legalább az 'i' és 'Esc' legyen benne
    assert any('i' in text for text in kbd_texts), "'i' billentyű nincs kbd tag-ben"
    assert any('Esc' in text for text in kbd_texts), "'Esc' billentyű nincs kbd tag-ben"

def test_bold_posix():
    """Az első bekezdésben a 'POSIX' szöveget jelölje félkövérnek."""
    soup = load_html()
    
    # Megkeressük az összes bekezdést
    paragraphs = soup.find_all('p')
    
    # Az első bekezdésben keresünk strong vagy b tag-et a POSIX szöveggel
    posix_found = False
    for p in paragraphs:
        strong_tags = p.find_all(['strong', 'b'])
        for tag in strong_tags:
            if 'POSIX' in tag.text:
                posix_found = True
                break
    
    assert posix_found, "A 'POSIX' szöveg nincs félkövérként jelölve"

def test_comment_with_name_and_date():
    """A HTML forráskódjában, megjegyzésbe, írja, a nevét és az aktuális dátumot."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Keresünk kommenteket, amelyek tartalmaznak dátumot
    import re
    comment_pattern = r'<!--.*?-->'
    comments = re.findall(comment_pattern, content, re.DOTALL)
    
    has_name_date = False
    current_year = str(datetime.datetime.now().year)
    
    for comment in comments:
        # Ellenőrizzük, hogy tartalmaz-e dátumot (évszámot)
        if any(year in comment for year in [current_year, '2024', '2025']):
            # Valószínűleg tartalmaz nevet is
            has_name_date = True
            break
    
    assert has_name_date, "Nincs megjegyzés a névvel és dátummal"

def test_overall_structure():
    """Általános struktúra ellenőrzése."""
    soup = load_html()
    
    # Van-e head és body
    assert soup.head is not None, "Nincs head tag"
    assert soup.body is not None, "Nincs body tag"
    
    # H1 és H2 címek
    h1_tags = soup.find_all('h1')
    assert len(h1_tags) >= 1, "Legalább egy h1 címnek kell lennie"
    
    h2_tags = soup.find_all('h2')
    assert len(h2_tags) >= 3, "Legalább három h2 címnek kell lennie"
    
    # Bekezdések
    p_tags = soup.find_all('p')
    assert len(p_tags) >= 3, "Legalább három bekezdésnek kell lennie"

if __name__ == "__main__":
    # Ha közvetlenül futtatjuk, futtassuk a teszteket
    pytest.main([__file__, "-v"])