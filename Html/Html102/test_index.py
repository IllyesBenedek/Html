import pytest
from bs4 import BeautifulSoup

@pytest.fixture
def dom():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return BeautifulSoup(f, "html.parser")
    except FileNotFoundError:
        pytest.fail("Az index.html fájl nem található!")

def test_feladat_01_magyar_nyelv(dom):
    """1. Feladat: Magyar nyelv ellenőrzése"""
    assert dom.html.get("lang") == "hu", "A weboldal nyelve nem 'hu'!"

def test_feladat_02_halozat_cim(dom):
    """2. Feladat: Böngésző fül címe"""
    assert dom.title.string.strip() == "Hálózat", "A title nem 'Hálózat'!"

def test_feladat_03_utf8(dom):
    """3. Feladat: UTF-8 kódolás"""
    meta = dom.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8", "Nincs beállítva az utf-8 kódolás!"

def test_feladat_04_h1_fejezetcim(dom):
    """4. Feladat: 'A hálózat' h1 cím"""
    h1 = dom.find("h1")
    assert h1 and h1.text.strip() == "A hálózat", "Hiányzik vagy hibás az <h1> cím!"

def test_feladat_05_figure1_helye(dom):
    """5. Feladat: Figure 1 kép a LAN bekezdésben"""
    # Megkeressük a 'Helyi hálózatok' címet, majd az utána lévő bekezdést
    h2 = dom.find("h2", string=lambda x: x and "Helyi hálózatok" in x)
    assert h2, "Nincs 'Helyi hálózatok' h2 fejezetcím!"
    p = h2.find_next("p")
    imgs = p.find_all("img")
    assert len(imgs) > 0, "Nincs kép a Helyi hálózatok bekezdésben!"
    assert "fig1" in imgs[-1]["src"].lower(), "A bekezdés végén nem a Figure 1 szerepel!"

def test_feladat_06_lista_kepek(dom):
    """6. Feladat: Figure 2-6 képek a lista elemek végén"""
    li_elements = dom.find_all("li")
    assert len(li_elements) == 5, "Nincs meg az 5 lista elem!"
    for i, li in enumerate(li_elements):
        assert li.find("img"), f"A(z) {i+1}. lista elemben nincs kép!"

def test_feladat_07_bekezdesek_es_lista(dom):
    """7. Feladat: Bekezdések és a lista beágyazása"""
    # A lista a 'Szimbólumok' bekezdésen belül kell legyen
    h2 = dom.find("h2", string=lambda x: x and "Szimbólumok" in x)
    p = h2.find_next("p")
    assert p.name == "p", "A Szimbólumok után nem bekezdés áll!"
    assert p.find("ul"), "A lista nincs benne a bekezdésben!"

def test_feladat_08_h2_fejezetcimek(dom):
    """8. Feladat: h2 címek a megjegyzések szövegével"""
    h2_szovegek = [h.text.strip() for h in dom.find_all("h2")]
    elvart = ["Helyi hálózatok", "Forgalomirányító", "Kapcsoló", "Szimbólumok"]
    for cim in elvart:
        assert cim in h2_szovegek, f"Hiányzik a '{cim}' h2 fejezetcím!"

def test_feladat_09_lablec_blokk(dom):
    """9. Feladat: Név és dátum blokk elemben"""
    divs = dom.find_all("div")
    assert len(divs) > 0, "Nincs általános blokk elem (div) az oldal alján!"
    footer_text = divs[-1].text
    import re
    assert re.search(r"\d{4}", footer_text), "A lábléc nem tartalmaz évszámot!"