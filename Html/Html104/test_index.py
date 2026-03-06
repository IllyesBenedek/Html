import pytest
from bs4 import BeautifulSoup, Comment

@pytest.fixture
def soup():
    with open("index.html", "r", encoding="UTF-8") as f:
        return BeautifulSoup(f, "html.parser")

# 1. Oldal nyelve
def test_1_lang(soup):
    assert soup.html.get("lang") == "hu", "1. Hiba: Az oldal nyelve nem 'hu'!"

# 2. UTF-8 kódolás
def test_2_charset(soup):
    meta = soup.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8", "2. Hiba: Az utf-8 kódolás hiányzik!"

# 3. Böngészőfülön 'VLAN'
def test_3_title(soup):
    assert soup.title and soup.title.string == "VLAN", "3. Hiba: A böngésző fülön nem 'VLAN' szerepel!"

# 4. 'LAN' megjegyzés alatt h1 cím
def test_4_lan_h1(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "LAN" in t)
    assert comment, "4. Hiba: Hiányzik a 'LAN' megjegyzés!"
    h1 = comment.find_next("h1")
    assert h1 and h1.text.strip() == "LAN", "4. Hiba: A LAN megjegyzés alatt nem 'LAN' címsor van!"

# 5. 'Hálózat ábra' megjegyzés alatt a kép
def test_5_image_path(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "Hálózat ábra" in t)
    assert comment, "5. Hiba: Hiányzik a 'Hálózat ábra' megjegyzés!"
    img = comment.find_next("img")
    assert img and img.get("src") == "images/feladat_104_halozat.png", "5. Hiba: A kép forrása nem 'images/feladat_104_halozat.png'!"

# 6. 'Hálózat leírása' megjegyzés alatti szöveg bekezdésben
def test_6_description_paragraph(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "Hálózat leírása" in t)
    assert comment, "6. Hiba: Hiányzik a 'Hálózat leírása' megjegyzés!"
    p = comment.find_next("p")
    assert p, "6. Hiba: A szöveg nem bekezdésben (<p>) van!"

# 7. 'IP címek' megjegyzés alatt h2 cím
def test_7_ip_h2(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "IP címek" in t)
    assert comment, "7. Hiba: Hiányzik az 'IP címek' megjegyzés!"
    h2 = comment.find_next("h2")
    assert h2 and h2.text.strip() == "IP címek", "7. Hiba: Az 'IP címek' megjegyzés alatt nem H2 cím van!"

# 8. 'IP címek listája' megjegyzés alatt lista
def test_8_list_container(soup):
    comment = soup.find(string=lambda t: isinstance(t, Comment) and "IP címek listája" in t)
    assert comment, "8. Hiba: Hiányzik az 'IP címek listája' megjegyzés!"
    assert comment.find_next("ul"), "8. Hiba: A számozatlan lista (<ul>) nem található!"

# 9. Listaelemek száma (5 sor = 5 elem)
def test_9_list_items(soup):
    ul = soup.find("ul")
    items = ul.find_all("li")
    assert len(items) == 5, f"9. Hiba: A listának 5 elemet kell tartalmaznia, de {len(items)} van!"