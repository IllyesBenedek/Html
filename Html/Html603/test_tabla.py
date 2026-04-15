import pytest
import os

def hiba(msg, feladat_szam):
    pytest.fail(f"\n[FELADAT 0603-{feladat_szam}. HIBA]: {msg}")

# 1. JAVÍTÁS: TR tagek (t -> tr)
def test_javitas_01():
    if not os.path.exists("tabla.html"): hiba("A tabla.html nem található!", 1)
    with open("tabla.html", 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Szigorú keresés: ha a "t" tag önmagában (vagy rosszul) szerepel, az hiba
        # Regex nélkül is működik: keresünk olyan mintákat, amik "t" tag-re utalnak, 
        # de nem a helyes "tr" vagy "td" részei.
        if "<t " in content or "<t>" in content or "</t>" in content:
            # Itt most kivételt teszünk a <td> és <tr>-ekkel
            # Ha bármilyen "t" tag maradt, ami nem <td>, <tr>, </td> vagy </tr>
            clean_content = content.replace("<tr>", "").replace("</tr>", "").replace("<td>", "").replace("</td>", "")
            if "<t" in clean_content or "</t" in clean_content:
                hiba("Hibás tag maradt a kódban: 't' helyett 'tr' vagy 'td' kell!", 1)


# 2. JAVÍTÁS: TD tagek (</t> -> </td>)
def test_javitas_02():
    with open("tabla.html", 'r', encoding='utf-8') as f:
        content = f.read()
        if "</t>" in content:
            hiba("A cellák záró tagjei el vannak írva (</t> helyett </td> kell)!", 2)

# 3. JAVÍTÁS: Struktúra (5 sor)
def test_javitas_03():
    with open("tabla.html", 'r', encoding='utf-8') as f:
        content = f.read()
        # Megszámoljuk a 'tr' nyitó tageket
        darab = content.count("<tr")
        if darab != 5:
            hiba(f"5 darab <tr> táblázatsort vártam, de csak {darab}-t találtam.", 3)
