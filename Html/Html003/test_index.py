import pytest
from bs4 import BeautifulSoup
import re

def test_1_aix_txt_tartalom_beillesztese():
    """1. A aix.txt állomány tartalmát illessze be a HTML oldal törzs részébe"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_text = soup.get_text()
    
    key_phrases = [
        "Az AIX az Advanced Interactive eXecutive rövidítése",
        "Az AIX egy kereskedelmi Unix operációs rendszer",
        "az IBM fejleszt",
        "Az AIX a UNIX System V rendszeren alapszik",
        "Támogatott platformok:",
        "IBM RS/6000",
        "POWER",
        "PowerPC",
        "IBM System i",
        "System/370",
        "PS/2",
        "Apple Network Server"
    ]
    
    for phrase in key_phrases:
        assert phrase in html_text, f"Hiányzik: {phrase}"
    
    print("✅ 1. Szöveg tartalom beillesztve")

def test_2_magyar_nyelv():
    """2. Állítsa be az oldalt magyar nyelvűre"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_tag = soup.find("html")
        
        assert html_tag is not None, "Nincs html tag"
        assert html_tag.get("lang") == "hu", f"Nincs lang='hu', hanem: {html_tag.get('lang')}"
    
    print("✅ 2. Magyar nyelv beállítva")

def test_3_bongeszoful_cim():
    """3. Állítsa be, hogy a böngészőfülön a „AIX” felirat jelenjen meg"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        title_tag = soup.find("title")
        
        assert title_tag is not None, "Nincs title tag"
        assert title_tag.text == "AIX", f"Title nem 'AIX', hanem: '{title_tag.text}'"
    
    print("✅ 3. Böngészőfül cím beállítva")

def test_4_egyes_szintu_cim():
    """4. Állítson be a szöveg előtt egyes szintű fejezetcímet, „AIX” tartalommal"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h1_tags = soup.find_all("h1")
        
        assert len(h1_tags) >= 1, "Nincs H1 cím"
        assert h1_tags[0].text.strip() == "AIX", f"H1 nem 'AIX', hanem: '{h1_tags[0].text}'"
    
    print("✅ 4. H1 cím beállítva")

def test_5_harom_bekezdes():
    """5. A három bekezdést jelölje HTML elemmel, bekezdésnek"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        p_tags = soup.find_all("p")
        
        assert len(p_tags) == 3, f"Nincs 3 bekezdés, hanem: {len(p_tags)}"
    
    print("✅ 5. 3 bekezdés létrehozva")

def test_6_kettes_szintu_cimek():
    """6. A bekezdések a következő címeket kapják, 2-s fejezetcímmel"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h2_tags = soup.find_all("h2")
        
        expected_titles = ["Egy", "Kettő", "Három"]
        
        assert len(h2_tags) == 3, f"Nincs 3 H2 cím, hanem: {len(h2_tags)}"
        
        for i, (h2, expected) in enumerate(zip(h2_tags, expected_titles)):
            assert h2.text.strip() == expected, f"H2[{i}] nem '{expected}', hanem: '{h2.text}'"
    
    print("✅ 6. H2 címek beállítva")

def test_7_advanced_interactive_executive_felkover():
    """7. Az Advanced Interactive eXecutive szavakat, együtt jelölje félkövérnek"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_content = str(soup)
        
        # Ellenőrizzük, hogy van <strong> vagy <b> tag a teljes szöveg körül
        found = False
        
        # 1. Keressünk strong tag-eket
        strong_tags = soup.find_all(["strong", "b"])
        for tag in strong_tags:
            if "Advanced Interactive eXecutive" in tag.text:
                found = True
                break
        
        # 2. VAGY keressünk regex-szel
        if not found:
            pattern = r'<strong>.*?Advanced Interactive eXecutive.*?</strong>'
            if re.search(pattern, html_content, re.IGNORECASE | re.DOTALL):
                found = True
        
        # 3. Ellenőrizzük, hogy az első bekezdésben van-e
        if not found and len(soup.find_all("p")) > 0:
            first_p = str(soup.find_all("p")[0])
            if "Advanced Interactive eXecutive" in first_p and ("<strong>" in first_p or "<b>" in first_p):
                found = True
        
        assert found, "Nincs 'Advanced Interactive eXecutive' félkövérként jelölve"
    
    print("✅ 7. 'Advanced Interactive eXecutive' félkövérként jelölve")

def test_8_aix_mindenhol_kiemelt():
    """8. Az AIX szó, mindenhol legyen kiemeltnek jelölve"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_content = str(soup)
        
        # Ellenőrizzük az első bekezdést
        p_tags = soup.find_all("p")
        assert len(p_tags) >= 1, "Nincs bekezdés"
        
        # Az első bekezdésben ellenőrizzük minden AIX-t
        first_p = str(p_tags[0])
        
        # Számoljuk meg, hányszor szerepel AIX az első bekezdésben
        aix_occurrences = first_p.upper().count("AIX")
        
        # Számoljuk meg, hányszor van kiemelve
        aix_emphasized = 0
        
        # Ellenőrizzük strong tag-eket
        strong_tags = soup.find_all(["strong", "b"])
        for tag in strong_tags:
            if "AIX" in tag.text.upper():
                aix_emphasized += 1
        
        # Megjegyzés: a feladat szerint "mindenhol legyen kiemeltnek jelölve"
        # De a lista részt nem kell kiemelni, csak a szövegrészekben
        assert aix_emphasized >= 3, f"Az AIX nincs elég kiemelve (csak {aix_emphasized} helyen)"
        
        # Ellenőrizzük, hogy az első bekezdés első AIX-e kiemelve van-e
        assert "<strong>AIX</strong>" in first_p or "<b>AIX</b>" in first_p, \
               "Az első AIX nincs kiemelve az első bekezdésben"
    
    print("✅ 8. AIX szó kiemelve")

def test_9_megjegyzes_nev_datum():
    """9. A HTML forráskódjában, megjegyzésbe, írja, a nevét és az aktuális dátumot"""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ellenőrizzük, hogy van HTML komment
    comments = re.findall(r'<!--.*?-->', content, re.DOTALL)
    assert len(comments) > 0, "Nincs HTML komment"
    
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

def run_all_tests():
    """Az összes teszt futtatása"""
    tests = [
        test_1_aix_txt_tartalom_beillesztese,
        test_2_magyar_nyelv,
        test_3_bongeszoful_cim,
        test_4_egyes_szintu_cim,
        test_5_harom_bekezdes,
        test_6_kettes_szintu_cimek,
        test_7_advanced_interactive_executive_felkover,
        test_8_aix_mindenhol_kiemelt,
        test_9_megjegyzes_nev_datum
    ]
    
    passed = 0
    failed = 0
    
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
    
    print("\n" + "="*50)
    print(f"ÖSSZEFOGLALÓ: {passed} sikeres, {failed} sikertelen")
    print("="*50)
    
    return failed == 0

if __name__ == "__main__":
    if run_all_tests():
        print("🎉 Összes teszt sikeres!")
    else:
        print("❌ Van hibás teszt!")