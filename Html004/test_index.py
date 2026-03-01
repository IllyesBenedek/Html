import os
import re
from datetime import datetime

def test_hpux_tartalom():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd, hogy tartalmazza-e a HP-UX szöveget
    assert 'HP-UX' in content
    assert 'Hewlett Packard Unix' in content
    
def test_nyelv_beallitas():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd, hogy a nyelv magyarra van-e állítva
    assert 'lang="hu"' in content or "lang='hu'" in content
    
def test_cim():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd a címét
    assert '<title>HP-UX</title>' in content
    
def test_fejcim():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd az első szintű fejezetcímet
    assert '<h1>HP-UX</h1>' in content
    
def test_masodik_szintu_fejcim():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd a második szintű fejezetcímet
    assert '<h2>Támogatás</h2>' in content
    
def test_rovidites():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd az rövidítést
    assert '<abbr' in content
    assert 'HP 9000' in content
    
def test_kiemeles():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd a kiemelést
    assert '<b>HP Integral PC</b>' in content
    
def test_komment():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd a HTML kommentet
    assert '<!--' in content
    assert '-->' in content
    assert '2025' in content  # vagy az aktuális év
    
def test_bekezdesek():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ellenőrizd a bekezdéseket
    assert '<p>' in content
    assert '</p>' in content
    # Legalább 2 bekezdésnek kell lennie
    assert content.count('<p>') >= 2