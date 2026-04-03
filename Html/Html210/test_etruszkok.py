import pytest
from bs4 import BeautifulSoup
import os

# Alapbeállítások a teszthez
HTML_FILE = "etruszkok.html"

def get_soup():
    """Segédfüggvény a HTML beolvasásához."""
    if not os.path.exists(HTML_FILE):
        pytest.fail(f"A {HTML_FILE} fájl nem található!")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

# 1. Főcím: Legyen egy <h1>Etruszkok</h1> főcím az oldalon.
def test_01_h1_focim():
    h1 = get_soup().find("h1")
    assert h1 is not None, "FAIL: 1. pont - Hiányzik a főcím (<h1>)!"
    assert h1.text.strip() == "Etruszkok", "FAIL: 1. pont - A főcím szövege nem 'Etruszkok'!"

# 2. Városlista: Hozzon létre egy számozatlan listát (<ul>) a városokkal.
def test_02_szamozatlan_lista():
    # Az első listát keressük
    ul = get_soup().find("ul")
    assert ul is not None, "FAIL: 2. pont - Hiányzik a számozatlan lista (<ul>)!"
    li_items = ul.find_all("li")
    assert len(li_items) >= 3, "FAIL: 2. pont - A városlistának legalább 3 elemből kell állnia!"

# 3. Tisztítás: A listában csak a városok nevei szerepeljenek (kötőjel és URL nélkül).
def test_03_tisztitas_ellenorzese():
    ul = get_soup().find("ul")
    li_texts = [li.get_text() for li in ul.find_all("li")]
    for text in li_texts:
        assert "-" not in text, f"FAIL: 3. pont - A listaelemben maradt kötőjel: {text}"
        assert "http" not in text.lower(), f"FAIL: 3. pont - A listaelemben benne maradt az URL: {text}"

# 4. Linkelés: Mindhárom városnév mutasson a saját Wikipédia oldalára.
def test_04_varos_linkek_url():
    links = get_soup().find("ul").find_all("a")
    hrefs = [a.get("href") for a in links]
    assert "https://hu.wikipedia.org/wiki/Velch" in hrefs, "FAIL: 4. pont - Vulci linkje hibás!"
    assert "https://hu.wikipedia.org/wiki/Cortona" in hrefs, "FAIL: 4. pont - Cortona linkje hibás!"
    assert "https://hu.wikipedia.org/wiki/Volterra" in hrefs, "FAIL: 4. pont - Volterra linkje hibás!"

# 5. Cél (Target): Minden link új lapon nyíljon meg (target="_blank").
def test_05_target_blank_mindenhol():
    all_links = get_soup().find_all("a")
    assert len(all_links) > 0, "FAIL: 5. pont - Nincsenek linkek az oldalon!"
    for a in all_links:
        assert a.get("target") == "_blank", f"FAIL: 5. pont - A(z) '{a.text}' linknél hiányzik a target='_blank'!"

# 6. Forrás fejezet: Legyen egy <h2>Forrás</h2> fejezetcím és alatta egy lista.
def test_06_forras_h2_es_lista():
    soup = get_soup()
    h2 = soup.find("h2")
    assert h2 is not None, "FAIL: 6. pont - Hiányzik a kettes szintű fejezetcím (<h2>)!"
    assert h2.text.strip() == "Forrás", "FAIL: 6. pont - A fejezetcím szövege nem 'Forrás'!"
    # Ellenőrizzük, hogy van-e második lista a h2 után
    source_ul = h2.find_next("ul")
    assert source_ul is not None, "FAIL: 6. pont - A Forrás alatt hiányzik a lista!"
    assert "https://hu.wikipedia.org/wiki/Etruszkok" in source_ul.find("a").get("href"), "FAIL: 6. pont - A forrás link hibás!"

# 7. Nyelv: Az oldal nyelve legyen magyar (<html lang="hu">).
def test_07_nyelv_hu():
    html_tag = get_soup().find("html")
    assert html_tag is not None and html_tag.get("lang") == "hu", "FAIL: 7. pont - A nyelv nincs magyarra (hu) állítva!"

# 8. Kódolás: A karakterkódolás legyen UTF-8 (<meta charset="utf-8">).
def test_08_utf8_kodolas():
    # Itt nyers szövegként is nézzük a biztonság kedvéért
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        content = f.read().lower()
    assert 'charset="utf-8"' in content, "FAIL: 8. pont - Hiányzik az UTF-8 kódolás beállítása!"
