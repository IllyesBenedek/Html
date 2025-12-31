import pytest
from bs4 import BeautifulSoup
import re

def test_1_weboldal_letezik():
    """1. Készítsen egy weboldalt had.html néven"""
    try:
        with open("had.html", "r", encoding="utf-8") as f:
            assert True
    except FileNotFoundError:
        assert False, "A had.html fájl nem létezik"
    
    print("✅ 1. Weboldal létrehozva (had.html)")

def test_2_magyar_nyelv():
    """2. Állítsa be a weboldal nyelvét magyarra"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_tag = soup.find("html")
        
        assert html_tag is not None, "Nincs html tag"
        assert html_tag.get("lang") == "hu", f"Nincs lang='hu', hanem: {html_tag.get('lang')}"
    
    print("✅ 2. Magyar nyelv beállítva")

def test_3_utf8_kodolas():
    """3. Oldal kódolása legyen utf-8"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        meta_charset = soup.find("meta", charset=True)
        
        assert meta_charset is not None, "Nincs charset meta tag"
        assert meta_charset.get("charset").lower() == "utf-8", f"Nincs utf-8, hanem: {meta_charset.get('charset')}"
    
    print("✅ 3. UTF-8 kódolás beállítva")

def test_4_bongeszoful_cim():
    """4. A böngésző fülön a „Had” szó jelenjen meg"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        title_tag = soup.find("title")
        
        assert title_tag is not None, "Nincs title tag"
        assert title_tag.text == "Had", f"Title nem 'Had', hanem: '{title_tag.text}'"
    
    print("✅ 4. Böngészőfül cím: 'Had'")

def test_5_szoveg_beillesztese():
    """5. A fenti szöveget illessze be a weblap törzs részére"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_text = soup.get_text()
    
    key_phrases = [
        "indigótelepítvényt találtak megrohanni",
        "Blackfort-ház tulajdona volt",
        "afgánok jártak",
        "vad szomszédok",
        "legtekintélyesebb gyárházak",
        "Calcuttából a Hindukus felé",
        "négy zászlóalj vadász",
        "lovas karabinier",
        "utászszázadnál voltam én főhadnagy"
    ]
    
    for phrase in key_phrases:
        assert phrase in html_text, f"Hiányzik: {phrase}"
    
    print("✅ 5. Szöveg beillesztve")

def test_6_h2_cimek():
    """6. Van három bekezdés külön külön címekkel: Telep, Szomszédok, Hadcsapat"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h2_tags = soup.find_all("h2")
        
        expected_titles = ["Telep", "Szomszédok", "Hadcsapat"]
        
        assert len(h2_tags) == 3, f"Nincs 3 H2 cím, hanem: {len(h2_tags)}"
        
        for i, (h2, expected) in enumerate(zip(h2_tags, expected_titles)):
            assert h2.text.strip() == expected, f"H2[{i}] nem '{expected}', hanem: '{h2.text}'"
    
    print("✅ 6. 3 H2 cím (Telep, Szomszédok, Hadcsapat)")

def test_7_h1_cim():
    """7. A weblap tetejére a következő címet állítsa be, egyes szintű fejezetcímmé: A láthatatlan csillag"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h1_tags = soup.find_all("h1")
        
        assert len(h1_tags) >= 1, "Nincs H1 cím"
        assert h1_tags[0].text.strip() == "A láthatatlan csillag", f"H1 nem 'A láthatatlan csillag', hanem: '{h1_tags[0].text}'"
    
    print("✅ 7. H1 cím: 'A láthatatlan csillag'")

