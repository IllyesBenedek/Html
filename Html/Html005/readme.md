# Feladat 005 - FreeBSD Projekt

Ez a projekt a **FreeBSD** operációs rendszerről szóló weboldal feladatait tartalmazza.

## Elvégzendő feladatok
1. Az oldal nyelvének beállítása magyarra (`hu`).
2. Karakterkódolás beállítása (UTF-8) a magyar ékezetekhez.
3. Böngészőfül címe: `FreeBSD`.
4. Első szintű fejezetcím (`<h1>`): `FreeBSD`.
5. A "hasonlóság" megjegyzés alatti bekezdésben a `FreeBSD` szó félkövér (`<strong>`).
6. Felsorolások tagolása vesszővel, a végén ponttal (GNOME-tól Xfce-ig, és Openbox-tól bspwm-ig).
7. A "hasonlóság" megjegyzés alatti bekezdésben a `FreeBSD` szó kiemelt (`<mark>`).
8. A "FreeBSD" megjegyzés alatti bekezdésben a `Berkeley Software Distribution` egyszerre félkövér és dőlt (`<strong><em>`).
9. A weboldal alján a név és az aktuális dátum egy blokk elemben (`<div>`).

## Tesztelés
Futtasd a következő parancsot:
```bash
pytest test_freebsd.py