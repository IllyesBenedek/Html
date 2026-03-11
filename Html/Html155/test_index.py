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


# 3. Cím: Versenyzők
def test_title():
    html = load_html()
    assert "<title>Versenyzők</title>" in html, "❌ 3. feladat: A cím nem 'Versenyzők'."
    print("✔️ 3. feladat rendben: cím 'Versenyzők'.")


# 4. Táblázat létezik
def test_table_exists():
    assert soup().find("table") is not None, "❌ 4. feladat: Nincs táblázat."
    print("✔️ 4. feladat rendben: táblázat megtalálva.")


# 5. Sornyúlás (padding)
def test_padding():
    html = load_html()
    assert "padding" in html, "❌ 5. feladat: Nincs sornyúlás (padding)."
    print("✔️ 5. feladat rendben: van sornyúlás.")


# 6. H1: Személyek
def test_h1():
    h1 = soup().find("h1")
    assert h1 is not None, "❌ 6. feladat: Nincs H1 cím."
    assert h1.text.strip() == "Személyek", "❌ 6. feladat: A H1 cím nem 'Személyek'."
    print("✔️ 6. feladat rendben: H1 = Személyek.")


# 7. Caption: Kajak versenyzőink
def test_caption():
    caption = soup().find("caption")
    assert caption is not None, "❌ 7. feladat: Nincs caption."
    assert caption.text.strip() == "Kajak versenyzőink", \
        "❌ 7. feladat: A caption nem 'Kajak versenyzőink'."
    print("✔️ 7. feladat rendben: caption = Kajak versenyzőink.")


# 8. Footer tartalom
def test_footer():
    footer = soup().find("footer")
    assert footer is not None, "❌ 8. feladat: Nincs footer."
    assert "2024-s Kajak-kenu versenyre készült" in footer.text, \
        "❌ 8. feladat: A footer szövege nem megfelelő."
    print("✔️ 8. feladat rendben: footer megfelelő.")


# 9. Megjegyzés a tetején
def test_comment_top():
    html = load_html().strip()
    first_line = html.split("\n")[0]
    assert first_line.startswith("<!--"), "❌ 9. feladat: A fájl tetején nincs megjegyzés."
    assert re.search(r"\d{4}\.\d{2}\.\d{2}", first_line), \
        "❌ 9. feladat: A megjegyzésben nincs dátum."
    print("✔️ 9. feladat rendben: megjegyzés a fájl tetején.")
