# Feladat 006 - HP-UX

## Elvégzendő lépések:
1. **Nyelv**: Az oldal nyelve magyar (`hu`).
2. **Böngésző fül**: A cím (`title`) legyen `HP-UX`.
3. **Főcím**: Az első bekezdés előtt egy `<h1>HP-UX</h1>` fejezetcím.
4. **Alcímek**: Minden fejezet előtt `<h2>` cím, a felette lévő megjegyzés szövegével.
5. **Kiemelés**: A „Hewlett Packard Unix” szöveg legyen kiemelt (`strong`).
6. **Rövidítés**: A „HP-UX” szöveg legyen rövidítés (`abbr`).
7. **Forráskód megjegyzés**: A név és az aktuális dátum szerepeljen HTML kommentben.
8. **Félkövér**: Az első bekezdésben a „Unix operációs” szöveg legyen félkövér.
9. **Dőlt**: Az utolsó bekezdésben a „VxFS” szöveg legyen dőlt (toldalék nélkül).

## Tesztelés:
```bash
pytest -v test_index.py