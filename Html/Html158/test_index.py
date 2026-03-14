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


# 4. feladat – táblázat létezik
def test_4_table_exists():
    table = soup().find("table")
    assert table is not None, "FAIL: 4. feladat – A táblázat nem található."
    print("PASS: 4. feladat – táblázat megtalálva.")


# 5. feladat – padding
def test_5_padding():
    html = load_html()
    assert "padding" in html, "FAIL: 5. feladat – Nincs padding beállítva."
    print("PASS: 5. feladat – padding beállítva.")


# 6. feladat – táblázat tartalma
def test_6_table_content():
    rows = soup().find_all("tr")

    expected = [
        ["Fizetés"],  # 1. sor
        ["Fizetési mód", "Status", "Határidő"],  # 2. sor
        ["Készpénz", "Sikeres", "2023.11.01"],   # 3. sor
        ["Banki átutalás", "Folyamatban", "2023.11.05"],  # 4. sor
        ["Paypal", "Sikeres", "2023.11.03"],  # 5. sor
        ["Hitelkártya", "Sikertelen", "2023.11.02"]  # 6. sor
    ]

    for i, row in enumerate(expected):
        cells = rows[i].find_all(["th", "td"])
        for j, value in enumerate(row):
            assert cells[j].text.strip() == value, \
                f"FAIL: Tartalmi hiba a(z) {i+1}. sor {j+1}. cellájában."

    print("PASS: 6. feladat – táblázat tartalma helyes.")
