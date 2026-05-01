# Feladat 001 - Szoliman oldal összeállítása

A feladat során a megadott források alapján egy strukturált HTML oldalt kell létrehozni.

## Elvégzendő feladatok:
1. **Tartalom beillesztése**: Másold be a szöveget az `index.html` törzsébe.
2. **Nyelv beállítása**: Állítsd be az oldal nyelvét magyarra (`hu`).
3. **Böngésző fül címe**: A `<title>` elem tartalma legyen "Szoliman".
4. **Főcím**: Szúrj be egy `h1` fejezetcímet "Szoliman" tartalommal a szöveg elé.
5. **Bekezdések**: A szöveget tagold három különálló `<p>` elemre.
6. **Alcímek**: Minden bekezdés kapjon egy `h2` szintű alcímet: *A szemrehányás*, *A szentkönyv*, *A leborulás*.
7. **Dőlt formázás**: Az első bekezdésben a "tekintete azalatt" szöveget tedd döltté.
8. **Kiemelés**: A harmadik bekezdésben "A szultán" kifejezéseket jelöld kiemeltként (félkövér).
9. **Dokumentáció**: A forráskódban megjegyzésként tüntesd fel a nevedet és az aktuális dátumot.

## Ellenőrzés
Futtasd a tesztet a terminálban:
```bash
pytest -v test_solution.py