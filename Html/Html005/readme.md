# Feladat 005 - FreeBSD

## Elvégzendő lépések:
1. **Nyelv**: Magyar (`hu`) nyelv beállítása a html tagben.
2. **Kódolás**: Karakterkódolás beállítása `UTF-8`-ra.
3. **Cím**: A böngészőfülön megjelenő cím: `FreeBSD`.
4. **Főcím**: Az oldal főcíme: `<h1>FreeBSD</h1>`.
5. **Kiemelés**: A „FreeBSD” szó legalább két helyen legyen félkövér (`strong`).
6. **Formázás**: A „Berkeley Software Distribution” szöveg legyen egyszerre félkövér és dőlt (`strong` és `em`).
7. **Tagolás**: Az asztali környezetek és ablakkezelők listáját vesszővel válaszd el, a végén ponttal.
8. **Kommentek**: Használj HTML megjegyzéseket (pl. `<!-- hasonlóság -->`, `<!-- engedély -->`).
9. **Lábléc**: Az oldal alján egy blokk elemben szerepeljen a neved és az aktuális dátum.

## Tesztelés:
A teszteléshez a `test_index.py` fájlt használjuk.
```bash
pytest -v test_index.py