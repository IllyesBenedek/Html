# Feladat 001 - Szolimán

## Elvégzendő lépések:
1. **Tartalom**: A `szoveg.txt` tartalmát illessze a HTML oldal törzs részébe.
2. **Nyelv**: Állítsa be az oldalt magyar (`hu`) nyelvűre.
3. **Cím**: A böngészőfülön a „Szolimán” felirat jelenjen meg (`title`).
4. **Főcím**: A szöveg előtt egyes szintű fejezetcím (`<h1>`), „Szolimán” tartalommal.
5. **Bekezdések**: A három bekezdést jelölje HTML bekezdésnek (`p`).
6. **Alcímek**: A bekezdéseknek adjon kettes fejezetcímet (`<h2>`):
   - 1. bekezdés: A szemrehányás
   - 2. bekezdés: A szentkönyv
   - 3. bekezdés: A leborulás
7. **Dőlt**: A „tekintete azalatt” szöveget az első bekezdésben jelölje dőltnek (`i` vagy `em`).
8. **Kiemelt**: A harmadik bekezdésben „A szultán” szövegeket jelölje kiemeltnek (`strong`).
9. **Komment**: A HTML forráskódjában, megjegyzésbe írja a nevét és az aktuális dátumot.

## Tesztelés:
```bash
pytest -v test_szoliman.py
