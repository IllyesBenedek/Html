# Feladat 003 - AIX

## Elvégzendő lépések:
1. **Tartalom**: Az `aix.txt` állomány tartalmának beillesztése a HTML oldal törzs részébe.
2. **Nyelv**: Az oldal nyelvének beállítása magyarra (`lang="hu"`).
3. **Cím**: A böngészőfülön (title) az „AIX” felirat jelenjen meg.
4. **Főcím**: A szöveg előtt egyes szintű fejezetcím (h1) szerepeljen „AIX” tartalommal.
5. **Tagolás**: A beillesztett szöveget három különálló bekezdésre (p) kell bontani.
6. **Alcímek**: A bekezdések előtt 2-es szintű fejezetcímek (h2) legyenek: `Egy`, `Kettő`, `Három`.
7. **Kiemelés**: Az „Advanced Interactive eXecutive” szavakat együtt kell félkövérrel jelölni.
8. **Globális kiemelés**: Az összes „AIX” szónak kiemeltnek (félkövérnek) kell lennie a szövegben.
9. **Komment**: A HTML forráskód végén megjegyzésben szerepeljen a név és az aktuális dátum.

## Tesztelés:
A feladat ellenőrzése a `test_unix.py` fájllal történik. A teszt reguláris kifejezést használ a dátumhoz, így bármilyen napon elfogadja a megjegyzést.
```bash
pytest -v test_unix.py