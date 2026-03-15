from bs4 import BeautifulSoup

HTML_FILE = "index.html"

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")


# 1. feladat – magyar nyelv
def test_1_nyelv_magyar():
    html = load_html()
    assert 'lang="hu"' in html, "FAIL: 1. feladat – A weboldal nyelve nincs magyarra állítva."


# 2. feladat – UTF-8 kódolás
def test_2_utf8():
    html = load_html()
    assert "<meta charset=\"UTF-8\">" in html or "<meta charset=\"utf-8\">" in html, \
        "FAIL: 2. feladat – A kódolás nem UTF-8."


# 3. feladat – title
def test_3_title():
    html = load_html()
    assert "<title>Felszerelés</title>" in html, "FAIL: 3. feladat – A title nem 'Felszerelés'."


# 4. feladat – caption
def test_4_caption():
    caption = soup().find("caption")
    assert caption is not None, "FAIL: 4. feladat – Nincs táblázatfelirat."
    assert caption.text.strip() == "Felszerelés", "FAIL: 4. feladat – A táblázatfelirat nem 'Felszerelés'."


# 5. feladat – táblázat tartalma
def test_5_table_content():
    rows = soup().find_all("tr")

    expected = [
        ["Felszerelés", "Állapot", "Ár", "Összesen"],
        ["Fényképezőgép", "Újszerű", "10000 Ft", "110000 Ft"],
        ["Telefontöltő", "Használható", "20000 Ft", ],
        ["Tv távirányító", "Rossz állapotban", "30000 Ft", ],
        ["Laptop", "Új", "50000 Ft", ]
    ]

    for i, row in enumerate(expected):
        cells = rows[i].find_all(["th", "td"])
        for j, value in enumerate(row):
            assert cells[j].text.strip() == value, \
                f"FAIL: 5. feladat – Tartalmi hiba a(z) {i+1}. sor {j+1}. cellájában."


# 6. feladat – padding
def test_6_padding():
    html = load_html()
    assert "padding" in html, "FAIL: 6. feladat – Nincs padding beállítva."
