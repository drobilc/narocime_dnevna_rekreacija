import narocime
from datetime import datetime, timedelta

# Ustvarimo uporabnika s katerim se bomo prijavljali na vadbo
uporabnik = narocime.User("ime", "priimek", "email", "telefon", "vpisna_stevilka", "naziv_fakultete")

# Ustvarimo klienta za upravljanje z vadbami
klient = narocime.Client()

# Ustvarimo iskanje za vse vadbe, ki bodo potekale danes med 14:00 in 16:00
zacetek = datetime.now().replace(hour=13, minute=00)
konec = zacetek + timedelta(hours=3)

# Poiscemo vse dogodke, ki bodo potekali v tem casovnem intervalu
dogodki = klient.getEvents(zacetek, konec)

# Najdemo samo dogodke, ki imajo naslov 'Fitnes'
fitnesDogodki = list(filter(lambda dogodek: dogodek.title == 'Fitnes' and dogodek.start >= zacetek and dogodek.end <= konec, dogodki))

# Preveri ali sploh je kaksen tak dogodek
if len(fitnesDogodki) > 0:
	# Najdemo prvi dogodek na katerega se bomo prijavili
	dogodek = fitnesDogodki[0]

	print("Prijava na dogodek {}, ki traja od {} do {}.".format(dogodek.title, dogodek.start, dogodek.end))

	# Prijavimo se na dogodek
	rezultat = klient.signup(uporabnik, dogodek)