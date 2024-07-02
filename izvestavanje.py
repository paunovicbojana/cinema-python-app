from prettytable import *
from datetime import datetime, timedelta
from rich.console import Console
console = Console()

def izvestaj_a(sve_karte, svi_termini_projekcija):
    tabela = PrettyTable()
    tabela.field_names = ["Šifra karte", "Datum prodaje", "Kupac", "Termin projekcije", "Datum termina projekcije", "Sedište", "Cena karte", "Prodavac"]

    while True:
        datum_unos = input("\nUnesite željeni datum prodaje za izveštavanje (npr. 21.01.2024.): ").lower().strip()

        if datum_unos == "x":
            console.print("[bright_red]\nOTKAZANO.\n[/]")
            break

        i = 0

        with open("Izveštaji/izvestaj_a.txt", "w", encoding="utf8") as fajl:
            for id, podaci in sve_karte.items():
                if datum_unos in podaci["Datum prodaje"].lower() and podaci["Status karte"] == "PRODATA":
                    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                                                                id, podaci["Datum prodaje"], podaci["Korisnik"], podaci["Šifra termina"], 
                                                                svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"], 
                                                                podaci["Sedište"], podaci["Cena karte"], podaci["Prodavac"])
            )
                
                    tabela.add_row([id, podaci["Datum prodaje"], podaci["Korisnik"], podaci["Šifra termina"], 
                                    svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"], 
                                    podaci["Sedište"], podaci["Cena karte"], podaci["Prodavac"]])
                    i += 1

        if i == 0:  
            console.print("[bright_red]\nNema prodate karte za ovaj datum.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        print()
        print(tabela)
        print()
        break

def izvestaj_b(sve_karte, svi_termini_projekcija):
    tabela = PrettyTable()
    tabela.field_names = ["Šifra karte", "Datum prodaje", "Kupac", "Termin projekcije", "Datum termina projekcije", "Sedište", "Cena karte", "Prodavac"]

    while True:
        datum_unos = input("\nUnesite željeni datum termina projekcije za izveštavanje (npr. 21.01.2024.): ").lower().strip()

        if datum_unos == "x":
            console.print("[bright_red]\nOTKAZANO.\n[/]")
            break

        i = 0

        with open("Izveštaji/izvestaj_b.txt", "w", encoding="utf8") as fajl:
            for id, podaci in sve_karte.items():
                if datum_unos in svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"].lower() and podaci["Status karte"] == "PRODATA":
                    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                                                                id, podaci["Datum prodaje"], podaci["Korisnik"], podaci["Šifra termina"], 
                                                                svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"], 
                                                                podaci["Sedište"], podaci["Cena karte"], podaci["Prodavac"])
            )
                    tabela.add_row([id, podaci["Datum prodaje"], podaci["Korisnik"], podaci["Šifra termina"], 
                                    svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"], 
                                    podaci["Sedište"], podaci["Cena karte"], podaci["Prodavac"]])
                    i += 1

        if i == 0:  
            console.print("[bright_red]\nNema prodate karte za ovaj datum.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        print()
        print(tabela)
        print()
        break

def izvestaj_c(sve_karte, svi_termini_projekcija, svi_korisnici):
    tabela = PrettyTable()
    tabela.field_names = ["Šifra karte", "Datum prodaje", "Kupac", "Termin projekcije", "Datum termina projekcije", "Sedište", "Cena karte"]

    while True:
        datum_unos = input("\nUnesite željeni datum prodaje za izveštavanje (npr. 21.01.2024.): ").lower().strip()
        tabela_prodavac = PrettyTable()
        tabela_prodavac.field_names = ["Broj", "Korisničko ime", "Ime i prezime"]

        brojac = 1
        lista = []
        for kor_ime, podaci in svi_korisnici.items():
            if podaci["Uloga"] != "Prodavac":
                continue
            ime_prezime = podaci["Ime"] + " " + podaci["Prezime"]
            tabela_prodavac.add_row([brojac, kor_ime, ime_prezime])
            lista.append(kor_ime)
            brojac += 1

        print()
        print(tabela_prodavac)

        uneseni_broj = input("\nUnesite broj željenog prodavca za izveštavanje: ").lower().strip()
        if datum_unos == "x":
            console.print("[bright_red]\nOTKAZANO.\n[/]")
            break
        if uneseni_broj == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return

        try:
            uneseni_broj = int(uneseni_broj) - 1 
            
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]")
            continue
        if uneseni_broj not in range(brojac):
            console.print("[bright_red]\nUnesite jednu od dostupnih opcija.[/]")
            continue
        prodavac = lista[uneseni_broj]

        i = 0

        with open("Izveštaji/izvestaj_c.txt", "w", encoding="utf8") as fajl:
            for id, podaci in sve_karte.items():
                if datum_unos in podaci["Datum prodaje"].lower() and podaci["Status karte"] == "PRODATA":
                    if podaci["Prodavac"] != prodavac:
                        continue
                    fajl.write("{}|{}|{}|{}|{}|{}|{}\n".format(
                                                                id, podaci["Datum prodaje"], podaci["Korisnik"], podaci["Šifra termina"], 
                                                                svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"], 
                                                                podaci["Sedište"], podaci["Cena karte"])
            )
                
                    tabela.add_row([id, podaci["Datum prodaje"], podaci["Korisnik"], podaci["Šifra termina"], 
                                    svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"], 
                                    podaci["Sedište"], podaci["Cena karte"]])
                    i += 1

        if i == 0:  
            console.print("[bright_red]\nNema prodate karte za ovaj datum i željenog prodavca.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        print()
        print(tabela)
        print()
        break

def izvestaj_e(sve_karte, svi_termini_projekcija):
    tabela = PrettyTable()
    tabela.field_names = ["Ukupan broj", "Ukupna cena"]

    while True:
        unos = input("\nUnesite broj željenog dana za izveštavanje (ponedeljak = 1 itd.): ").lower().strip()

        if unos == "x":
            console.print("[bright_red]\nOTKAZANO.\n[/]")
            break

        dani = [
            "ponedeljak",
            "utorak",
            "sreda",
            "četvrtak",
            "petak",
            "subota",
            "nedelja"
        ]

        try:
            unos = int(unos) - 1 
            
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]")
            continue
        if unos not in range(len(dani)):
            console.print("[bright_red]\nUnesite jednu od dostupnih opcija.[/]")
            continue
        dan = dani[unos]

        i = 0
        ukupna_cena = 0.0
        for id, podaci in sve_karte.items():
            if dan == svi_termini_projekcija[podaci["Šifra termina"]]["Dan projekcije"] and podaci["Status karte"] == "PRODATA":
                ukupna_cena += float(podaci["Cena karte"])
                i += 1

        if i == 0:  
            console.print("[bright_red]\nNema prodatih karata za termin projekcije koje se održavaju na ovaj dan u nedelji.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        with open("Izveštaji/izvestaj_e.txt", "w", encoding="utf8") as fajl:
            fajl.write("{}|{}\n".format(i, ukupna_cena))
        tabela.add_row([i, ukupna_cena])

        print()
        print(tabela)
        print()
        break

def izvestaj_d(sve_karte):
    tabela = PrettyTable()
    tabela.field_names = ["Ukupan broj", "Ukupna cena"]

    while True:
        unos = input("\nUnesite broj željenog dana za izveštavanje (ponedeljak = 1 itd.): ").lower().strip()

        if unos == "x":
            console.print("[bright_red]\nOTKAZANO.\n[/]")
            break

        dani = [
            "ponedeljak",
            "utorak",
            "sreda",
            "četvrtak",
            "petak",
            "subota",
            "nedelja"
        ]

        try:
            unos = int(unos) - 1 
            
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]")
            continue
        if unos not in range(len(dani)):
            console.print("[bright_red]\nUnesite jednu od dostupnih opcija.[/]")
            continue
        dan = dani[unos]

        i = 0
        ukupna_cena = 0.0
        for id, podaci in sve_karte.items():
            dan_prodaje = datetime.strptime(podaci["Datum prodaje"], "%d.%m.%Y.").weekday()
            dan_prodaje = dani[dan_prodaje]
            if dan == dan_prodaje and podaci["Status karte"] == "PRODATA":
                ukupna_cena += float(podaci["Cena karte"])
                i += 1

        if i == 0:  
            console.print("[bright_red]\nNema prodatih karata za ovaj dan u nedelji.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        with open("Izveštaji/izvestaj_d.txt", "w", encoding="utf8") as fajl:
            fajl.write("{}|{}\n".format(i, ukupna_cena))
        tabela.add_row([i, ukupna_cena])

        print()
        print(tabela)
        print()
        break

def izvestaj_f(sve_karte, svi_termini_projekcija):
    tabela = PrettyTable()
    tabela.field_names = ["Ukupna cena", "Ime filma"]

    while True:
        unikatno = []
        tabela_film = PrettyTable()
        tabela_film.field_names = ["Broj", "Ime filma"]

        brojac = 1
        for film_id, film in svi_termini_projekcija.items():
            ime_filma = film["Ime filma"]
            if ime_filma not in unikatno:
                tabela_film.add_row([brojac, ime_filma])
                unikatno.append(ime_filma)
                brojac += 1

        print()
        print(tabela_film)
        
        uneseni_broj = input("\nUnesite broj željenog filma: ").lower().strip()

        if uneseni_broj == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return

        try:
            uneseni_broj = int(uneseni_broj) - 1
            
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]\n")
            continue
        if uneseni_broj not in range(len(unikatno)):
            console.print("[bright_red]\nUnesite jednu od dostupnih opcija.[/]\n")
            continue
        ime_filma = unikatno[uneseni_broj]

        i = 0
        ukupna_cena = 0.0

        with open("Izveštaji/izvestaj_f.txt", "w", encoding="utf8") as fajl:
            for id, podaci in sve_karte.items():
                if ime_filma.lower() == svi_termini_projekcija[podaci["Šifra termina"]]["Ime filma"].lower() and podaci["Status karte"] == "PRODATA":
                    ukupna_cena += float(podaci["Cena karte"])
                    i += 1
            fajl.write("{}|{}\n".format(ukupna_cena, ime_filma))
            tabela.add_row([ukupna_cena, ime_filma])
                

        if i == 0:  
            console.print("[bright_red]\nNema prodate karte za ovaj film.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        print()
        print(tabela)
        print()
        break

def izvestaj_g(sve_karte, svi_korisnici):
    tabela = PrettyTable()
    tabela.field_names = ["Ukupan broj", "Ukupna cena", "Korisničko ime prodavca"]

    while True:
        unos = input("\nUnesite broj željenog dana za izveštavanje (ponedeljak = 1 itd.): ").lower().strip()

        if unos == "x":
            console.print("[bright_red]\nOTKAZANO.\n[/]")
            break
        
        try:
            unos = int(unos) - 1 
            
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]")
            continue

        dani = [
            "ponedeljak",
            "utorak",
            "sreda",
            "četvrtak",
            "petak",
            "subota",
            "nedelja"
        ]

        if unos not in range(len(dani)):
            console.print("[bright_red]\nUnesite jednu od dostupnih opcija.[/]")
            continue
         
        dan = dani[unos]

        tabela_prodavac = PrettyTable()
        tabela_prodavac.field_names = ["Broj", "Korisničko ime", "Ime i prezime"]

        brojac = 1
        lista = []
        for kor_ime, podaci in svi_korisnici.items():
            if podaci["Uloga"] != "Prodavac":
                continue
            ime_prezime = podaci["Ime"] + " " + podaci["Prezime"]
            tabela_prodavac.add_row([brojac, kor_ime, ime_prezime])
            lista.append(kor_ime)
            brojac += 1

        print()
        print(tabela_prodavac)

        uneseni_broj = input("\nUnesite broj željenog prodavca za izveštavanje: ").lower().strip()
        
        if uneseni_broj == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return

        try:
            uneseni_broj = int(uneseni_broj) - 1 
            
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]")
            continue
        if uneseni_broj not in range(brojac):
            console.print("[bright_red]\nUnesite jednu od dostupnih opcija.[/]")
            continue
        prodavac = lista[uneseni_broj]

        i = 0
        ukupna_cena = 0.0
        for id, podaci in sve_karte.items():
            dan_prodaje = datetime.strptime(podaci["Datum prodaje"], "%d.%m.%Y.").weekday()
            dan_prodaje = dani[dan_prodaje]
            if prodavac != podaci["Prodavac"]:
                continue
            if dan == dan_prodaje and podaci["Status karte"] == "PRODATA":
                ukupna_cena += float(podaci["Cena karte"])
                i += 1

        if i == 0:  
            console.print("[bright_red]\nNema prodatih karata za ovaj dan u nedelji i željenog prodavca.\n[/]")
            break

        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)

        with open("Izveštaji/izvestaj_g.txt", "w", encoding="utf8") as fajl:
            fajl.write("{}|{}|{}\n".format(i, ukupna_cena, prodavac))
        tabela.add_row([i, ukupna_cena, prodavac])

        print()
        print(tabela)
        print()
        break

def izvestaj_h(sve_karte, svi_korisnici):
    tabela = PrettyTable()
    tabela.field_names = ["Ukupan broj", "Ukupna cena", "Korisničko ime prodavca"]
    with open("Izveštaji/izvestaj_h.txt", "w", encoding="utf8") as fajl:
        for kor_ime, info in svi_korisnici.items():
            if info["Uloga"] != "Prodavac":
                continue
            i = 0
            ukupna_cena = 0.0
            for id, podaci in sve_karte.items():
                if podaci["Prodavac"] != kor_ime:
                    continue
                datum_prodaje = datetime.strptime(podaci["Datum prodaje"], "%d.%m.%Y.")
                if datum_prodaje <= datetime.today() + timedelta(days=30) and podaci["Status karte"] == "PRODATA":
                    ukupna_cena += float(podaci["Cena karte"])
                    i += 1

            fajl.write("{}|{}|{}\n".format(i, ukupna_cena, kor_ime))
            tabela.add_row([i, ukupna_cena, kor_ime])

    tabela.valign = "m"
    tabela.hrules = ALL
    tabela.set_style(DOUBLE_BORDER)

    print()
    print(tabela)
    print()