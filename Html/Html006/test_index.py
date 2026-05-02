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

def test_02_title(html_soup):
    assert html_soup.title.text == "HP-UX"

def test_03_focim(html_soup):
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "HP-UX"

def test_04_alcimek(html_soup):
    h2s = html_soup.find_all("h2")
    assert len(h2s) >= 3

def test_05_strong_hewlett(html_soup):
    # Keresünk olyan elemet, amiben benne van a Hewlett Packard Unix
    target = html_soup.find(["strong", "b"], string=re.compile("Hewlett Packard Unix"))
    assert target is not None

def test_06_abbr_hpux(html_soup):
    assert html_soup.find("abbr", string="HP-UX") is not None

def test_07_komment_adatok(html_soup):
    # A fájl végén lévő komment ellenőrzése
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*\d{4}[-.]\d{2}[-.]\d{2}.*-->", content) is not None

def test_08_felkover_unix(html_soup):
    # Unix operációs szó félkövér keresése
    target = html_soup.find(["strong", "b"], string=re.compile("Unix operációs"))
    assert target is not None

def test_09_dolt_vxfs(html_soup):
    # Ez CSAK akkor megy át, ha a dőlt rész (i vagy em) 
    # tartalma pontosan "VxFS", se több, se kevesebb.
    vxfs_italic = html_soup.find(["em", "i"], string="VxFS")
    assert vxfs_italic is not None
