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
    meta = html_soup.find("meta", charset=re.compile(r"utf-8", re.I))
    assert meta is not None, "HIBA: Hiányzik a <meta charset='utf-8'/>!"

def test_03_title_freebsd(html_soup):
    assert html_soup.title.text.strip() == "FreeBSD", "HIBA: A title nem 'FreeBSD'!"

def test_04_h1_freebsd(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "FreeBSD", "HIBA: A h1 nem 'FreeBSD'!"

def test_05_strong_freebsd(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "hasonlóság" in t)
    target_p = comment.find_next("p")
    strong_tag = target_p.find(["strong", "b"])
    assert strong_tag is not None, "HIBA: Nincs félkövér szöveg a bekezdésben!"
    assert "FreeBSD" in strong_tag.get_text(), "HIBA: A 'FreeBSD' szó nem félkövér!"

def test_06_felsorolas_tagolas(html_soup):
    text = " ".join(html_soup.get_text().split())
    assert "GNOME, KDE, Xfce." in text, "HIBA: A GNOME-Xfce felsorolás nem megfelelő!"
    assert "openbox, fluxbox, dwm, bspwm." in text, "HIBA: Az ablakkezelő felsorolás nem megfelelő!"

def test_07_mark_freebsd(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "hasonlóság" in t)
    target_p = comment.find_next("p")
    mark_tag = target_p.find("mark")
    assert mark_tag is not None, "HIBA: Nincs <mark> a bekezdésben!"
    assert mark_tag.get_text().strip() == "FreeBSD"
   
def test_08_strong_em_berkeley(html_soup):
    comment = html_soup.find(string=lambda t: isinstance(t, Comment) and "FreeBSD" in t.strip())
    target_p = comment.find_next("p")
    target = target_p.select_one("strong em, em strong, b i, i b")
    assert target is not None, "HIBA: Nincs félkövér és dőlt szöveg!"
    assert "Berkeley Software Distribution" in target.get_text()
        
def test_09_footer_div(html_soup):
    footer_div = html_soup.find_all("div")[-1]
    text = footer_div.get_text().strip()
    assert len(text) > 10, "HIBA: A név vagy a dátum hiányzik!"
    assert re.search(r"202[0-9]", text) is not None, "HIBA: A dátum hiányzik!"
