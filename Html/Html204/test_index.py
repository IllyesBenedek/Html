from bs4 import BeautifulSoup
import os

HTML_FILE = "vitorlas.html"  # A fájl neve
URL_204 = "https://hu.wikipedia.org/wiki/Vitorlashajo"

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
    html = load_html()
    assert 'lang="hu"' in html, "FAIL: 2. feladat – A nyelv nincs magyarra állítva."


# 3. feladat – UTF-8 kódolás
def test_3_utf8():
    html = load_html().lower()
    assert 'charset="utf-8"' in html, "FAIL: 3. feladat – A kódolás nem UTF-8."


# 4. feladat – 'vitorlás hajó' link szövege
def test_4_vitorlas_link_szoveg():
    a = soup().find("a")
    assert a is not None, "FAIL: 4. feladat – Nincs hiperhivatkozás a szövegben."
    assert "vitorlás hajó" in a.text.lower(), "FAIL: 4. feladat – A link szövege nem 'vitorlás hajó'."


# 5. feladat – link URL helyes
def test_5_link_url():
    a = soup().find("a")
    assert a is not None and a["href"] == URL_204, \
        f"FAIL: 5. feladat – A hivatkozás URL-je hibás. (Várt: {URL_204})"


# 6. feladat – új ablakban nyíljon meg (target="_blank")
def test_6_target_blank():
    a = soup().find("a")
    assert a is not None and a.get("target") == "_blank", \
        "FAIL: 6. feladat – A link nem nyílik új ablakban (hiányzik a target=\"_blank\")."


# 7. feladat – a szöveg tartalma pontos
def test_7_szoveg_tartalom():
    html = load_html()
    assert "árbocok alapján tipizálhatók" in html, "FAIL: 7. feladat – A szöveg hiányos vagy hibás."
    assert "másfél, két és három vagy sokárbocú" in html, "FAIL: 7. feladat – A szöveg vége hiányzik."