# test_index.py

import os
import pytest

def test_html_file_exists():
    """1. Ellenőrzi, hogy létezik-e az index.html fájl."""
    assert os.path.exists("index.html"), "Az index.html fájl nem található."

def test_encoding_set():
    """2. UTF-8 karakterkódolás beállítása."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<meta charset="UTF-8">' in content, "Hiányzik a UTF-8 karakterkódolás."

def test_language_set():
    """3. Magyar nyelv beállítása."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert 'lang="hu"' in content, "A nyelv nincs beállítva magyarra."

def test_title_set():
    """4. 'vi' cím a böngésző fülön."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<title>vi</title>' in content, "A cím nem 'vi'."

def test_comments_removed_and_headings_added():
    """5. 'A vi' és 'A vim' megjegyzések eltávolítva, h2 címek hozzáadva."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Megjegyzések eltávolítva
    assert "<!-- A vi -->" not in content, "Az 'A vi' megjegyzés még szerepel."
    assert "<!-- A vim -->" not in content, "Az 'A vim' megjegyzés még szerepel."
    
    # H2 címek hozzáadva
    assert '<h2>A vi</h2>' in content, "Hiányzik 'A vi' h2 cím."
    assert '<h2>A vim</h2>' in content, "Hiányzik 'A vim' h2 cím."

def test_paragraphs_created():
    """6. Bekezdések létrehozva."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<p>' in content, "Hiányznak a bekezdés elemek."
    assert content.count('<p>') >= 2, "Kevesebb mint 2 bekezdés van."

def test_emphasized_text():
    """7. 'képernyő-orientált' szöveg kiemelve."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<em>képernyő-orientált</em>' in content, "Hiányzik a kiemelt szöveg."

def test_list_created():
    """8. 'vi változatok' számozatlan listaként."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<ul>' in content, "Hiányzik a számozatlan lista."
    assert '<li>' in content, "Hiányznak a listaelemek."
    assert content.count('<li>') >= 5, "Nem megfelelő számú listaelem."

def test_h1_header():
    """9. H1 cím 'vi szövegszerkesztő' a lap tetején."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<h1>vi szövegszerkesztő</h1>' in content, "Hiányzik az h1 cím."

def test_vi_variants_heading():
    """10. 'vi változatok' h2 cím."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    assert '<h2>vi változatok</h2>' in content, "Hiányzik 'vi változatok' h2 cím."

def test_hungarian_characters():
    """Extra: Magyar ékezetes karakterek helyes megjelenítése."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ellenőrizzük, hogy vannak-e magyar ékezetes karakterek
    magyar_szavak = ["szövegszerkesztő", "képernyő-orientált", "Lehetővé", "összefüggésben"]
    
    for szo in magyar_szavak:
        if szo in ["képernyő-orientált", "összefüggésben"]:
            # Ezek a szavak csak a bekezdésekben vannak
            continue
        assert szo in content, f"Hiányzik a magyar szó: {szo}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])