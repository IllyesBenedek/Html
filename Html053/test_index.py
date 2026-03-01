"""
Feladat 053 - HTML szerkesztés és tesztelés
"""

import re
from pathlib import Path


def test_001_fajl_letezese():
    """Az index.html fájl létezik"""
    assert Path("index.html").exists(), "Az index.html fájl nem létezik!"


def test_002_html_struktur():
    """Alapvető HTML struktúra ellenőrzése"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # DOCTYPE ellenőrzés
    assert "<!DOCTYPE html>" in content, "Hiányzik a DOCTYPE!"
    
    # HTML struktúra
    assert "<html" in content, "Hiányzik az <html> tag!"
    assert "</html>" in content, "Hiányzik a </html> tag!"
    assert "<head>" in content, "Hiányzik a <head> tag!"
    assert "</head>" in content, "Hiányzik a </head> tag!"
    assert "<body>" in content, "Hiányzik a <body> tag!"
    assert "</body>" in content, "Hiányzik a </body> tag!"


def test_003_nyelv_beallitas():
    """Magyar nyelv beállítása"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ellenőrizd, hogy a nyelv magyarra van-e állítva
    assert 'lang="hu"' in content or "lang='hu'" in content, \
        "A nyelv nincs beállítva magyarra (hu)!"


def test_004_charset_utf8():
    """UTF-8 karakterkódolás"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # UTF-8 charset ellenőrzése
    charset_patterns = [
        'charset="UTF-8"',
        'charset="utf-8"',
        "charset='UTF-8'",
        "charset='utf-8'"
    ]
    
    assert any(pattern in content for pattern in charset_patterns), \
        "Hiányzik a UTF-8 karakterkódolás!"


def test_005_title_fdisk():
    """Címsorban az fdisk szó"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # <title> tag ellenőrzése és tartalma
    title_match = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
    assert title_match is not None, "Hiányzik a <title> tag!"
    
    title_content = title_match.group(1).strip()
    assert "fdisk" in title_content.lower(), \
        f"A title nem tartalmazza az 'fdisk' szót! Title: '{title_content}'"


def test_006_fdisk_h1_cim():
    """Egyes szintű címsor (h1) az fdisk-hez"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # H1 cím ellenőrzése
    h1_match = re.search(r"<h1>(.*?)</h1>", content, re.DOTALL | re.IGNORECASE)
    assert h1_match is not None, "Hiányzik az <h1> cím!"
    
    h1_content = h1_match.group(1).strip()
    assert "fdisk" in h1_content.lower(), \
        f"Az h1 cím nem tartalmazza az 'fdisk' szót! h1: '{h1_content}'"


def test_007_fdisk_h2_cim():
    """Kettes szintű fejezetcím az 'az fdisk program' szöveggel"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # H2 cím ellenőrzése
    h2_matches = re.findall(r"<h2>(.*?)</h2>", content, re.DOTALL | re.IGNORECASE)
    assert len(h2_matches) > 0, "Hiányzik az <h2> cím!"
    
    # Ellenőrizd, hogy valamelyik h2 tartalmazza a szöveget
    h2_contains_text = any("az fdisk program" in h2.lower().strip() for h2 in h2_matches)
    assert h2_contains_text, \
        f"Nincs 'az fdisk program' szövegű h2 cím! h2-ek: {h2_matches}"


def test_008_elso_bekezdes():
    """Első bekezdés az 'az fdisk program' után"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # <p> tag ellenőrzése
    p_matches = re.findall(r"<p>(.*?)</p>", content, re.DOTALL | re.IGNORECASE)
    assert len(p_matches) >= 2, f"Kevesebb mint 2 bekezdés van! p-ek: {len(p_matches)}"
    
    # Ellenőrizd, hogy az első bekezdés tartalmazza-e az "Az fdisk egy" kezdetű szöveget
    first_para_ok = False
    for p in p_matches:
        if "Az fdisk egy párbeszéd" in p:
            first_para_ok = True
            break
    
    assert first_para_ok, "Hiányzik az első bekezdés az 'Az fdisk egy párbeszéd' szöveggel!"


def test_009_kiemelt_bsd_szoveg():
    """BSD szöveg kiemelése a bekezdésben"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # <strong> tag ellenőrzése
    strong_matches = re.findall(r"<strong>(.*?)</strong>", content, re.DOTALL | re.IGNORECASE)
    assert len(strong_matches) > 0, "Nincs <strong> tag a BSD kiemeléséhez!"
    
    # Ellenőrizd, hogy valamelyik <strong> tartalmazza-e a BSD szöveget
    bsd_in_strong = any("BSD" in s.upper() for s in strong_matches)
    assert bsd_in_strong, \
        f"A BSD szöveg nincs kiemelve <strong> tag-ben! strong-ok: {strong_matches}"
    
    # Ellenőrizd, hogy a BSD a bekezdésen belül van-e
    p_strong_pattern = r"<p>.*?BSD.*?</p>"
    assert re.search(p_strong_pattern, content, re.DOTALL | re.IGNORECASE) is not None, \
        "A BSD szöveg nincs bekezdésen belül kiemelve!"


