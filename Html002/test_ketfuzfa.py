import pytest
from bs4 import BeautifulSoup
import re
from datetime import datetime

def test_1_szoveg_tartalom_beillesztese():
    """1. A adat.txt állomány tartalmát illessze be a HTML oldal törzs részébe"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_text = soup.get_text()
    
    # Ellenőrizzük, hogy tartalmazza a szöveg.txt kulcsszavait
    key_phrases = [
        "Öt-hatszáz fogadott fia",
        "tisztes matrónának",
        "nagyenyedi kollégium",
        "Tordai Szabó Gerzson",
        "bevette magát iszonyú fóliánsai közé",
        "csillagászat és mechanika"
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
    """3. Állítsa be, hogy a böngészőfülön a „Két fűzfa” felirat jelenjen meg"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        title_tag = soup.find("title")
        
        assert title_tag is not None, "Nincs title tag"
        assert title_tag.text == "Két fűzfa", f"Title nem 'Két fűzfa', hanem: '{title_tag.text}'"
    
    print("✅ 3. Böngészőfül cím beállítva")

def test_4_egyes_szintu_cim():
    """4. Állítson be a szöveg előtt egyes szintű fejezetcímet, „Két fűzfa” tartalommal"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h1_tags = soup.find_all("h1")
        
        assert len(h1_tags) >= 1, "Nincs H1 cím"
        assert h1_tags[0].text.strip() == "Két fűzfa", f"H1 nem 'Két fűzfa', hanem: '{h1_tags[0].text}'"
    
    print("✅ 4. H1 cím beállítva")

def test_5_harom_bekezdes():
    """5. A három bekezdést jelölje HTML elemmel, bekezdésnek"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        p_tags = soup.find_all("p")
        
        assert len(p_tags) == 3, f"Nincs 3 bekezdés, hanem: {len(p_tags)}"
    
    print("✅ 5. 3 bekezdés létrehozva")

def test_6_kettes_szintu_cimek():
    """6. A bekezdéseknek a következő címet adja, kettes fejezetcímmel"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h2_tags = soup.find_all("h2")
        
        expected_titles = ["A jövedelem", "A kollégium", "Az orákulum"]
        
        assert len(h2_tags) == 3, f"Nincs 3 H2 cím, hanem: {len(h2_tags)}"
        
        for i, (h2, expected) in enumerate(zip(h2_tags, expected_titles)):
            assert h2.text.strip() == expected, f"H2[{i}] nem '{expected}', hanem: '{h2.text}'"
    
    print("✅ 6. H2 címek beállítva")

def test_7_kiemelt_szoveg():
    """7. A „bevette magát” szöveget, a harmadik bekezdésben, jelölje meg kiemeltnek"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        p_tags = soup.find_all("p")
        
        assert len(p_tags) >= 3, "Nincs harmadik bekezdés"
        
        third_p = p_tags[2]
        strong_tags = third_p.find_all(["strong", "b"])
        
        found = False
        for tag in strong_tags:
            if "bevette magát" in tag.text:
                found = True
                break
        
        assert found, "Nincs 'bevette magát' kiemelve a harmadik bekezdésben"
    
    print("✅ 7. 'bevette magát' kiemelve")

def test_8_dolt_szoveg():
    """8. A második bekezdésben a „időszerint” szót, jelölje meg dőlt szövegnek"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        p_tags = soup.find_all("p")
        
        assert len(p_tags) >= 2, "Nincs második bekezdés"
        
        second_p = p_tags[1]
        em_tags = second_p.find_all(["i", "em"])
        
        found = False
        for tag in em_tags:
            if "időszerint" in tag.text:
                found = True
                break
        
        assert found, "Nincs 'időszerint' dőltté téve a második bekezdésben"
    
    print("✅ 8. 'időszerint' dőltté téve")

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
        r'\d{4}\.\d{1,2}\.\d{1,2}',  # 2024.12.29
        r'\d{4}-\d{1,2}-\d{1,2}',     # 2024-12-29
        r'\d{4}/\d{1,2}/\d{1,2}',     # 2024/12/29
    ]
    
    has_date = any(re.search(pattern, comment_text) for pattern in date_patterns)
    assert has_date, "Nincs dátum a kommentben"
    
    print("✅ 9. Megjegyzés névvel és dátummal")

def test_html_structure():
    """Összesített ellenőrzés"""
    with open("index.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    # Ellenőrizzük az alapvető HTML struktúrát
    assert soup.find("html") is not None
    assert soup.find("head") is not None
    assert soup.find("body") is not None
    
    print("✅ HTML struktúra helyes")

def run_all_tests():
    """Az összes teszt futtatása"""
    tests = [
        test_1_szoveg_tartalom_beillesztese,
        test_2_magyar_nyelv,
        test_3_bongeszoful_cim,
        test_4_egyes_szintu_cim,
        test_5_harom_bekezdes,
        test_6_kettes_szintu_cimek,
        test_7_kiemelt_szoveg,
        test_8_dolt_szoveg,
        test_9_megjegyzes_nev_datum,
        test_html_structure
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
    # Ha közvetlenül futtatod
    if run_all_tests():
        print("🎉 Összes teszt sikeres!")
    else:
        print("❌ Van hibás teszt!")