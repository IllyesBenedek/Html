import pytest
from bs4 import BeautifulSoup
import os

HTML_FILE = "ut.html"
URL_UT = "https://hu.wikipedia.org/wiki/%C3%9At_(k%C3%B6zleked%C3%A9s)"

def get_soup():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

# 1. Az oldalnak legyen főcíme (h1): „Út”.
def test_01_h1_focim():
    h1 = get_soup().find("h1")
    assert h1 and h1.text.strip() == "Út", "FAIL: 1. pont – A főcím (h1) nem 'Út'!"

# 2. A szöveg bekezdésben (p) szerepeljen.
def test_02_p_tag():
    p = get_soup().find("p")
    assert p is not None, "FAIL: 2. pont – A szöveg nem bekezdésben (<p>) szerepel!"

# 3. Az első mondatban az „utak” szó legyen hiperhivatkozás.
def test_03_utak_link_szoveg():
    a = get_soup().find("p").find("a")
    assert a and "utak" in a.text.lower(), "FAIL: 3. pont – Az 'utak' szó nincs linkelve a bekezdésben!"

# 4. URL: https://hu.wikipedia.org/wiki/%C3%9At_(k%C3%B6zleked%C3%A9s)
def test_04_url_check():
    a = get_soup().find("p").find("a")
    assert a and a["href"] == URL_UT, "FAIL: 4. pont – A megadott URL hibás!"

# 5. Készítsen egy kettes szintű fejezetcímet (h2): „Forrás”.
def test_05_h2_forras():
    h2 = get_soup().find("h2")
    assert h2 and h2.text.strip() == "Forrás", "FAIL: 5. pont – Hiányzik a 'Forrás' fejezetcím (h2)!"

# 6. A fejezetcím alá vegye fel listába (<ul><li>) az előbbi URL-t.
def test_06_lista_es_url():
    ul = get_soup().find("ul")
    assert ul and ul.find("li"), "FAIL: 6. pont – Hiányzik a lista (<ul><li>)!"
    assert ul.find("a")["href"] == URL_UT, "FAIL: 6. pont – A listában lévő link hibás!"

# 7. Magyar nyelv kötelező (lang="hu")
def test_07_nyelv_hu():
    soup = get_soup()
    html_tag = soup.find("html")
    assert html_tag and html_tag.get("lang") == "hu", "FAIL: 7. pont – A nyelv nincs magyarra (hu) állítva!"

# 8. UTF-8 kódolás kötelező
def test_08_utf8_kodolas():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_text = f.read().lower()
    assert 'charset="utf-8"' in html_text, "FAIL: 8. pont – Hiányzik az UTF-8 kódolás beállítása!"