def test_010_kapcsolok_bekezdes():
    """Kapcsolók bekezdése"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Keressük a "kapcsolói" szót tartalmazó bekezdést
    kapcsolok_pattern = r"<p>[^<]*?kapcsolói[^<]*?</p>"
    kapcsolok_match = re.search(kapcsolok_pattern, content, re.DOTALL | re.IGNORECASE)
    
    assert kapcsolok_match is not None, \
        "Hiányzik a 'kapcsolói' szót tartalmazó bekezdés!"


def test_011_szamozott_lista():
    """Számozott lista a kapcsolóknak"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # <ol> tag ellenőrzése
    assert "<ol>" in content and "</ol>" in content, "Hiányzik a számozott lista (<ol>)!"
    
    # <li> tag-ek ellenőrzése (minimum 10)
    li_matches = re.findall(r"<li>(.*?)</li>", content, re.DOTALL | re.IGNORECASE)
    assert len(li_matches) >= 10, \
        f"Kevesebb mint 10 listaelem (<li>) van! Jelenleg: {len(li_matches)}"
    
    # Ellenőrizd, hogy a lista tartalmazza-e a -b kapcsolót
    first_li = li_matches[0].strip() if li_matches else ""
    assert "-b" in first_li or "--sector-size" in first_li, \
        f"Az első listaelem nem tartalmazza a -b kapcsolót! Első li: '{first_li}'"
    
    # Ellenőrizd, hogy a lista tartalmazza-e a -u kapcsolót
    last_li = li_matches[-1].strip() if li_matches else ""
    assert "-u" in last_li or "--units" in last_li, \
        f"Az utolsó listaelem nem tartalmazza a -u kapcsolót! Utolsó li: '{last_li}'"


def test_012_megjegyzes_felso_reszen():
    """Megjegyzés a tetején (név, osztály, dátum)"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Megjegyzés keresése <!-- -->
    comments = re.findall(r"<!--(.*?)-->", content, re.DOTALL)
    assert len(comments) >= 1, "Nincsenek megjegyzések a fájlban!"
    
    # Keressük az első, a <body> után található kommentet
    body_start = content.find("<body>")
    if body_start != -1:
        body_content = content[body_start:]
        body_comments = re.findall(r"<!--(.*?)-->", body_content, re.DOTALL)
        
        if body_comments:
            # Az első komment a testben (elvileg a név, osztály, dátum)
            first_body_comment = body_comments[0].strip()
            
            # Ellenőrizd, hogy tartalmaz-e vesszőt (név, osztály elválasztására)
            assert "," in first_body_comment, \
                f"Az első komment a testben nem tartalmaz vesszőt (név, osztály elválasztás)! Komment: '{first_body_comment}'"
            
            # Ellenőrizd a hosszt (minimális információ)
            assert len(first_body_comment) > 5, \
                f"Az első komment túl rövid a név, osztály, dátum tárolásához! Komment: '{first_body_comment}'"
            
            print(f"  ✓ Felül található komment: {first_body_comment[:50]}...")


def test_013_osszes_kovetelmeny():
    """Összes követelmény együttes ellenőrzése"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Összefoglaló ellenőrzések
    ellenorzesek = [
        ('lang="hu"', "Nyelv beállítás"),
        ('charset="UTF-8"', "Karakterkódolás"),
        ('<title>fdisk</title>', "Címsor"),
        ('<h1>fdisk</h1>', "H1 cím"),
        ('<h2>az fdisk program</h2>', "H2 cím"),
        ('<strong>BSD', "BSD kiemelés"),
        ('<ol>', "Számozott lista"),
    ]
    
    sikertelenek = []
    for pattern, leiras in ellenorzesek:
        if pattern not in content and pattern.lower() not in content.lower():
            sikertelenek.append(leiras)
    
    assert len(sikertelenek) == 0, \
        f"Hiányzó elemek: {', '.join(sikertelenek)}"


if __name__ == "__main__":
    """Ha közvetlenül futtatjuk a fájlt"""
    import sys
    
    print("=" * 60)
    print("Feladat 053 - HTML tesztelés")
    print("=" * 60)
    
    # Futtasd az összes tesztet
    osszes_teszt = [f for f in globals().keys() if f.startswith("test_")]
    
    sikeresek = 0
    osszes = len(osszes_teszt)
    
    for teszt_nev in osszes_teszt:
        teszt_fv = globals()[teszt_nev]
        
        try:
            teszt_fv()
            print(f"✅ {teszt_nev}: Sikeres")
            sikeresek += 1
        except AssertionError as e:
            print(f"❌ {teszt_nev}: Hiba - {e}")
        except Exception as e:
            print(f"⚠️  {teszt_nev}: Váratlan hiba - {type(e).__name__}: {e}")
    
    print("=" * 60)
    print(f"Eredmény: {sikeresek}/{osszes} teszt sikeres")
    
    if sikeresek == osszes:
        print("🎉 Összes teszt sikeresen lefutott!")
        sys.exit(0)
    else:
        print("⚠️  Néhány teszt nem futott le sikeresen!")
        sys.exit(1)