def test_8_p_bekezdesek():
    """8. A cím alatti bekezdéseket tegye p elemek közzé"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        p_tags = soup.find_all("p")
        
        assert len(p_tags) == 3, f"Nincs 3 bekezdés, hanem: {len(p_tags)}"
        
        # Ellenőrizzük, hogy mindhárom p tag tartalmaz szöveget
        for i, p in enumerate(p_tags):
            assert len(p.text.strip()) > 0, f"A {i+1}. bekezdés üres"
    
    print("✅ 8. 3 bekezdés (p elemek)")

def test_9_megjegyzes_nev_datum():
    """9. A weblap tetején legyen megjegyzésben a neve és a készítés dátuma"""
    with open("had.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ellenőrizzük, hogy van HTML komment
    comments = re.findall(r'<!--.*?-->', content, re.DOTALL)
    assert len(comments) > 0, "Nincs HTML komment"
    
    # Ellenőrizzük, hogy a komment a body elején van
    body_start = content.find("<body>")
    comment_start = content.find("<!--", body_start)
    comment_end = content.find("-->", comment_start)
    
    assert comment_start > body_start and comment_end > comment_start, "A komment nincs a body elején"
    
    # Ellenőrizzük, hogy van név és dátum
    comment_text = comments[0]
    
    # Név ellenőrzése (legalább 2 karakter)
    assert re.search(r'[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{2,}', comment_text), "Nincs név a kommentben"
    
    # Dátum ellenőrzése (valamilyen dátum formátum)
    date_patterns = [
        r'\d{4}\.\d{1,2}\.\d{1,2}',  # 2025.12.30
        r'\d{4}-\d{1,2}-\d{1,2}',     # 2025-12-30
        r'\d{4}/\d{1,2}/\d{1,2}',     # 2025/12/30
    ]
    
    has_date = any(re.search(pattern, comment_text) for pattern in date_patterns)
    assert has_date, "Nincs dátum a kommentben"
    
    print("✅ 9. Megjegyzés névvel és dátummal")

def test_10_struktura_ellenorzes():
    """10. Általános HTML struktúra ellenőrzés"""
    with open("had.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    # Alapvető HTML elemek
    assert soup.find("html") is not None
    assert soup.find("head") is not None
    assert soup.find("body") is not None
    assert soup.find("title") is not None
    assert soup.find("h1") is not None
    assert len(soup.find_all("h2")) == 3
    assert len(soup.find_all("p")) == 3
    
    print("✅ 10. HTML struktúra helyes")

def test_11_sorrend_ellenorzes():
    """11. Ellenőrizzük az elemek sorrendjét"""
    with open("had.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ellenőrizzük a sorrendet: <body> → komment → <h1> → <h2> → <p> → <h2> → <p> stb.
    body_pos = content.find("<body>")
    comment_pos = content.find("<!--", body_pos)
    h1_pos = content.find("<h1>", comment_pos)
    h2_1_pos = content.find("<h2>", h1_pos)
    p_1_pos = content.find("<p>", h2_1_pos)
    h2_2_pos = content.find("<h2>", p_1_pos)
    p_2_pos = content.find("<p>", h2_2_pos)
    h2_3_pos = content.find("<h2>", p_2_pos)
    p_3_pos = content.find("<p>", h2_3_pos)
    
    # Ellenőrizzük, hogy minden pozíció megtalálható és helyes sorrendben van
    positions = [body_pos, comment_pos, h1_pos, h2_1_pos, p_1_pos, h2_2_pos, p_2_pos, h2_3_pos, p_3_pos]
    for i in range(len(positions) - 1):
        if positions[i] != -1 and positions[i+1] != -1:
            assert positions[i] < positions[i+1], f"Hibás sorrend: {i}. elem után nem következik a {i+1}. elem"
    
    print("✅ 11. Elemek helyes sorrendben")

def run_all_tests():
    """Az összes teszt futtatása"""
    tests = [
        test_1_weboldal_letezik,
        test_2_magyar_nyelv,
        test_3_utf8_kodolas,
        test_4_bongeszoful_cim,
        test_5_szoveg_beillesztese,
        test_6_h2_cimek,
        test_7_h1_cim,
        test_8_p_bekezdesek,
        test_9_megjegyzes_nev_datum,
        test_10_struktura_ellenorzes,
        test_11_sorrend_ellenorzes
    ]
    
    passed = 0
    failed = 0
    
    print("🔬 TESZTEK FUTTATÁSA")
    print("=" * 50)
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  {test.__name__}: Váratlan hiba: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 ÖSSZEFOGLALÓ: {passed} sikeres, {failed} sikertelen")
    print("=" * 50)
    
    if failed == 0:
        print("🎉 ÖSSZES TESZT SIKERES!")
    else:
        print("❌ VAN HIBA A TESZTEKBEN!")
    
    return failed == 0

if __name__ == "__main__":
    run_all_tests()