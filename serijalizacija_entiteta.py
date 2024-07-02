from rezervacije_prodaje import generisanje_sedista
from implementacija_entiteta import generisanje_ids
from datetime import datetime, timedelta

def ucitaj_filmove(svi_filmovi):
    fajl = open("Svi entiteti/filmovi.txt", encoding="utf8")

    for linija in fajl:
        linija = linija.replace("\n","").split("|")
        ids = int(linija[0])
        svi_filmovi[ids] = {
            "Ime": linija[1],
            "Žanr": linija[2],
            "Trajanje": linija[3],
            "Režiseri": linija[4],
            "Glavne uloge": linija[5],
            "Zemlja porekla": linija[6],
            "Godina proizvodnje": linija[7],
            "Opis": linija[8],
            "Validnost": linija[9]
        }
    fajl.close()

def ucitaj_sve_projekcije(sve_projekcije, svi_filmovi):
    fajl = open("Svi entiteti/projekcije.txt", encoding="utf8")

    for linija in fajl:
        linija = linija.replace("\n","").split("|")
        ids = int(linija[0])
        generator = generisanje_ids()
        if svi_filmovi[int(linija[5])]["Validnost"] == "NEVALIDNO":
            linija[8] = "NEVALIDNO"
        sve_projekcije[ids] = {
            "Sala": linija[1],
            "Početak": linija[2],
            "Kraj": linija[3],
            "Dani": linija[4],
            "ID filma": linija[5],
            "Film": linija[6],
            "Cena karte": linija[7],
            "Validnost": linija[8],
            "Fabrika": generator
            }
    fajl.close()

def sacuvaj_projekcije(sve_projekcije):
    with open("Svi entiteti/projekcije.txt", "w", encoding="utf8") as fajl:
        for sifra_projekcije, podaci in sve_projekcije.items():
            fajl.write(f'{sifra_projekcije}|{podaci["Sala"]}|{podaci["Početak"]}|{podaci["Kraj"]}|{podaci["Dani"]}|{podaci["ID filma"]}|{podaci["Film"]}|{podaci["Cena karte"]}|{podaci["Validnost"]}\n')

def ucitaj_sve_termine_projekcije(svi_termini_projekcija, sve_projekcije, sve_sale):
    dani = ["ponedeljak", "utorak", "sreda", "četvrtak", "petak", "subota", "nedelja"]
    with open("Svi entiteti/termini_projekcija.txt", encoding="utf8") as fajl:
        for linija in fajl:
            if len(linija) == 0:
                continue
            linija = linija.strip().split("|")
            sifra_termina = linija[0]
            datum_termina = linija[1]
            validnost_termina = linija[2]
            projekcija = sve_projekcije[int(sifra_termina[:-2])]
            next(projekcija["Fabrika"])

            sala = projekcija["Sala"]
            pocetak_projekcije = projekcija["Početak"]
            kraj_projekcije = projekcija["Kraj"]
            dan = datetime.strptime(datum_termina, "%d.%m.%Y.").weekday()
            dan_projekcije = dani[dan]
            id_filma = projekcija["ID filma"]
            ime_filma = projekcija["Film"]
            cena_karte = projekcija["Cena karte"]

            str_format = f"{datum_termina} {pocetak_projekcije}"
            datum_pocetka_novi = datetime.strptime(str_format, "%d.%m.%Y. %H:%M")
            sad = datetime.now()
            if sad > datum_pocetka_novi: 
                validnost_termina = "NEVALIDNO"
            else: 
                validnost_termina = "VALIDNO"
            red = int(sve_sale[sala]["Broj redova"])
            kolona = int(sve_sale[sala]["Broj kolona"])
            sedista = generisanje_sedista(red, kolona)
            svi_termini_projekcija[sifra_termina] = {
                "Datum projekcije": datum_termina,
                "Sala": sala,
                "Početak projekcije": pocetak_projekcije,
                "Kraj projekcije": kraj_projekcije,
                "Dan projekcije": dan_projekcije,
                "ID filma": id_filma,
                "Ime filma": ime_filma,
                "Cena karte": cena_karte,
                "Validnost": validnost_termina,
                "Sedišta": sedista
            }

    sacuvaj_termine(svi_termini_projekcija)

def ucitaj_sve_sale(sve_sale):
    with open("Svi entiteti/sale.txt", encoding="utf8") as fajl:
        for linija in fajl:
            linija = linija.split("|")
            ime_sale = linija[0]
            sve_sale[ime_sale] = {
                "Broj redova": linija[1],
                "Broj kolona": linija[2]
            }

def sacuvaj_termine(svi_termini_projekcija):
    with open("Svi entiteti/termini_projekcija.txt", "w", encoding="utf8") as fajl:
        for sifra_termina, podaci in svi_termini_projekcija.items():
            fajl.write(f'{sifra_termina}|{podaci["Datum projekcije"]}|{podaci["Validnost"]}\n')

def ucitaj_sve_karte(sve_karte, svi_termini_projekcija):
    with open("Svi entiteti/karte.txt", encoding="utf8") as fajl:
        for linija in fajl:
            linija = linija.replace("\n", "").split("|")
            if linija[0] == "":
                break
            id_karte = int(linija[0])
            str_format = f'{svi_termini_projekcija[linija[2]]["Datum projekcije"]} {svi_termini_projekcija[linija[2]]["Početak projekcije"]}'
            datum_pocetka_novi = datetime.strptime(str_format, "%d.%m.%Y. %H:%M")
            sad = datetime.now()
            if sad > datum_pocetka_novi: 
                linija[6] = "NEVALIDNA"
            sve_karte[id_karte] = {
                "Korisnik": linija[1],
                "Šifra termina": linija[2],
                "Sedište": linija[3],
                "Datum prodaje": linija[4],
                "Status karte": linija[5],
                "Validnost": linija[6],
                "Prodavac": linija[7],
                "Cena karte": linija[8],
                "Uloga": linija[9]
            }

    with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
        for id_karte, podaci in sve_karte.items():
            fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                int(id_karte), podaci["Korisnik"], podaci["Šifra termina"],
                podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
            )

def ucitaj_datum_generisanja(svi_termini_projekcija):
    lista = []
    datum_poredjenje = datetime.strptime("01.01.1900.", "%d.%m.%Y.")
    for id, podaci in svi_termini_projekcija.items():
        datum = podaci["Datum projekcije"]
        datum_novi = datetime.strptime(datum, "%d.%m.%Y.")
        if datum_novi > datum_poredjenje:
            lista.append(datum_novi)
    try:
        datum_generisanje = max(lista) + timedelta(days=1)
    except ValueError:
        datum_generisanje = ""
    return datum_generisanje