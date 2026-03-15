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
    print("PASS: 1. feladat – magyar nyelv beállítva.")


# 2. feladat – UTF-8 kódolás
def test_2_utf8():
    html = load_html()
    assert "<meta charset=\"UTF-8\">" in html or "<meta charset=\"utf-8\">" in html, \
        "FAIL: 2. feladat – A kódolás nem UTF-8."
    print("PASS: 2. feladat – UTF-8 kódolás rendben.")


# 3. feladat – title
def test_3_title():
    html = load_html()
    assert "<title>Fizetés</title>" in html, "FAIL: 3. feladat – A title nem 'Fizetés'."
    print("PASS: 3. feladat – title helyes.")


# 4. feladat – H1 létezik és 'Fizetés'
def test_4_h1():
    h1 = soup().find("h1")
    assert h1 is not None, "FAIL: 4. feladat – Nincs H1 cím."
    assert h1.text.strip() == "Fizetés", "FAIL: 4. feladat – A H1 szövege nem 'Fizetés'."
    print("PASS: 4. feladat – H1 helyes.")


# 5. feladat – táblázat tartalma (az ábra alapján)
def test_5_table_content():
    rows = soup().find_all("tr")
    assert len(rows) >= 5, "FAIL: 5. feladat – A táblázat nem tartalmazza az összes sort."

    expected = [
        ["Fizetés"],  # 1. sor: címsor (th colspan=3)
        ["Fizetési mód", "Státusz", "Határidő"],
        ["Készpénz", "Sikeres", "2023.11.01."],
        ["Banki átutalás", "Folyamatban", "2023.11.05."],
        ["Paypal", "Sikeres", "2023.11.03."],
        ["Hitelkártya", "Sikertelen", "2023.11.02."]
    ]

    for i, row in enumerate(expected):
        cells = rows[i].find_all(["th", "td"])
        for j, value in enumerate(row):
            assert cells[j].text.strip() == value, \
                f"FAIL: 5. feladat – Tartalmi hiba a(z) {i+1}. sor {j+1}. cellájában."

    print("PASS: 5. feladat – táblázat tartalma helyes.")


# 6. feladat – padding (oszlopnyúlás)
def test_6_padding():
    html = load_html()
    assert "padding" in html, "FAIL: 6. feladat – Nincs padding beállítva."
    print("PASS: 6. feladat – padding beállítva.")
