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
        return BeautifulSoup(f.read(), "html.parser")

def test_01_nyelv_magyar(html_soup):
    lang = html_soup.html.get("lang")
    assert lang == "hu", f"HIBA: A nyelv nincs magyarra (hu) állítva! (Jelenleg: {lang})"

def test_02_karakterkodolas(html_soup):
    assert html_soup.find("meta", charset=re.compile(r"utf-8", re.I)), "HIBA: Hiányzik az UTF-8 kódolás!"

def test_03_title_freebsd(html_soup):
    assert html_soup.title.text.strip() == "FreeBSD", "HIBA: A title nem 'FreeBSD'!"

def test_04_h1_freebsd(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "FreeBSD", "HIBA: A h1 nem 'FreeBSD'!"

def test_05_strong_freebsd(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "hasonlóság" in t)
    p = comment.find_next("p")
    assert p.find(["strong", "b"], string=re.compile("FreeBSD")), "HIBA: A 'FreeBSD' nem félkövér!"
   
def test_06_felsorolas_tagolas(html_soup):
    text = " ".join(html_soup.get_text().split())
    assert "GNOME, KDE, Xfce." in text, "HIBA: A Elérhető asztali környez felsorolás rossz!"
    assert "openbox, fluxbox, dwm, bspwm." in text, "HIBA: Az ablakkezelő felsorolás rossz!"

def test_07_mark_freebsd(html_soup):
   comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "FreeBSD" in t)
   target = comment.find_next("p").select_one("strong em, em strong, b i, i b")
   assert target and "Berkeley Software Distribution" in target.text, "HIBA: Hiányzik a félkövér+dőlt rész!"
   
def test_08_strong_em_berkeley(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "FreeBSD" in t)
    target = comment.find_next("p").select_one("strong em, em strong, b i, i b")
    assert target and "Berkeley Software Distribution" in target.text, "HIBA: Hiányzik a félkövér és dőlt rész!"

def test_09_footer_div(html_soup):
    div_text = " ".join(d.get_text() for d in html_soup.find_all("div"))
    minta = r"[a-zA-Záéíóöőúüű].*\d{4}"
    assert re.search(minta, div_text), "HIBA: A név vagy a dátum hiányzik a div-ből!"
