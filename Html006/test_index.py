import os
import re
from datetime import datetime

def test_nyelv():
    """Teszt: az oldal nyelv magyarra van állítva."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'lang="hu"' in content or "lang='hu'" in content

def test_cim():
    """Teszt: böngészőfülön HP-UX."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<title>HP-UX</title>' in content

def test_h1():
    """Teszt: egyes szintű fejezetcím HP-UX."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<h1>HP-UX</h1>' in content

def test_h2_cimek():
    """Teszt: minden bekezdés előtt h2 cím."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<h2>A HP-UX</h2>' in content
    assert '<h2>Korábbi verziók</h2>' in content
    assert '<h2>Fájlrendszer</h2>' in content

def test_rovidites():
    """Teszt: HP-UX rövidítésként jelölve."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<abbr' in content
    assert 'title=' in content
    assert 'Hewlett Packard Unix' in content

def test_kiemeles():
    """Teszt: Hewlett Packard Unix kiemelve."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # <b> vagy <strong> használható
    assert '<b>Hewlett Packard Unix</b>' in content or '<strong>Hewlett Packard Unix</strong>' in content

def test_unix_bold():
    """Teszt: Unix operációs félkövér."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<strong>Unix operációs</strong>' in content

def test_vxfs_italic():
    """Teszt: VxFS-t dőlt."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<em>VxFS-t</em>' in content

def test_komment():
    """Teszt: HTML komment névvel és dátummal."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<!--' in content
    assert '-->' in content
    assert 'Illyés Benedek' in content
    # Dátum ellenőrzése
    date_pattern = r'202[0-9]\.[0-9]{2}\.[0-9]{2}'
    assert re.search(date_pattern, content) is not None

def test_bekezdesek():
    """Teszt: 3 bekezdés."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert content.count('<p>') == 3
    assert content.count('</p>') == 3

def test_minden_szo():
    """Teszt: minden fontos szó szerepel."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    fontos_szavak = ['HP-UX', 'Hewlett Packard Unix', 'Unix System V', 
                     '1984', 'HP 9000', 'PA-RISC', 'HPE Integrity Servers',
                     'Motorolla 68000', 'HP Integral PC', 'ACL', 'Veritas', 'VxFS-t']
    for szo in fontos_szavak:
        assert szo in content, f"Hiányzó szó: {szo}"

def test_struktura():
    """Teszt: helyes struktúra."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Sorrend: h1, h2, p, h2, p, h2, p
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    # Egyszerű struktúra ellenőrzés
    assert '<h1>' in content
    assert content.count('<h2>') >= 3
    assert content.count('<p>') >= 3

if __name__ == "__main__":
    # Manuális futtatáshoz
    import sys
    import inspect
    
    sikeres = 0
    osszes = 0
    
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isfunction(obj) and name.startswith('test_'):
            try:
                obj()
                print(f"✓ {name}")
                sikeres += 1
            except AssertionError as e:
                print(f"✗ {name}: {e}")
            osszes += 1
    
    print(f"\nÖsszesen: {sikeres}/{osszes} teszt sikeres")