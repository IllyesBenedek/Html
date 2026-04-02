from bs4 import BeautifulSoup
import os

HTML_FILE = "lakokocsi.html"
URL_207 = "https://en.wikipedia.org/wiki/Caravan_(trailer)"

def load_html():
    with open(HTML_FILE, encoding="utf-8") as f:
        return f.read()

def soup():
    return BeautifulSoup(load_html(), "html.parser")


# 1. feladat – fájl létezik
def test_1_file_exists():
    assert os.path.exists(HTML_FILE), f"FAIL: 1. feladat – A {HTML_FILE} fájl nem létezik."


# 2. feladat – magyar nyelv
def test_2_lang_hu():
    s = soup().find("html")
    assert s and s.get("lang") == "hu", "FAIL: 2. feladat – A nyelv nincs magyarra állítva (<html lang=\"hu\">)."


# 3. feladat – UTF-8 kódolás
def test_3_utf8():
    html = load_html().lower()
    assert 'charset="utf-8"' in html, "FAIL: 3. feladat – A kódolás nem UTF-8."


# 4. feladat – 'lakókocsi' link szövege az első mondatban
def test_4_lakokocsi_link_szoveg():
    s = soup()
    # Keressük a linket a szöveg alapján
    a = s.find("a", string=lambda t: t and "lakókocsi" in t.lower())
    assert a is not None, "FAIL: 4. feladat – A 'lakókocsi' szó nincs linkké (<a>) alakítva."


# 5. feladat – link URL helyes
def test_5_link_url():
    s = soup()
    a = s.find("a", string=lambda t: t and "lakókocsi" in t.lower())
    assert a is not None and a["href"] == URL_207, \
        f"FAIL: 5. feladat – A hivatkozás URL-je hibás. (Várt: {URL_207})"


# 6. feladat – új lapon nyíljon meg (target="_blank")
def test_6_target_blank():
    s = soup()
    a = s.find("a", string=lambda t: t and "lakókocsi" in t.lower())
    assert a is not None and a.get("target") == "_blank", \
        "FAIL: 6. feladat – A link nem nyílik új lapon (hiányzik a target=\"_blank\")."


# 7. feladat – a bekezdés szövege pontos
def test_7_szoveg_tartalom():
    text = soup().get_text()
    assert "önerejéből mozgásra képtelen" in text, "FAIL: 7. feladat – A szöveg eleje hibás vagy hiányzik."
    assert "konyha, wc, hálóhely, zuhany" in text, "FAIL: 7. feladat – A felsorolás hibás vagy hiányzik."
    assert "régi lovas karavánokhoz" in text, "FAIL: 7. feladat – A szöveg vége hibás vagy hiányzik."
