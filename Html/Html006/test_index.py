import pytest
from bs4 import BeautifulSoup
import os
import re

@pytest.fixture
def html_soup():
    path = "index.html"
    if not os.path.exists(path):
        pytest.fail(f"{path} nem található!")
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def test_01_nyelv_magyar(html_soup):
    # 1. Állítsa be az oldal nyelvét magyarra.
    assert html_soup.html.get("lang") == "hu"

def test_02_title_hpux(html_soup):
    # 2. Állítsa be, hogy a böngészőfülön a HP-UX felirat jelenjen meg.
    assert html_soup.title.text.strip() == "HP-UX"

def test_03_h1_hpux(html_soup):
    # 3. Weblap tetején egyes szintű fejezetcím, HP-UX tartalommal.
    h1 = html_soup.find("h1")
    assert h1 is not None and h1.text.strip() == "HP-UX"

def test_04_h2_alcimek(html_soup):
    # 4. Minden fejezet előtt legyen egy kettes szintű fejezetcím.
    expected = {"A HP-UX", "Korábbi verziók", "Fájlrendszer"}
    actual = {tag.text.strip() for tag in html_soup.find_all("h2")}
    hianyzo = expected - actual
    assert not hianyzo, f"Hiba! Ez hiányzik: {', '.join(hianyzo)}"
    assert len(actual) == 3, f"Hiba: {len(actual)} alcím van a 3 helyett!"

def test_05_mark_hewlett_packard(html_soup):
    # 5. Jelölje kiemeltnek (mark) a Hewlett Packard Unix szöveget.
    assert html_soup.find("mark", string=re.compile("Hewlett Packard Unix")) is not None

def test_06_abbr_hpux(html_soup):
    # 5/b. A HP-UX szöveg jelölése rövidítésnek (abbr).
    assert html_soup.find("abbr", string="HP-UX")
    p_tags = html_soup.find_all("p")
    assert len(p_tags) == 3, f"Hiba: {len(p_tags)} bekezdés (<p>) van a 3 helyett!"

def test_07_komment_adatok(html_soup):
    # 7. HTML forráskódban megjegyzésben név és dátum.
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert re.search(r"<!--.*202[0-9].*-->", content) is not None

def test_08_strong_unix_operacios(html_soup):
    # 8. Az első bekezdésben a „Unix operációs” szó legyen félkövér.
    first_p = html_soup.find_all("p")[0]
    target = first_p.find(["strong", "b"], string=re.compile("Unix operációs"))
    assert target is not None

def test_09_em_vxfs(html_soup):
    # 9. Az utolsó bekezdésben a „VxFS-t” szöveg legyen dőlt.
    last_p = html_soup.find_all("p")[-1]
    target = last_p.find(["em", "i"], string=re.compile("VxFS"))
    assert target is not None
