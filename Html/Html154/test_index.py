import re
from bs4 import BeautifulSoup

HTML_FILE = "index.html"

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")


# 1. Magyar nyelv
def test_language():
    html = load_html()
    assert 'lang="hu"' in html, "❌ 1. feladat: A HTML nyelve nincs magyarra állítva."
    print("✔️ 1. feladat rendben: magyar nyelv beállítva.")


# 2. UTF-8 kódolás
def test_utf8():
    html = load_html()
    assert "<meta charset=\"UTF-8\">" in html or "<meta charset=\"utf-8\">" in html, \
        "❌ 2. feladat: A kódolás nem UTF-8."
    print("✔️ 2. feladat rendben: UTF-8 kódolás.")


# 3. Cím: Verseny
def test_title():
    html = load_html()
    assert "<title>Verseny</title>" in html, "❌ 3. feladat: A cím nem 'Verseny'."
    print("✔️ 3. feladat rendben: cím 'Verseny'.")


# 4. Táblázat létezik
def test_table_exists():
    assert soup().find("table") is not None, "❌ 4. feladat: Nincs táblázat."
    print("✔️ 4. feladat rendben: táblázat megtalálva.")


# 5. Oszlopnyúlás (colspan)
def test_colspan():
    html = load_html()
    assert "colspan" in html, "❌ 5. feladat: Nincs oszlopnyúlás (colspan)."
    print("✔️ 5. feladat rendben: van colspan.")


# 6. Sornyúlás (rowspan)
def test_rowspan():
    html = load_html()
    assert "rowspan" in html, "❌ 6. feladat: Nincs sornyúlás (rowspan)."
    print("✔️ 6. feladat rendben: van rowspan.")


# 7. Leírás p elemben
def test_description():
    p = soup().find("p")
    assert p is not None, "❌ 7. feladat: Nincs p elem."
    assert p.text.strip() == "Kötött pályás jármű árlista.", \
        "❌ 7. feladat: A p elem szövege nem megfelelő."
    print("✔️ 7. feladat rendben: p elem megfelelő.")


# 8. Footer doboz
def test_footer():
    footer = soup().find("footer")
    assert footer is not None, "❌ 8. feladat: Nincs footer."
    assert footer.text.strip() != "", "❌ 8. feladat: A footer üres."
    print("✔️ 8. feladat rendben: footer megtalálva.")


# 9. Megjegyzés a tetején
def test_comment_top():
    html = load_html().strip()
    first_line = html.split("\n")[0]
    assert first_line.startswith("<!--"), "❌ 9. feladat: A fájl tetején nincs megjegyzés."
    assert re.search(r"\d{4}\.\d{2}\.\d{2}", first_line), "❌ 9. feladat: A megjegyzésben nincs dátum."
    print("✔️ 9. feladat rendben: megjegyzés a fájl tetején.")
