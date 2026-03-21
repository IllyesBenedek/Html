import os

def test_file_exists():
    assert os.path.exists("index.html"), "index.html nem található"
    assert os.path.exists("feladat.txt"), "feladat.txt nem található"

def test_utf8_encoding():
    # Próbáljuk meg UTF-8-ként beolvasni
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            f.read()
        with open("feladat.txt", "r", encoding="utf-8") as f:
            f.read()
    except UnicodeDecodeError:
        assert False, "A fájl nem UTF-8 kódolású"

def test_link_present():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert '<a href="' in content, "Nincs hivatkozás az index.html-ben"
    assert 'motorcsónaknak</a>' in content, "A motorcsónaknak nincs linkké alakítva"

def test_correct_url():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert 'href="https://hu.wikipedia.org/wiki/Motorcs%C3%B3nak"' in content, "Nem a megfelelő URL-re mutat a link"

def test_no_plain_word_left():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Töröljük a linkelt változatot, és nézzük meg, maradt-e sima szó
    cleaned = content.replace('<a href="https://hu.wikipedia.org/wiki/Motorcs%C3%B3nak">motorcsónaknak</a>', "")
    assert "motorcsónaknak" not in cleaned, "A régi motorcsónaknak szó még szerepel link nélkül"

def test_html_structure():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    assert "<html" in content.lower(), "Hiányzik a <html> tag"
    assert "<body" in content.lower(), "Hiányzik a <body> tag"
    assert "</html>" in content.lower(), "Hiányzik a lezáró </html> tag"
