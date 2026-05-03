import pytest
from bs4 import BeautifulSoup
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
    # 1. Nyelv beállítása magyarra
    assert html_soup.html.get("lang") == "hu"

def test_02_karakterkodolas(html_soup):
    # 2. Karakterkódolás UTF-8 (ékezetek miatt)
    meta = html_soup.find("meta", charset=re.compile(r"utf-8", re.I))
    assert meta is not None

def test_03_title_freebsd(html_soup):
    # 3. Böngészőfül címe: FreeBSD
    assert html_soup.title.text.strip() == "FreeBSD"

def test_04_h1_freebsd(html_soup):
    # 4. Egyes szintű fejezetcím: FreeBSD
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "FreeBSD"

def test_05_strong_freebsd(html_soup):
    # 5. A hasonlóság blokkban a FreeBSD szó félkövér
    target = html_soup.find_all("strong", string="FreeBSD")
    assert target is not None, "Nem található félkövér (strong) FreeBSD szó!"

def test_06_felsorolas_tagolas(html_soup):
    # 6. Vesszős tagolás és pont a végén
    body_text = html_soup.get_text()
    assert "GNOME, KDE, Xfce." in body_text
    assert "openbox, fluxbox, dwm, bspwm." in body_text

def test_07_mark_freebsd(html_soup):
    # 7. FreeBSD szó kiemelt (mark)
    assert html_soup.find("mark", string="FreeBSD") is not None

def test_08_strong_em_berkeley(html_soup):
    # 8. Berkeley Software Distribution félkövér ÉS dőlt
    target = html_soup.find(["strong", "b"])
    inner = target.find(["em", "i"])
    assert "Berkeley Software Distribution" in inner.text

def test_09_footer_div(html_soup):
    # 9. Név és dátum blokk elemben (div) a végén
    div = html_soup.find_all("div")[-1]
    assert re.search(r"202[0-9]", div.text) is not None
