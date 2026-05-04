import pytest
from bs4 import BeautifulSoup, Comment
import os
import re

@pytest.fixture
def html_soup():
    path = "index.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "parser.parser" if "parser.parser" in str(f) else "html.parser")

def test_01_nyelv_magyar(html_soup):
    assert html_soup.html.get("lang") == "hu", "Hiba: A nyelv nincs 'hu'-ra állítva!"

def test_02_karakterkodolas(html_soup):
    meta = html_soup.find("meta", charset=re.compile(r"utf-8", re.I))
    assert meta is not None, "Hiba: Hiányzik az UTF-8 kódolás beállítása!"

def test_03_title_vi(html_soup):
    assert html_soup.title.text.strip() == "vi", "Hiba: A <title> nem 'vi'!"

def test_04_h1_vi(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "vi", "Hiba: Nincs <h1> 'vi' tartalommal!"

def test_05_h2_szamlalas(html_soup):
    exp, act = {"Az eredeti", "Szabvány", "Interfész"}, {h.text.strip() for h in html_soup.find_all("h2")}
    hiany = exp - act
    assert not hiany, f"HIBA: {len(hiany)} hiányzik: {hiany}. Megvan: {len(act)}/4"
    for h in html_soup.find_all("h2"):
        c = h.find_previous(string=lambda t: isinstance(t, Comment))
        assert c and h.text.strip() == c.strip(), f"HIBA: Rossz komment: '{h.text.strip()}'"

def test_06_p_szamlalas(html_soup):
    ps = html_soup.find_all("p")
    assert len(ps) == 4, f"Hiba: {len(ps)} bekezdés van a 4 helyett!"

def test_07_kbd_interfesz_blokk(html_soup):
    last_p = html_soup.find_all("p")[-1]
    kbds = last_p.find_all("kbd")
    assert len(kbds) >= 3, "Hiba: Kevés számítógép billentyűnek jelölő elemet használtál az Interfész szakaszban!"
    
    # 6.c. Az Esc szó szintén legyen számítógép billentyűnek jelölve
    esc_kbd = last_p.find("kbd", string=re.compile("Esc"))
    assert esc_kbd is not None, "Hiba: Az 'Esc' nincs <kbd> tagek között!"

def test_08_strong_posix(html_soup):
    # 8. Az első bekezdésben a „POSIX” szöveg legyen félkövér.
    first_p = html_soup.find_all("p")[0]
    target = first_p.find(["strong", "b"], string=re.compile("POSIX"))
    assert target is not None, "Hiba: A 'POSIX' szöveg nem félkövér!"

def test_09_komment_nev_datum(html_soup):
    # 9. HTML forráskódban megjegyzés névvel és dátummal
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*202[0-9].*-->", content), "Hiba: Hiányzik a név/dátum megjegyzés!"
