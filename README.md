# naroci.me - Dnevna rekreacija
Knjižnica pred vami omogoča prijavo na dnevno rekreacijo univerze v Ljubljani s pomočjo programskega jezika Python.

## Namestitev
Knjižnjico lahko namestimo tako, da si prenesemo ta repozitorij, nato pa datoteko `narocime.py` kopiramo v mapo v kateri jo želimo uporabiti.

## Uporaba knjižnice
Za uporabo knjižnice je potrebno naprej vključiti knjižnico. To storimo tako, da na vrh svojega programa dodamo
```python
import narocime
```

Za prijavo je potrebno najprej ustvariti uporabnika. To storimo tako, da ustvarimo objekt tipa `User` in mu nastavimo atribute `first_name`, `last_name`, `email`, `phone`, `vpisna_stevilka`, `fakulteta`.
```python
uorabnik = User("Miha", "Petek", "miha.petek@gmail.com", "040123456", "70170000", "Fakulteta za elektrotehniko")
```

Da se lahko prijavimo na vadbo je najprej potrebno ustvariti še klienta. To storimo na naslednji način.
```python
klient = narocime.Client()
```

Ko imamo ustvarjenega klienta, lahko pridobimo seznam vadb tako, da pokličemo funkcijo `getEvents` kot argumente pa navedemo interval iskanja.
```python
# Vkljucimo knjiznjico datetime za datume
from datetime import datetime, timedelta

# Najdemo trenutni datum in cas
zacetek = datetime.now()

# Trenutnemu casu dodamo 1 dan
konec = zacetek + timedelta(days=1)

# Poiscemo vse vadbe, ki se bodo izvajale med danes in jutri
dogodki = klient.najdiDogodke(zacetek, konec)
```

Z uporabo klienta se lahko sedaj prijavljamo, odjavljamo ter iščemo vadbe na katere se je mogoče prijaviti.
Na voljo so nam naslednje funkcije:
 * `getEvents(dateFrom, dateTo)` - vrne seznam vadb (objektov tipa `Event`) na katere se lahko prijavimo. `dateFrom` in `dateTo` sta objekta tipa `datetime` in označujeta dolžino intervala za iskanje vadb.
 * `signup(user, event)` - prijavi uporabnika user (objekt tipa `User`) na vadbo event (objekt tipa `Event`).
 * `cancel(eventResult)` - odjavi nas od vadbe, pri zahteva atribut `eventResult`, ki ga prejmemo pri klicu funkcije `signup`.

## Primeri
V mapi `examples` se nahajata dva primera uporabe knjižnice:
 * `primer.py` - ob zagonu poišče vadbe, ki potekajo danes med `13:00` in `16:00` in nosijo naslov `Fitnes` in se prijavi na prvo tako vadbo.
 * `primer_obvestilo.py` - naredi podobno kot `primer.py`, le da nam pri tem pošlje še obvestilo na telefon s pomočjo knjižnice `pushbullet` (za uporabo je potrebno torej namestiti to knjižnico in si kopirati API ključ).