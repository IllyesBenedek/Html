import pytest
import re

# 1. feladat: Weboldal kódolása utf-8
def test_utf8_charset():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read().lower()
        assert 'charset="utf-8"' in content or "charset='utf-8'" in content, "1. Hiba: A kódolás nem UTF-8!"

# 2. feladat: Böngésző fülön „Roborálás”
def test_title_tag():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<title>Roborálás</title>" in content, "2. Hiba: A title nem 'Roborálás'!"

# 3. feladat: „Roboráló gyügynövények” az oldal tetején H1
def test_h1_heading():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r'<h1>\s*Roboráló gyügynövények\s*</h1>', content), "3. Hiba: A 'Roboráló gyügynövények' nem H1-es fejezetcím!"

# 4. feladat: „Csipkebogyó” és „Csalán” alatti részek beállítása bekezdésnek (p)
def test_paragraphs():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        # Ellenőrizzük, hogy mindkét név után van-e bekezdés tag
        assert re.search(r'Csipkebogyó.*<p>', content, re.DOTALL), "4. Hiba: A Csipkebogyó után hiányzik a bekezdés (<p>)!"
        assert re.search(r'Csalán.*<p>', content, re.DOTALL), "4. Hiba: A Csalán után hiányzik a bekezdés (<p>)!"

# 5. feladat: „Csipkebogyó” és „Csalán” megjegyzések alatt kettes szintű fejezetcímek (H2)
def test_h2_headings():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r'\s*<h2>\s*Csipkebogyó\s*</h2>', content), "5. Hiba: A 'Csipkebogyó' H2 hiányzik a megjegyzés alól!"
        assert re.search(r'\s*<h2>\s*Csalán\s*</h2>', content), "5. Hiba: A 'Csalán' H2 hiányzik a megjegyzés alól!"

# 6. feladat: Az oldal nyelve magyar
def test_language_hu():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read().lower()
        assert '<html lang="hu">' in content, "6. Hiba: Az oldal nyelve nincs magyarra állítva (<html lang='hu'>)!"

# 7. feladat: „Növények listája” megjegyzés alatt számozatlan lista (ul)
def test_unordered_list():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r'\s*<ul>', content), "7. Hiba: A számozatlan lista hiányzik a megjegyzés alól!"
        assert len(re.findall(r'<li>', content)) == 4, "7. Hiba: A listának 4 elemet (li) kell tartalmaznia!"

# 8. feladat: „sources” megjegyzés alatt „Forrás” kettes szintű fejezetcím (H2)
def test_source_h2():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r'\s*<h2>\s*Forrás\s*</h2>', content), "8. Hiba: A 'Forrás' H2 hiányzik a 'sources' megjegyzés alól!"

# 9. feladat: Első bekezdésben a „Roboráló” szó kiemelt
def test_highlighted_word():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        # A kiemelés lehet strong vagy b
        assert re.search(r'<(strong|b)>Roboráló</(strong|b)>', content), "9. Hiba: A 'Roboráló' szó nincs kiemelve (strong vagy b)!"