import os
import re
from datetime import datetime

def test_nyelv_beallitas():
    """Teszt: az oldal nyelv magyarra van állítva."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'lang="hu"' in content

def test_karakterkodolas():
    """Teszt: megfelelő karakterkódolás."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'charset="UTF-8"' in content or "charset='UTF-8'" in content
    assert 'utf-8' in content.lower()

def test_cim():
    """Teszt: böngészőfülön FreeBSD."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<title>FreeBSD</title>' in content

def test_h1_fejezetcim():
    """Teszt: egyes szintű fejezetcím FreeBSD tartalommal."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<h1>FreeBSD</h1>' in content

def test_hasonlosag_paragraph_felkover():
    """Teszt: 'hasonlóság' bekezdésben FreeBSD félkövér."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Az első FreeBSD a hasonlóság bekezdésben
    assert '<b>FreeBSD</b>' in content or '<strong>FreeBSD</strong>' in content

def test_felsorolas_vesszovel():
    """Teszt: felsorolások vesszővel tagolva, végén pont."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Asztali környezetek
    assert 'GNOME, KDE, Xfce.' in content
    # Ablakkezelők
    assert 'openbox, fluxbox, dwm, bspwm.' in content

def test_hasonlosag_kiemelt():
    """Teszt: 'hasonlóság' bekezdésben FreeBSD kiemelt."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Minden FreeBSD kiemelve legyen (legalább egy)
    assert '<b>' in content or '<strong>' in content

def test_berkeley_bold_italic():
    """Teszt: Berkeley Software Distribution félkövér és dőlt."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<strong><em>Berkeley Software Distribution</em></strong>' in content
    # vagy külön <strong> és <em> is jó lehet
    assert 'Berkeley Software Distribution' in content

def test_footer():
    """Teszt: név és dátum az oldal alján."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    assert '<footer>' in content
    assert '</footer>' in content
    assert 'Illyés Benedek' in content
    # Dátum ellenőrzése (bármilyen formátum)
    date_pattern = r'202[0-9]\.[0-9]{2}\.[0-9]{2}'
    assert re.search(date_pattern, content) is not None

def test_bekezdesek():
    """Teszt: bekezdések megfelelően jelölve."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    # Legalább 4 bekezdésnek kell lennie
    assert content.count('<p>') >= 4

def test_minden_keresett_szo():
    """Teszt: minden szükséges szó szerepel."""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    keresett_szavak = ['FreeBSD', 'Linux', 'GNOME', 'KDE', 'Xfce', 
                       'openbox', 'fluxbox', 'dwm', 'bspwm',
                       'Berkeley Software Distribution']
    for szo in keresett_szavak:
        assert szo in content, f"Hiányzó szó: {szo}"

if __name__ == "__main__":
    # Manuális futtatáshoz
    import sys
    import inspect
    
    osz = 0
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isfunction(obj) and name.startswith('test_'):
            try:
                obj()
                print(f"✓ {name}")
                osz += 1
            except AssertionError as e:
                print(f"✗ {name}: {e}")
    
    print(f"\nÖsszesen: {osz}/{len([x for x in dir() if x.startswith('test_')])} teszt sikeres")