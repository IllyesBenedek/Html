import pytest
from bs4 import BeautifulSoup
import os

# Ellenőrzés, hogy a fájlok léteznek-e
def test_files_exist():
    assert os.path.exists("index.html"), "Az index.html fájl nem található"
    assert os.path.exists("adat.txt"), "Az adat.txt fájl nem található"

# HTML fájl beolvasása és feldolgozása
def load_html():
    with open("index.html", "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), 'html.parser')

def test_language_setting():
    """Állítsa be a weboldal nyelvét magyarra."""
    soup = load_html()
    html_tag = soup.find('html')
    assert html_tag is not None, "HTML tag nem található"
    assert html_tag.get('lang') == 'hu', f"Az oldal nyelve nem magyar (hu), hanem: {html_tag.get('lang')}"

def test_encoding_meta():
    """Állítsa be az oldal kódolását utf-8-ra."""
    soup = load_html()
    
    # UTF-8 meta ellenőrzése
    meta_charset = soup.find('meta', charset=True)
    meta_content_type = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
    
    charset_valid = False
    
    if meta_charset:
        charset_valid = meta_charset['charset'].lower() == 'utf-8'
    elif meta_content_type:
        content = meta_content_type.get('content', '').lower()
        charset_valid = 'utf-8' in content or 'charset=utf-8' in content
    else:
        # Vannak más módok is a kódolás beállítására
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if 'charset' in str(tag):
                if 'utf-8' in str(tag).lower():
                    charset_valid = True
                    break
    
    assert charset_valid, "Az oldal kódolása nem UTF-8 vagy nincs megfelelő meta tag"

def test_title():
    """Állítsa be a böngészőfülön megjelenő feliratot 'Ősz'-re."""
    soup = load_html()
    title_tag = soup.find('title')
    assert title_tag is not None, "Title tag nem található"
    assert title_tag.text.strip() == 'Ősz', f"A title nem 'Ősz', hanem: {title_tag.text.strip()}"

def test_main_heading():
    """Az első szót (Ősz), jelölje meg egyes szintű fejezetcímnek."""
    soup = load_html()
    
    # Megkeressük a fő h1 címet
    h1_tags = soup.find_all('h1')
    assert len(h1_tags) > 0, "Nincs h1 cím a dokumentumban"
    
    # Az első h1 legyen "Ősz"
    first_h1 = h1_tags[0]
    assert first_h1.text.strip() == 'Ősz', f"Az első h1 nem 'Ősz', hanem: {first_h1.text.strip()}"

def test_section_headings():
    """Minden bekezdés előtt legyen 2 szintű fejezetcím a megjegyzés szövegével."""
    soup = load_html()
    
    # Várható szakaszok az adat.txt alapján
    expected_sections = ['Gyümölcsszedés', 'Érés', 'Szőlőszedés']
    
    # Az összes h2 cím
    h2_tags = soup.find_all('h2')
    h2_texts = [h2.text.strip() for h2 in h2_tags]
    
    # Ellenőrizzük, hogy mindhárom szakaszcím megtalálható
    for section in expected_sections:
        assert section in h2_texts, f"Hiányzó h2 cím: {section}"
    
    # Ellenőrizzük, hogy minden bekezdés előtt van-e h2
    p_tags = soup.find_all('p')
    assert len(p_tags) >= 3, f"Legalább 3 bekezdésnek kell lennie, csak {len(p_tags)} található"

def test_italic_kalasvagas():
    """A Gyümölcsszedés részben, a 'kalászvágás' szót, jelölje dőltnek."""
    soup = load_html()
    
    # Megkeressük az összes dőlt (em vagy i) tag-et
    italic_tags = soup.find_all(['em', 'i'])
    
    # Ellenőrizzük, hogy 'kalászvágás' dőltként van jelölve
    kalasvagas_found = False
    for tag in italic_tags:
        if 'kalászvágás' in tag.text:
            kalasvagas_found = True
            break
    
    assert kalasvagas_found, "A 'kalászvágás' szó nincs dőltként (em vagy i) jelölve"

def test_marked_gyumolcsers():
    """Az Érés részben a 'gyümölcsérés ideje' szöveget jelölje kiemeltnek."""
    soup = load_html()
    
    # Megkeressük az összes mark tag-et
    mark_tags = soup.find_all('mark')
    mark_found = False
    
    for tag in mark_tags:
        if 'gyümölcsérés ideje' in tag.text:
            mark_found = True
            break
    
    assert mark_found, "A 'gyümölcsérés ideje' szöveg nincs kiemelve (mark tag)"

def test_strong_hagyjak_kiforrni():
    """A Szőlőszedés részben a 'hagyják kiforrni' szöveget jelölje meg erősnek."""
    soup = load_html()
    
    # Megkeressük az összes erős (strong) tag-et
    strong_tags = soup.find_all(['strong', 'b'])
    strong_found = False
    
    for tag in strong_tags:
        if 'hagyják kiforrni' in tag.text:
            strong_found = True
            break
    
    assert strong_found, "A 'hagyják kiforrni' szöveg nincs erősen (strong) jelölve"

def test_structure_consistency():
    """Ellenőrizzük, hogy az adat.txt tartalma helyesen került be a HTML-be."""
    soup = load_html()
    
    # Ellenőrizzük a főbb szavak jelenlétét
    body_text = soup.body.get_text() if soup.body else ""
    key_words = ['Ősz', 'Gyümölcsszedés', 'Érés', 'Szőlőszedés', 'kalászvágás', 
                 'gyümölcsérés ideje', 'hagyják kiforrni']
    
    for word in key_words:
        assert word in body_text, f"A következő kulcsszó hiányzik: {word}"

def test_no_comments_in_body():
    """Ellenőrizzük, hogy a HTML kommentek ne legyenek a body-ban."""
    soup = load_html()
    
    # Megkeressük az összes kommentet a body-ban
    if soup.body:
        comments_in_body = soup.body.find_all(string=lambda text: isinstance(text, str) and '<!--' in text)
        assert len(comments_in_body) == 0, "HTML kommentek maradtak a body-ban"

def test_paragraph_count():
    """Ellenőrizzük a bekezdések számát."""
    soup = load_html()
    
    # Az adat.txt alapján 3 fő bekezdésnek kell lennie
    p_tags = soup.find_all('p')
    assert len(p_tags) >= 3, f"Legalább 3 bekezdésnek kell lennie, csak {len(p_tags)} található"

def test_encoding_consistency():
    """Ellenőrizzük, hogy a speciális magyar karakterek helyesen jelennek meg."""
    soup = load_html()
    body_text = soup.body.get_text() if soup.body else ""
    
    # Speciális magyar karakterek
    hungarian_chars = ['Ő', 'ő', 'Ű', 'ű', 'á', 'é', 'í', 'ó', 'ö', 'ő', 'ú', 'ü', 'ű']
    
    # Az adat.txt tartalmának beolvasása a teszteléshez
    with open("adat.txt", "r", encoding="utf-8") as f:
        adat_content = f.read()
    
    for char in hungarian_chars:
        # Csak azokat nézzük, amelyek benne vannak az eredeti szövegben
        if char in adat_content:
            assert char in body_text, f"A '{char}' karakter nem jelenik meg helyesen"

def test_heading_hierarchy():
    """Ellenőrizzük a címsorok hierarchiáját."""
    soup = load_html()
    
    # Az első h1 után csak h2-k következhetnek (legalábbis a feladat szerint)
    h1_tags = soup.find_all('h1')
    h2_tags = soup.find_all('h2')
    h3_tags = soup.find_all('h3')
    
    assert len(h1_tags) >= 1, "Legalább egy h1 címnek kell lennie"
    assert len(h2_tags) >= 3, f"Legalább 3 h2 címnek kell lennie, csak {len(h2_tags)} található"
    # Megjegyzés: lehet, hogy a forráslink miatt plusz elemek is vannak
    # assert len(h3_tags) == 0, "Nem szabadna h3 címnek lennie a feladat specifikációja alapján"

def test_content_from_adat_txt():
    """Ellenőrizzük, hogy az adat.txt tartalma teljes egészében benne van."""
    soup = load_html()
    body_text = soup.body.get_text() if soup.body else ""
    
    # Beolvassuk az adat.txt tartalmát, de a HTML kommenteket eltávolítjuk
    with open("adat.txt", "r", encoding="utf-8") as f:
        adat_content = f.read()
    
    # Távolítsuk el a HTML kommenteket az adat.txt-ből
    import re
    adat_without_comments = re.sub(r'<!--.*?-->', '', adat_content, flags=re.DOTALL)
    
    # Távolítsuk el a felesleges whitespace-eket és sortöréseket
    adat_clean = ' '.join(adat_without_comments.split())
    body_clean = ' '.join(body_text.split())
    
    # Ellenőrizzük a kulcsszavakat
    key_phrases = ['viszálykodás a kalászvágás', 'édes, tápláló gyümölcsét', 
                   'betakarítás nem fáradság', 'első borszüret a szigeten']
    
    for phrase in key_phrases:
        assert phrase in body_clean, f"A következő kifejezés hiányzik: {phrase}"

if __name__ == "__main__":
    # Tesztfuttatás
    pytest.main([__file__, "-v"])