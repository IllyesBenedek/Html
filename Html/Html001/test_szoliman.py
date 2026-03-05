import pytest
from bs4 import BeautifulSoup

def test_html_file_exists():
    """
    Ellenőrzi, hogy a szoliman.html fájl létezik-e.
    """
    try:
        with open("szoliman.html", "r", encoding="utf-8") as f:
            assert True
    except FileNotFoundError:
        assert False, "A szoliman.html fájl nem létezik."
    
def test_html_lang_attribute():
    """
    Ellenőrzi, hogy a HTML dokumentum nyelvi attribútuma helyesen van-e beállítva.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        html_tag = soup.find("html")
        assert html_tag is not None, "A html tag hiányzik."
        assert html_tag.get("lang") == "hu", "A nyelvi attribútum nincs 'hu'-ra állítva."
    
def test_title_element():
    """
    Ellenőrzi, hogy a title elem 'Szoliman'-ra van-e állítva.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
         soup = BeautifulSoup(f, "html.parser")
         title_tag = soup.find("title")
         assert title_tag is not None, "A title tag hiányzik."
         assert title_tag.text == "Szoliman", "A title nem 'Szoliman'-ra van állítva."

def test_h1_element():
    """
    Ellenőrzi, hogy az h1 elem jelen van-e és a tartalma "Szoliman".
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        h1_tag = soup.find("h1")
        assert h1_tag is not None, "Az h1 tag hiányzik."
        assert h1_tag.text == "Szoliman", "Az h1 tag tartalma nem megfelelő."

def test_paragraph_elements():
    """
    Ellenőrzi, hogy három bekezdés van-e.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        paragraphs = soup.find_all("p")
        h2_tags = soup.find_all("h2")
        assert len(paragraphs) == 3, "Három bekezdés elemnek kell lennie."
        
def test_paragraph_elements_and_h2_elements():
    """
    Ellenőrzi, hogy három bekezdés van-e és mindegyik előtt egy h2 fejléc.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        paragraphs = soup.find_all("p")
        h2_tags = soup.find_all("h2")
        assert len(paragraphs) == 3, "Három bekezdés elemnek kell lennie."
        assert len(h2_tags) == 3, "Három h2 elemnek kell lennie."
    
        expected_headers = ["A szemrehányás", "A szentkönyv", "A leborulás"]
        for i, h2_tag in enumerate(h2_tags):
           assert h2_tag.text == expected_headers[i], f"A h2 fejléc tartalma a(z) {i}. indexen nem megfelelő."

def test_first_paragraph_emphasis():
    """
    Ellenőrzi, hogy a 'tekintete azalatt' dőlt betűs az első bekezdésben.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        first_paragraph = soup.find_all("p")[0]
        em_tag = first_paragraph.find("i")
        assert em_tag is not None, "Az 'i' tag hiányzik az első bekezdésből."
        assert em_tag.text == "tekintete azalatt", "A dőlt betűs szöveg az első bekezdésben nem megfelelő."

def test_third_paragraph_strong_emphasis():
    """
    Ellenőrzi, hogy az "A szultán" szöveg kiemelt az harmadik bekezdésben.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        third_paragraph = soup.find_all("p")[2]
        strong_tags = third_paragraph.find_all("strong")
        assert len(strong_tags) == 2, "Két strong tagnek kell lennie a harmadik bekezdésben."
        for strong_tag in strong_tags:
            assert strong_tag.text == "A szultán", "A kiemelt szöveg a harmadik bekezdésben nem megfelelő."
        

def test_html_comment():
    """
    Ellenőrzi, hogy a "Vizsgafeladat" komment létezik-e a HTML forráskódban.
    """
    with open("szoliman.html", "r", encoding="utf-8") as f:
        content = f.read()
        assert "<!-- Vizsgafeladat -->" in content, "A 'Vizsgafeladat' komment hiányzik a HTML kódból."

if __name__ == "__main__":
    pytest.main()

