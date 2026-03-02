import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def soup():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return BeautifulSoup(f.read(), "html.parser")
    except FileNotFoundError:
        pytest.fail("Az index.html fájl nem található!")

# 1. feladat: Magyar nyelv beállítása
def test_feladat_1_nyelv(soup):
    assert soup.html.get("lang") == "hu", "1. hiba: A weboldal nyelve nem magyar (lang='hu')!"

# 2. feladat: Böngésző fül szövege
def test_feladat_2_title(soup):
    assert soup.title is not None and soup.title.string == "Solaris", "2. hiba: A böngésző fülén nem a 'Solaris' szöveg szerepel!"

# 3. feladat: UTF-8 kódolás
def test_feladat_3_utf8(soup):
    meta = soup.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8", "3. hiba: Az utf-8 kódolás nincs beállítva!"

# 4. feladat: Egyes szintű fejezetcím (h1)
def test_feladat_4_h1(soup):
    h1 = soup.find("h1")
    assert h1 is not None, "4. hiba: Hiányzik az egyes szintű fejezetcím (h1)!"
    assert h1.text.strip() == "A Solaris", "4/a hiba: Az egyes szintű fejezetcím tartalma nem 'A Solaris'!"

# 5. feladat: Bekezdések jelölése
def test_feladat_5_p_tag(soup):
    p_tags = soup.find_all("p")
    assert len(p_tags) >= 4, "5/a hiba: Nem minden bekezdés van <p> taggel jelölve!"

# 6. feladat: Kettes szintű fejezetcímek (h2)
def test_feladat_6_h2_cimek(soup):
    h2_tags = soup.find_all("h2")
    elvart_szovegek = ["A Solaris", "Korai verziók", "Használat", "Megnyitás"]
    aktulis_szovegek = [h.text.strip() for h in h2_tags]
    
    assert len(h2_tags) == 4, "6. hiba: Nem 4 darab kettes szintű fejezetcím van!"
    for szoveg in elvart_szovegek:
        assert szoveg in aktulis_szovegek, f"6/a hiba: A(z) '{szoveg}' kettes szintű fejezetcím hiányzik!"

# 7. feladat: Kép beszúrása az első bekezdés után
def test_feladat_7_kep_helye(soup):
    first_p = soup.find("p")
    assert first_p is not None, "7. hiba: Nincs bekezdés, ami után be lehetne szúrni a képet!"
    img = soup.find("img")
    assert img is not None, "7. hiba: A 'solarisLogo.png' kép nincs beszúrva!"
    assert img["src"] == "solarisLogo.png", "7. hiba: A kép forrása nem 'solarisLogo.png'!"

# 8. feladat: Kép alt attribútuma (Solaris Logo)
def test_feladat_8_kep_alt(soup):
    img = soup.find("img")
    assert img is not None and img.get("alt") == "Solaris Logo", "8/a/I hiba: A kép alt szövege nem 'Solaris Logo'!"

# 9. feladat: Kép title attribútuma (Egér ráhúzáskor megjelenő szöveg)
def test_feladat_9_kep_title(soup):
    img = soup.find("img")
    elvart_title = "A Solaris operációs rendszer logója"
    assert img is not None and img.get("title") == elvart_title, "9/a/I hiba: A kép title szövege nem megfelelő!"