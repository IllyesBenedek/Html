import pytest
from bs4 import BeautifulSoup, Comment
import os

def get_soup():
    file_path = "index.html"
    if not os.path.exists(file_path):
        return BeautifulSoup("", "html.parser")
    with open(file_path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

# 1. Nyelv magyar
def test_lang_hu():
    soup = get_soup()
    assert soup.html.get("lang") == "hu"

# 2. UTF-8 kódolás
def test_encoding_utf8():
    soup = get_soup()
    meta = soup.find("meta", charset=True)
    assert meta and meta["charset"].lower() == "utf-8"

# 3. Title: Repülőgép
def test_title_tag():
    soup = get_soup()
    assert soup.title.string == "Repülőgép"

# 4. H1: Repülőgépek
def test_h1_repulogepek():
    soup = get_soup()
    assert soup.find("h1").get_text().strip() == "Repülőgépek"

# 5. Cessna és Stearman H2 fejezetcímek
def test_h2_titles():
    soup = get_soup()
    h2_tags = [h2.get_text().strip() for h2 in soup.find_all("h2")]
    assert "Cessna" in h2_tags
    assert "Stearman" in h2_tags

# 6. Bekezdések (p) megléte
def test_paragraphs_exist():
    soup = get_soup()
    assert len(soup.find_all("p")) >= 2

# 7. Számozott lista (ol) 6 elemmel
def test_numbered_list():
    soup = get_soup()
    ol = soup.find("ol")
    assert ol is not None
    assert len(ol.find_all("li")) == 6

# 8. Forrás szöveg megjegyzésben
def test_source_is_comment():
    soup = get_soup()
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    assert any("Forrás:" in c for c in comments)

# 9. Cessna szó kiemelt (strong vagy b)
def test_cessna_highlight():
    soup = get_soup()
    p1 = soup.find("p")
    highlight = p1.find(["strong", "b"])
    assert highlight is not None and "Cessna" in highlight.text