from bs4 import BeautifulSoup
import os

HTML_FILE = "orion.html"
URL_1 = "https://en.wikipedia.org/wiki/Orion_Nebula"
URL_2 = "https://wp-hu.wikideck.com/Orion-kod"

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")

# 1. feladat – fájl létezik
def test_1_file_exists():
    assert os.path.exists(HTML_FILE), f"FAIL: 1. feladat – A {HTML_FILE} fájl nem létezik."

# 2. feladat – magyar nyelv
def test_2_lang_hu():
    s = soup().find("html")
    assert s and s.get("lang") == "hu", "FAIL: 2. feladat – A nyelv nincs magyarra állítva (<html lang=\"hu\">)."

# 3. feladat – UTF-8 kódolás (EZ AZ AMIT KÉRDEZTÉL)
def test_3_utf8():
    html = load_html().lower()
    assert '<meta charset="utf-8">' in html, "FAIL: 3. feladat – Hiányzik az UTF-8 kódolás beállítása!"

# 4. feladat – Orion-köd link és target
def test_4_orion_link():
    s = soup()
    link = s.find("a", string=lambda t: t and "Orion-köd" in t)
    assert link is not None, "FAIL: 4. feladat – Az 'Orion-köd' nincs linkké alakítva."
    assert link["href"] == URL_1, "FAIL: 4. feladat – Az URL hibás."
    assert link.get("target") == "_blank", "FAIL: 4. feladat – A link nem új lapon nyílik meg."

# 5. feladat – Forrás cím és lista
def test_5_forras_lista():
    s = soup()
    assert "Forrás" in s.get_text(), "FAIL: 5. feladat – Hiányzik a 'Forrás' felirat."
    ul = s.find("ul")
    assert ul is not None, "FAIL: 5. feladat – A források nincsenek listába (<ul>) téve."
    assert len(ul.find_all("li")) == 2, "FAIL: 5. feladat – A listának 2 elemből kell állnia."

# 6. feladat – Forrás linkek célja (új böngészőfül)
def test_6_source_targets():
    links = soup().find("ul").find_all("a")
    for l in links:
        assert l.get("target") == "_blank", "FAIL: 6. feladat – A forrás link nem új fülön nyílik meg."
