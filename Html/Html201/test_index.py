from bs4 import BeautifulSoup
import os

HTML_FILE = "dark.html"

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")


# 1. feladat – dark.html létezik
def test_1_fajl_letezik():
    assert os.path.exists(HTML_FILE), "FAIL: 1. feladat – A dark.html fájl nem létezik."


# 2. feladat – magyar nyelv
def test_2_nyelv_magyar():
    html = load_html()
    assert 'lang="hu"' in html, "FAIL: 2. feladat – A weboldal nyelve nincs magyarra állítva."


# 3. feladat – UTF-8 kódolás
def test_3_utf8():
    html = load_html()
    assert "<meta charset=\"UTF-8\">" in html or "<meta charset=\"utf-8\">" in html, \
        "FAIL: 3. feladat – A kódolás nem UTF-8."


# 4. feladat – title
def test_4_title():
    html = load_html()
    assert "<title>Dark</title>" in html, "FAIL: 4. feladat – A title nem 'Dark'."


# 5. feladat – H1 létezik és helyes
def test_5_h1():
    h1 = soup().find("h1")
    assert h1 is not None, "FAIL: 5. feladat – Nincs H1 cím."
    assert "sötét anyag" in h1.text.lower(), "FAIL: 5. feladat – A H1 szövege nem 'Sötét anyag'."


# 6. feladat – H1-ben hiperhivatkozás
def test_6_h1_link():
    h1 = soup().find("h1")
    a = h1.find("a")
    assert a is not None, "FAIL: 6. feladat – A H1 nem tartalmaz hiperhivatkozást."
    assert a.text.strip().lower() == "sötét anyag", "FAIL: 6. feladat – A link szövege nem 'Sötét anyag'."


# 7. feladat – hivatkozás URL-je
def test_7_link_url():
    a = soup().find("a")
    assert a is not None, "FAIL: 7. feladat – Nincs hivatkozás."
    assert a["href"] == "https://en.wikipedia.org/wiki/Dark_matter", \
        "FAIL: 7. feladat – A hivatkozás URL-je hibás."


# 8. feladat – 'sugárzást' kiemelve
def test_8_kielemeles():
    strong = soup().find("strong")
    assert strong is not None, "FAIL: 8. feladat – Nincs kiemelt szöveg."
    assert strong.text.strip().lower() == "sugárzást", "FAIL: 8. feladat – A kiemelt szöveg nem 'sugárzást'."


# 9. feladat – footer létezik és tartalmaz nevet + dátumot
def test_9_footer():
    footer = soup().find("footer")
    assert footer is not None, "FAIL: 9. feladat – Nincs lábléc."
    text = footer.text.lower()
    assert "benedek" in text, "FAIL: 9. feladat – A lábléc nem tartalmazza a nevet."
    assert any(char.isdigit() for char in text), "FAIL: 9. feladat – A lábléc nem tartalmaz dátumot."
