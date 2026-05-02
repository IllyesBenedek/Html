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

def test_01_nyelv(html_soup):
    assert html_soup.html.get("lang") == "hu"

def test_02_kodolas(html_soup):
    assert html_soup.find("meta", attrs={"charset": re.compile(r"utf-8", re.I)}) is not None

def test_03_title(html_soup):
    assert html_soup.title.text == "FreeBSD"

def test_04_h1(html_soup):
    assert html_soup.find("h1").text.strip() == "FreeBSD"

def test_05_kiemelesek_szama(html_soup):
    # Kikeressük az összes félkövér FreeBSD-t
    strongs = html_soup.find_all(["strong", "b"], string="FreeBSD")
    # Akkor fut le sikeresen, ha pontosan 2 (vagy több) van benne
    assert len(strongs) >= 2

def test_06_felsorolasok(html_soup):
    content = html_soup.text.lower()
    # Az összes kért környezet és ablakkezelő megléte
    assert "gnome" in content and "kde" in content and "xfce" in content
    assert "openbox" in content and "fluxbox" in content and "dwm" in content and "bspwm" in content

def test_07_bsd_formazas(html_soup):
    # Berkeley Software Distribution félkövér ÉS dőlt
    target = html_soup.find(string=re.compile("Berkeley Software Distribution"))
    p = target.parent
    tags = [t.name for t in p.find_parents() if t.name in ["strong", "b", "em", "i"]] + [p.name]
    assert any(t in ["strong", "b"] for t in tags) and any(t in ["em", "i"] for t in tags)

def test_08_vesszo_es_pont(html_soup):
    # Legyen benne vessző a felsorolásnál és pont a végén
    content = html_soup.text
    assert "," in content and "." in content

def test_09_komment(html_soup):
    # Dátum és név ellenőrzése az utolsó blokkban (footer, div vagy p)
    footer = html_soup.find_all(["footer", "div", "p"])[-1].get_text()
    assert re.search(r"\d{4}[-.]\d{2}[-.]\d{2}", footer) is not None
    assert len(footer.strip()) > 5