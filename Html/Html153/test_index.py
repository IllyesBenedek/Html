import re
from bs4 import BeautifulSoup

HTML_FILE = "index.html"

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")


# -----------------------------
# 1. Magyar nyelv beállítása
# -----------------------------
def test_language():
    html = load_html()
    assert 'lang="hu"' in html, "❌ 1. feladat: A HTML nyelve nincs magyarra állítva (lang='hu')."
    print("✔️ 1. feladat rendben: magyar nyelv beállítva.")


# -----------------------------
# 2. UTF-8 kódolás
# -----------------------------
def test_utf8():
    html = load_html()
    assert "<meta charset=\"UTF-8\">" in html or "<meta charset=\"utf-8\">" in html, \
        "❌ 2. feladat: A kódolás nem UTF-8."
    print("✔️ 2. feladat rendben: UTF-8 kódolás beállítva.")


# -----------------------------
# 3. Cím: Verseny
# -----------------------------
def test_title():
    html = load_html()
    assert "<title>Verseny</title>" in html, "❌ 3. feladat: A böngésző fül címe nem 'Verseny'."
    print("✔️ 3. feladat rendben: cím 'Verseny'.")


# -----------------------------
# 4. Táblázat létezik
# -----------------------------
def test_table_exists():
    t = soup().find("table")
    assert t is not None, "❌ 4. feladat: Nincs táblázat az oldalon."
    print("✔️ 4. feladat rendben: táblázat megtalálva.")


# -----------------------------
# 5. Oszlopnyúlás (colspan)
# -----------------------------
def test_colspan():
    html = load_html()
    assert "colspan" in html, "❌ 5. feladat: Nincs oszlopnyúlás (colspan)."
    print("✔️ 5. feladat rendben: van colspan.")


# -----------------------------
# 6. H1: Pénzek
# -----------------------------
def test_h1_penzek():
    h1 = soup().find("h1")
    assert h1 is not None, "❌ 6. feladat: Nincs H1 cím."
    assert h1.text.strip() == "Pénzek", "❌ 6. feladat: A H1 cím nem 'Pénzek'."
    print("✔️ 6. feladat rendben: H1 = Pénzek.")


# -----------------------------
# 7. Caption: Kerekítés
# -----------------------------
def test_caption():
    caption = soup().find("caption")
    assert caption is not None, "❌ 7. feladat: Nincs caption a táblázatban."
    assert caption.text.strip() == "Kerekítés", "❌ 7. feladat: A caption szövege nem 'Kerekítés'."
    print("✔️ 7. feladat rendben: caption = Kerekítés.")


# -----------------------------
# 8. Footer doboz + név + dátum
# -----------------------------
def test_footer_box():
    footer = soup().find("footer")
    assert footer is not None, "❌ 8. feladat: Nincs footer doboz."
    assert footer.text.strip() != "", "❌ 8. feladat: A footer üres."
    print("✔️ 8. feladat rendben: footer megtalálva.")


# -----------------------------
# 9. A név dőlt betűvel
# -----------------------------
def test_footer_italic_name():
    footer = soup().find("footer")
    italic = footer.find("i")
    assert italic is not None, "❌ 9. feladat: A footerben a név nincs dőlt betűvel."
    print("✔️ 9. feladat rendben: név dőlt betűvel.")


