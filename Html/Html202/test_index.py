from bs4 import BeautifulSoup
import os

HTML_FILE = "capa.html"   # vagy dark.html helyett, ha így nevezed

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")


# 1. feladat – fájl létezik
def test_1_file_exists():
    assert os.path.exists(HTML_FILE), "FAIL: 1. feladat – A fájl nem létezik."


# 2. feladat – magyar nyelv
def test_2_lang_hu():
    html = load_html()
    assert 'lang="hu"' in html, "FAIL: 2. feladat – A nyelv nincs magyarra állítva."


# 3. feladat – UTF-8
def test_3_utf8():
    html = load_html()
    assert "<meta charset=\"UTF-8\">" in html or "<meta charset=\"utf-8\">" in html, \
        "FAIL: 3. feladat – A kódolás nem UTF-8."


# 4. feladat – title = Cápa
def test_4_title():
    html = load_html()
    assert "<title>Cápa</title>" in html, "FAIL: 4. feladat – A title nem 'Cápa'."


# 5. feladat – H1 = Cápa
def test_5_h1():
    h1 = soup().find("h1")
    assert h1 is not None, "FAIL: 5. feladat – Nincs H1 cím."
    assert h1.text.strip() == "Cápa", "FAIL: 5. feladat – A H1 szövege nem 'Cápa'."


# 6. feladat – 'megalodon' hiperhivatkozás
def test_6_megalodon_link():
    a = soup().find("a")
    assert a is not None, "FAIL: 6. feladat – Nincs hiperhivatkozás."
    assert a.text.strip().lower() == "megalodon", "FAIL: 6. feladat – A link szövege nem 'megalodon'."


# 7. feladat – link URL helyes
def test_7_link_url():
    a = soup().find("a")
    assert a["href"] == "https://hu.wikipedia.org/wiki/%C3%93ri%C3%A1sfog%C3%BA_c%C3%A1pa", \
        "FAIL: 7. feladat – A hivatkozás URL-je hibás."


# 8. feladat – 'legnagyobb húsevő' kiemelve
def test_8_strong():
    strong = soup().find("strong")
    assert strong is not None, "FAIL: 8. feladat – Nincs kiemelt szöveg."
    assert strong.text.strip().lower() == "legnagyobb húsevő", \
        "FAIL: 8. feladat – A kiemelt szöveg nem 'legnagyobb húsevő'."


# 9. feladat – 'óriásfogú' dőlt
def test_9_italic():
    em = soup().find("em")
    assert em is not None, "FAIL: 9. feladat – Nincs dőlt szöveg."
    assert em.text.strip().lower() == "óriásfogú", \
        "FAIL: 9. feladat – A dőlt szöveg nem 'óriásfogú'."
