# Feladat 005 - FreeBSD Projekt

Ez a projekt a **FreeBSD** operációs rendszerről szóló weboldal feladatait tartalmazza.

## Elvégzendő feladatok
1. Állítsa be az oldal nyelvét magyarra.
2. Állítson be, olyan karakterkódolást, amelyben az összes magyar ékezetes megjeleníthető.
3. Állítsa be, hogy a böngészőfülön a „FreeBSD” felirat jelenjen meg.
4. Állítson be a szöveg előtt egyes szintű fejezetcímet, „FreeBSD” tartalommal.
5. A „hasonlóság” megjegyzéssel ellátott bekezdésben a FreeBSD szót, jelölje félkövérnek.
6. Ahol felsorolás van, tagolja az elemeket vesszővel, a végén ponttal.
a. GNOME-tól Xfce-ig, és openbox-tól bspwm-ig.
7. A „hasonlóság” tartalmú megjegyzés alatti bekezdésben
a. a „FreeBSD” szót jelölje kiemeltnek
8. A „FreeBSD” tartalmú megjegyzés alatti bekezdésben
a. a „Berkeley Software Distribution” szavakat jelölje félkövérnek, és dőltnek
9. A weboldal alján helyezze el egy általános blokk elemben a nevét és az aktuális dátumot.

## Tesztelés
Futtasd a következő parancsot:
```bash
pytest test_freebsd.py