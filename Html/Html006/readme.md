# Feladat 006 - HP-UX

## Elvégzendő lépések:
1. **Nyelv**: Az oldal nyelve legyen magyar (`hu`).
2. **Cím**: A böngészőfülön a `HP-UX` felirat jelenjen meg.
3. **Főcím**: A weblap tetején, az első bekezdés előtt egy `<h1>HP-UX</h1>` fejezetcím.
4. **Alcímek**: Minden fejezet előtt egy `<h2>` fejezetcím, aminek a tartalma a felette lévő megjegyzés szövege.
5. **Kiemelés (HP-UX bekezdés)**: A „Hewlett Packard Unix” szöveg legyen kiemelt (`strong`).
6. **Rövidítés**: A „HP-UX” szöveg legyen rövidítés (`abbr`).
7. **Komment**: A HTML forráskódban egy megjegyzésben szerepeljen a neved és az aktuális dátum.
8. **Félkövér**: Az első bekezdésben a „Unix operációs” szöveg legyen félkövér.
9. **Dőlt**: Az utolsó bekezdésben a „VxFS-t” szöveg legyen dőlt.

## Tesztelés:
```bash
pytest -v test_index.py