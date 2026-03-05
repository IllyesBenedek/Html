import pytest
from bs4 import BeautifulSoup, Comment
import os

def get_soup():
    file_path = "index.html"
    if not os.path.exists(file_path):
        return BeautifulSoup("", "html.parser")
    with open(file_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

# 1. Megjegyzés a tetején (név, csoport, dátum)
def test_top_comment():
    soup = get_soup()
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    assert len(comments) > 0, "Hiányzik a megjegyzés a fájl tetejéről!"

# 2. Nyelv magyar (hu)
def test_lang_hu():
    soup = get_soup()
    assert soup.html.get("lang") == "hu"

# 3. UTF-8 kódolás
def test_encoding_utf8():
    soup = get_soup()
    meta = soup.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8"

# 4. Title: Gomba
def test_title_gomba():
    soup = get_soup()
    assert soup.title.string == "Gomba"

# 5. div elem container osztállyal
def test_div_container():
    soup = get_soup()
    div = soup.find("div", class_="container")
    assert div is not None

# 6. Gombák -> h1, A gombákról -> h2, Rokon tulajdonságok -> h2
def test_headings():
    soup = get_soup()
    container = soup.find("div", class_="container")
    assert container.find("h1").get_text().strip() == "Gombák"
    h2_tags = [h2.get_text().strip() for h2 in container.find_all("h2")]
    assert "A gombákról" in h2_tags
    assert "Rokon tulajdonságok" in h2_tags

# 7. Leírás bekezdésben (p)
def test_description_p():
    soup = get_soup()
    p_tag = soup.find("p")
    assert p_tag is not None and "szénszükségletüket" in p_tag.text

# 8. Rokon lista (ul, gomblista osztály, 7 elem, L-lizin félkövér)
def test_list_requirements():
    soup = get_soup()
    ul = soup.find("ul", class_="gomblista")
    assert ul is not None
    li_tags = ul.find_all("li")
    assert len(li_tags) == 7
    # Félkövér ellenőrzése a listában
    bold = ul.find(["b", "strong"])
    assert bold is not None and "L-lizin" in bold.text

# 9. Névjegy section
def test_section_footer():
    soup = get_soup()
    section = soup.find("section")
    assert section is not None
    assert len(section.get_text().strip()) > 5 # Tartalmaznia kell adatokat