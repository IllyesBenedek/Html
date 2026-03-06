import pytest
from bs4 import BeautifulSoup, Comment
import os

@pytest.fixture
def soup():
    with open("index.html", "r", encoding="UTF-8") as f:
        return BeautifulSoup(f, "html.parser")

def test_1_lang(soup):
    assert soup.html.get("lang") == "hu", "1. Hiba: A nyelv nem magyar!"

def test_2_title(soup):
    assert soup.title.string == "Arduino", "2. Hiba: A title nem 'Arduino'!"

def test_3_charset(soup):
    assert soup.find("meta", charset="UTF-8"), "3. Hiba: Az utf-8 hiányzik!"

def test_4_h1(soup):
    assert soup.find("h1").text == "Az Arduino", "4. Hiba: A <h1> nem 'Az Arduino'!"

def test_5_pro_micro_image(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "Az arduino" in t)
    img = comment.find_next("p").find("img", alt="Az arduino")
    assert img, "5. Hiba: Az alt szöveg nem egyezik a megjegyzéssel ('Az arduino')!"

def test_6_robot_image(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "Arduino Board" in t)
    img = comment.find_next("p").find("img", alt="Arduino Board")
    assert img, "6. Hiba: Az alt szöveg nem egyezik a megjegyzéssel ('Arduino Board')!"

def test_7_uno_image(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "Shield" in t)
    img = comment.find_next("p").find("img", alt="Shield")
    assert img, "7. Hiba: Az alt szöveg nem egyezik a megjegyzéssel ('Shield')!"

def test_8_h2_headers(soup):
    h2s = [h.text.strip() for h in soup.find_all("h2")]
    assert all(x in h2s for x in ["Az arduino", "Szoftver", "Arduino Board", "Shield"]), "8. Hiba: Hiányzó H2!"

def test_9_intel_curie_italic(soup):
    assert soup.find(["i", "em"], string=lambda t: t and "Intel Curie" in t), "9. Hiba: Az 'Intel Curie' nincs dőltnek jelölve!"