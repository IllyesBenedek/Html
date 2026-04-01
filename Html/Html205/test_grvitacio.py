from bs4 import BeautifulSoup
import os

HTML_FILE = "gravitacio.html"
URL_205 = "https://hu.wikipedia.org/wiki/Gravitacio"

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
    assert 'lang="hu"' in html, "FAIL: 2. feladat – A nyelv nincs magyarra állítva (<html lang=\"hu\">)."


# 3. feladat – UTF-8 kódolás
def test_3_utf8():
    html = load_html().lower()
    assert 'charset="utf-8"' in html, "FAIL: 3. feladat – A kódolás nem UTF-8."


# 4. feladat – 'gravitáció' szó az első mondatban link
def test_4_gravitacio_link_szoveg():
    a = soup().find("a")
    assert a is not None, "FAIL: 4. feladat – Nincs hiperhivatkozás (<a>) a szövegben."
    assert a.text.strip().lower() == "gravitáció", "FAIL: 4. feladat – A link szövege nem 'gravitáció'."


# 5. feladat – link URL helyes
def test_5_link_url():
    a = soup().find("a")
    # Megnézzük, hogy az URL pontosan egyezik-e a képen lévővel
    assert a is not None and a["href"] == URL_205, \
        f"FAIL: 5. feladat – A hivatkozás URL-je hibás. (Várt: {URL_205})"


# 6. feladat – szövegtartalom ellenőrzése
def test_6_szoveg_pontossag():
    text = soup().get_text()
    assert "elhajlított téridő következménye" in text, "FAIL: 6. feladat – A szöveg eleje hibás vagy hiányzik."
    assert "erősödő gravitációként érzékelünk" in text, "FAIL: 6. feladat – A szöveg közepe hibás vagy hiányzik."
    assert "gyengébbnek érezzük" in text, "FAIL: 6. feladat – A szöveg vége hibás vagy hiányzik."