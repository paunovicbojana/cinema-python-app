from prettytable import *
from datetime import datetime
from rich.console import Console
console = Console()

def ispis_filmova(svi_filmovi):
    tabela = PrettyTable()
    tabela.field_names = ["Ime filma", "Žanr", "Trajanje (min)", "Režiseri", "Glavne uloge", "Zemlja porekla", "Godina proizvodnje"]
    for ids, podaci in svi_filmovi.items():
        ime = podaci["Ime"]
        zanr = "\n".join(podaci["Žanr"].split("/"))
        trajanje = podaci["Trajanje"]
        reziseri = "\n".join(podaci["Režiseri"].split(", "))
        uloge = "\n".join(podaci["Glavne uloge"].split(", "))
        zemlja = "\n".join(podaci["Zemlja porekla"].split("/"))
        godina = podaci["Godina proizvodnje"]
        if "VALIDNO" == podaci["Validnost"]:
            tabela.add_row([ime, zanr, trajanje, reziseri, uloge, zemlja, godina])
    tabela.sortby = "Ime filma"
    tabela.valign = "m"
    tabela.hrules = ALL
    tabela.set_style(DOUBLE_BORDER)
    print()
    print(tabela)
    print()

def pretraga_filmova(svi_filmovi):
    while True:
        print("Nalazite se u meniju za pretragu filmova. Izaberite jedan ili više kriterijuma pretrage odvojenih razmakom.")
        print("    [1] Ime filma")
        print("    [2] Žanr")
        print("    [3] Trajanje (min)")
        print("    [4] Režiseri")
        print("    [5] Glavne uloge")
        print("    [6] Zemlja porekla")
        print("    [7] Godina proizvodnje")
        print("    [x] Otkazivanje")

        izbor = input("\nBiram: ").lower().strip()
        if izbor == "":
            console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")
            continue
            
        izbor = izbor.split()
        uneti_do_sada = []
        for i in izbor:
            if i not in uneti_do_sada:
                uneti_do_sada.append(i)
        
        for i in uneti_do_sada:
            if not i.lower() in ["1", "2", "3", "4", "5", "6", "7", "x"]:
                console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")
                break
            if i == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                return

        else:
            filmovi_za_ispis = set(list(svi_filmovi.keys()))
            promenjeno = False
            pronadjeni_filmovi = set()
            print("Ukoliko želite da prekinete proces pretrage, unesite x.")
            for i in uneti_do_sada:
                if i == "1":
                    ime_filma = input("Unesite ime filma: ").lower().strip()

                    if ime_filma == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue
                        
                    pronadjeni_filmovi = set()
                    for id, podaci in svi_filmovi.items():
                        if ime_filma in podaci["Ime"].lower():
                            pronadjeni_filmovi.add(id)

                    filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                    promenjeno = True
                    continue

                if i == "2":
                    while True:
                        tabela = PrettyTable()
                        tabela.field_names = ["Broj", "Žanrovi"]

                        unikatno = []
                        brojac_zanrova = 1 

                        for id, film_podaci in svi_filmovi.items():
                            zanr_filma_lista = film_podaci["Žanr"].split("/")
                            
                            for zanr_film in zanr_filma_lista:
                                if zanr_film not in unikatno:
                                    tabela.add_row([brojac_zanrova, zanr_film])
                                    unikatno.append(zanr_film)
                                    brojac_zanrova += 1

                        print()
                        print(tabela)

                        zanr_filma_broj = input("\nUnesite broj žanra filma: ")
                        if zanr_filma_broj == "x":
                            console.print("[bright_red]\nOTKAZANO.[/]\n")
                            break
                        try:
                            zanr_filma_broj = int(zanr_filma_broj) - 1
                        except ValueError:
                            console.print("[bright_red]\nUnesite broj.[/]")
                            continue
                        if zanr_filma_broj not in range(len(unikatno)):
                            console.print("[bright_red]\nUnesite ispravan broj.[/]")
                            continue
                    
                        pronadjeni_filmovi = set()

                        for id, podaci in svi_filmovi.items():
                            zanrovi_filma = podaci["Žanr"].split("/")
                            for zanr in zanrovi_filma:
                                if unikatno[zanr_filma_broj] == zanr:
                                    pronadjeni_filmovi.add(id)
                                    break

                        filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                        promenjeno = True
                        break   

                if i == "3":
                    while True:
                        print("\nUkoliko želite da unesete samo jednu granicu, kod unosa druge pritisnite enter.")
                        min_trajanje_filma = input("Unesite minimalno trajanje filma u minutima: ").lower().strip()
                        max_trajanje_filma = input("Unesite maksimalno trajanje filma u minutima: ").lower().strip()

                        if min_trajanje_filma == "x" or max_trajanje_filma == "x":
                            console.print("[bright_red]\nOTKAZANO.[/]\n")
                            break
                        if min_trajanje_filma == "":
                            min_trajanje_filma = 0
                        if max_trajanje_filma == "":
                            max_trajanje_filma = 1000
                        try:
                            min_trajanje_filma = int(min_trajanje_filma)
                            max_trajanje_filma = int(max_trajanje_filma)
                        except ValueError:
                            console.print("[bright_red]\nUnesite broj.[/]")
                            continue
                        
                        pronadjeni_filmovi = set()
                        for id, podaci in svi_filmovi.items():
                            if min_trajanje_filma <= int(podaci["Trajanje"]) <= max_trajanje_filma:
                                pronadjeni_filmovi.add(id)
                        
                        filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                        promenjeno = True
                        break
                        

                if i == "4":
                    reziseri_filma = input("Unesite režisere filma: ").lower().strip()
                    if reziseri_filma == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue

                    pronadjeni_filmovi = set()
                    for id, podaci in svi_filmovi.items():
                        if reziseri_filma in podaci["Režiseri"].lower():
                            pronadjeni_filmovi.add(id)
                    
                    filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                    promenjeno = True
                    continue

                if i == "5":
                    uloge_filma = input("Unesite glavne uloge: ").lower().strip()
                    if uloge_filma == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue

                    pronadjeni_filmovi = set()
                    for id, podaci in svi_filmovi.items():
                        if uloge_filma in podaci["Glavne uloge"].lower():
                            pronadjeni_filmovi.add(id)
                    
                    filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                    promenjeno = True
                    continue

                if i == "6":
                    unikatno = set()
                    tabela = PrettyTable()
                    tabela.field_names = ["Zemlja porekla"]

                    for id, zemlja_film in svi_filmovi.items():
                        zemlja_film_lista = zemlja_film["Zemlja porekla"].split("/")

                        for zemlja_film in zemlja_film_lista:
                            if zemlja_film not in unikatno:
                                tabela.add_row([zemlja_film])
                                unikatno.add(zemlja_film)
                    print()
                    print(tabela)

                    zemlja_filma = input("\nUnesite zemlju porekla filma: ").lower().strip()
                    if zemlja_filma == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue

                    pronadjeni_filmovi = set()
                    for id, podaci in svi_filmovi.items():
                        if zemlja_filma in podaci["Zemlja porekla"].lower():
                            pronadjeni_filmovi.add(id)
                    
                    filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                    promenjeno = True
                    continue

                if i == "7":
                    godina_filma = input("Unesite godinu proizvodnje filma: ").strip()
                    godina_filma = godina_filma.replace(".", "")
                    if godina_filma == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue

                    pronadjeni_filmovi = set()
                    for id, podaci in svi_filmovi.items():
                        if godina_filma == podaci["Godina proizvodnje"]:
                            pronadjeni_filmovi.add(id)
                    
                    filmovi_za_ispis.intersection_update(pronadjeni_filmovi)
                    promenjeno = True
                    continue
                

            trazeni_filmovi = {}
            
            if promenjeno:
                for id, podaci in svi_filmovi.items():
                    if "VALIDNO" == podaci["Validnost"] and id in filmovi_za_ispis:
                        trazeni_filmovi[id] = podaci
                
                if len(trazeni_filmovi) == 0:
                    console.print("[bright_red]\nNema odgovarajućeg podatka pretrage.\n[/]")
                else:
                    ispis_filmova(trazeni_filmovi)
            break

def pretraga_termina_projekcija(svi_termini_projekcija):
    from datetime import datetime, time
    while True:
        print("Nalazite se u meniju za pretragu bioskopskih projekcija. Izaberite jedan ili više kriterijuma pretrage odvojenih razmakom.")
        print("    [1] Ime filma")
        print("    [2] Sala")
        print("    [3] Datum projekcije")
        print("    [4] Vreme projekcije")
        print("    [x] Otkazivanje")

        izbor = input("\nBiram: ").lower().strip()
        if izbor == "":
            console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")
            continue
        izbor = izbor.split()
        uneti_do_sada = []
        for i in izbor:
            if i not in uneti_do_sada:
                uneti_do_sada.append(i)
        
        for i in uneti_do_sada:
            if not i.lower() in ["1", "2", "3", "4", "x"]:
                console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")
                break
            if i == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                return
        else:
            termini_za_ispis = set(list(svi_termini_projekcija.keys()))
            promenjeno = False
            print("Ukoliko želite da prekinete proces pretrage, unesite x.")
            for i in uneti_do_sada:
                while True:
                    if i == "1":
                        unikatno = []
                        tabela = PrettyTable()
                        tabela.field_names = ["Broj", "Ime filma"]

                        brojac = 1
                        for film_id, film in svi_termini_projekcija.items():
                            ime_filma = film["Ime filma"]
                            if ime_filma not in unikatno:
                                tabela.add_row([brojac, ime_filma])
                                unikatno.append(ime_filma)
                                brojac += 1

                        print()
                        print(tabela)
                        
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
                        trazeni_film = unikatno[uneseni_broj]
                        pronadjene_projekcije = set()
                        for id, podaci in svi_termini_projekcija.items():
                            ime_filma = podaci["Ime filma"]
                            if ime_filma == trazeni_film:
                                pronadjene_projekcije.add(id)
                        termini_za_ispis.intersection_update(pronadjene_projekcije)
                        promenjeno = True
                        break        

                    elif i == "2":
                        with open("Svi entiteti/sale.txt", encoding="utf8") as fajl:
                            sala_lista = []  
                            for linija in fajl:
                                linija = linija.strip().split("|")
                                sala_lista.append(linija[0])  

                        tabela = PrettyTable()
                        tabela.field_names = ["Sala"]
                        for sala in sala_lista:
                            tabela.add_row([sala])
                        print()
                        print(tabela)
                            
                        sala_filma = input("\nUnesite željenu salu: ").lower().strip()

                        if sala_filma == "x":
                            console.print("[bright_red]\nOTKAZANO.\n[/]")
                            return
                            
                        pronadjene_projekcije = set()
                        for id, podaci in svi_termini_projekcija.items():
                            if sala_filma in podaci["Sala"].lower():
                                pronadjene_projekcije.add(id)

                        termini_za_ispis.intersection_update(pronadjene_projekcije)
                        promenjeno = True
                        break
                        
                    elif i == "3":
                        unikatno = []
                        tabela = PrettyTable()
                        tabela.field_names = ["Datum projekcije"]

                        for id, film in svi_termini_projekcija.items():
                            datum = film["Datum projekcije"]
                            datum_novi = datetime.strptime(datum, "%d.%m.%Y.")
                            sad_str = datetime.strftime(datetime.today(), "%d.%m.%Y.")
                            sad = datetime.strptime(sad_str, "%d.%m.%Y.")
                            if datum not in unikatno and datum_novi >= sad:
                                if film["Validnost"] != "VALIDNO":
                                    continue
                                tabela.add_row([datum])
                                unikatno.append(datum)
                        tabela.sortby = "Datum projekcije"
                        print()
                        print(tabela)

                        datum = input("\nUnesite datum projekcije: ").lower().strip()

                        if datum == "x":
                            console.print("[bright_red]\nOTKAZANO.\n[/]")
                            return
                            
                        pronadjene_projekcije = set()
                        for id, podaci in svi_termini_projekcija.items():
                            if datum in podaci["Datum projekcije"].lower(): 
                                pronadjene_projekcije.add(id)

                        termini_za_ispis.intersection_update(pronadjene_projekcije)
                        promenjeno = True
                        break

                    elif i == "4":
                        print("Ukoliko želite da unesete samo jednu granicu, kod unosa druge pritisnite enter.")
                        pocetak = input("\nUnesite željeni početak projekcije (npr. 10:00): ").lower().strip()
                        kraj = input("Unesite željeni završetak projekcije (npr. 13:00): ").lower().strip()
                        try:
                            if pocetak == "x" or kraj == "x":
                                console.print("[bright_red]\nOTKAZANO.[/]\n")
                                return
                            if pocetak == "":
                                pocetak = "10:00"
                            if kraj == "":
                                kraj = "22:00"
                            
                            pocetak_novi = datetime.strptime(pocetak, '%H:%M').time()
                            kraj_novi = datetime.strptime(kraj, '%H:%M').time()

                        except ValueError or UnboundLocalError:
                            console.print("[bright_red]\nNiste uneli dobar format vremena.[/]\n")
                            continue
                        pronadjene_projekcije = set()
                        for id, podaci in svi_termini_projekcija.items():
                            if pocetak_novi <= datetime.strptime((podaci["Početak projekcije"]), '%H:%M').time() and datetime.strptime((podaci["Kraj projekcije"]), '%H:%M').time() <= kraj_novi:
                                pronadjene_projekcije.add(id)

                        termini_za_ispis.intersection_update(pronadjene_projekcije)
                        promenjeno = True
                        break

            trazene_projekcije = {}
            if promenjeno:
                for id, podaci in svi_termini_projekcija.items():
                    if "VALIDNO" == podaci["Validnost"] and id in termini_za_ispis:
                        trazene_projekcije[id] = podaci
                        
                if len(trazene_projekcije) == 0:
                    console.print("[bright_red]\nNema odgovarajućeg podatka pretrage.\n[/]")
                    return

                else:
                    tabela = PrettyTable()
                    tabela.field_names = ["Šifra termina", "Ime filma", "Sala", "Datum projekcije", "Vreme početka", "Vreme kraja"]
                    for sifra, ids in trazene_projekcije.items():
                        tabela.add_row([sifra, ids["Ime filma"], ids["Sala"], ids["Datum projekcije"], ids["Početak projekcije"], ids["Kraj projekcije"]])
                    tabela.sortby = "Datum projekcije"
                    print()
                    print(tabela)
                    print()
            
            return True
        
def pregled_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik, svi_korisnici, prodavac=False):
    tabela = PrettyTable()
    tabela.field_names = ["Šifra karte", "Ime i prezime","Šifra termina", "Ime filma", "Datum projekcije", "Početak", "Kraj", "Sedište", "Status karte"]
    promenjeno = False
    if prodavac:
        for id_karte, podaci in sve_karte.items():
            korisnik = podaci["Korisnik"]
            if podaci["Uloga"] == "Registrovani kupac":
                ime_prezime = svi_korisnici[korisnik]["Ime"] + " " + svi_korisnici[korisnik]["Prezime"]
            else:
                ime_prezime = podaci["Korisnik"]
            id_termina = podaci["Šifra termina"]
            termin = svi_termini_projekcija[id_termina]
            validnost = podaci["Validnost"]
            status = podaci["Status karte"]
            if validnost == "VALIDNA":
                ime_filma = termin["Ime filma"]
                datum_projekcije = termin["Datum projekcije"]
                pocetak = termin["Početak projekcije"]
                kraj = termin["Kraj projekcije"]
                sediste = podaci["Sedište"]
                status = podaci["Status karte"]
                tabela.add_row([id_karte, ime_prezime, id_termina, ime_filma, datum_projekcije, pocetak, kraj, sediste, status])
                promenjeno = True
    else: 
        tren_kor = trenutni_korisnik
        for id_karte, podaci in sve_karte.items():
            id_termina = podaci["Šifra termina"]
            termin = svi_termini_projekcija[id_termina]
            korisnik = podaci["Korisnik"]
            if podaci["Uloga"] == "Registrovani kupac":
                ime_prezime = svi_korisnici[korisnik]["Ime"] + " " + svi_korisnici[korisnik]["Prezime"]

            else:
                ime_prezime = podaci["Korisnik"]
            validnost = podaci["Validnost"]
            if validnost == "VALIDNA" and korisnik == tren_kor:
                ime_filma = termin["Ime filma"]
                datum_projekcije = termin["Datum projekcije"]
                pocetak = termin["Početak projekcije"]
                kraj = termin["Kraj projekcije"]
                sediste = podaci["Sedište"]
                status = podaci["Status karte"]
                tabela.add_row([id_karte, ime_prezime, id_termina, ime_filma, datum_projekcije, pocetak, kraj, sediste, status])
                promenjeno = True

    if promenjeno:
        tabela.valign = "m"
        tabela.hrules = ALL
        tabela.set_style(DOUBLE_BORDER)
        print(tabela)
        print()
        return tabela
    else:
        console.print("[bright_red]Nema rezervisanih karata.[/]\n")
        return 
    
def pretraga_karata(sve_karte, svi_termini_projekcija, svi_korisnici):
    while True:
        print("\nNalazite se u meniju za pretragu karata. Izaberite jedan ili više kriterijuma pretrage odvojenih razmakom.")
        print("    [1] Šifra projekcije")
        print("    [2] Ime kupca")
        print("    [3] Prezime kupca")
        print("    [4] Datum projekcije")
        print("    [5] Početak i kraj projekcije")
        print("    [6] Status karte")
        print("    [x] Otkazivanje")

        izbor = input("\nBiram: ").lower().strip()
        if izbor == "":
            console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")
            continue
            
        izbor = izbor.split()
        uneti_do_sada = []
        for i in izbor:
            if i not in uneti_do_sada:
                uneti_do_sada.append(i)

        for i in uneti_do_sada:
            if not i.lower() in ["1", "2", "3", "4", "5", "6", "x"]:
                console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")
                break
            if i == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                return
            
        else:
            karte_za_ispis = set(list(sve_karte.keys()))
            promenjeno = False
            pronadjene_karte = set()
            for i in uneti_do_sada:
                print("Ukoliko želite da prekinete proces pretrage, unesite x.")
                if i == "1":
                    sifra_projekcije = input("Unesite šifru projekcije: ").lower().strip()

                    if sifra_projekcije == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue
                        
                    pronadjene_karte = set()
                    for id, podaci in sve_karte.items():
                        if sifra_projekcije == podaci["Šifra termina"][:-2].lower():
                            pronadjene_karte.add(id)

                    karte_za_ispis.intersection_update(pronadjene_karte)
                    promenjeno = True
                    continue

                if  i == "2":
                    ime_kupca = input("Unesite ime kupca: ").lower().strip()

                    if ime_kupca == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue
                        
                    pronadjene_karte = set()
                    for id, podaci in sve_karte.items():
                        if len(podaci["Korisnik"].split()) == 1:
                            if svi_korisnici[podaci["Korisnik"]]["Ime"].lower() == ime_kupca:
                                pronadjene_karte.add(id)

                        else:
                            if ime_kupca == podaci["Korisnik"].split()[0].lower():
                                pronadjene_karte.add(id)

                    karte_za_ispis.intersection_update(pronadjene_karte)
                    promenjeno = True
                    continue

                if  i == "3":
                    prezime_kupca = input("Unesite prezime kupca: ").lower().strip()

                    if prezime_kupca == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue
                        
                    pronadjene_karte = set()
                    for id, podaci in sve_karte.items():
                        if len(podaci["Korisnik"].split()) == 1:
                            if svi_korisnici[podaci["Korisnik"]]["Prezime"].lower() == prezime_kupca:
                                pronadjene_karte.add(id)

                        else:
                            if prezime_kupca == podaci["Korisnik"].split()[1].lower():
                                pronadjene_karte.add(id)

                    karte_za_ispis.intersection_update(pronadjene_karte)
                    promenjeno = True
                    continue

                if  i == "4":
                    datum_projekcije = input("Unesite datum projekcije (npr. 21.01.2024.): ").strip()

                    if datum_projekcije.lower() == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue
                        
                    pronadjene_karte = set()
                    for id, podaci in sve_karte.items():
                        sifra_termina = podaci["Šifra termina"]
                        if svi_termini_projekcija[sifra_termina]["Datum projekcije"] == datum_projekcije:
                            pronadjene_karte.add(id)

                    karte_za_ispis.intersection_update(pronadjene_karte)
                    promenjeno = True
                    continue

                if  i == "5":
                    print("Ukoliko želite da unesete samo jednu granicu, kod unosa druge pritisnite enter.")
                    pocetak = input("\nUnesite željeni početak projekcije (npr. 10:00): ").lower().strip()
                    kraj = input("Unesite željeni završetak projekcije (npr. 13:00): ").lower().strip()
                    try:
                        if pocetak == "x" or kraj == "x":
                            console.print("[bright_red]\nOTKAZANO.[/]\n")
                            return
                        if pocetak == "":
                            pocetak = "10:00"
                        if kraj == "":
                            kraj = "22:00"
                        
                        pocetak_novi = datetime.strptime(pocetak, '%H:%M').time()
                        kraj_novi = datetime.strptime(kraj, '%H:%M').time()

                    except ValueError or UnboundLocalError:
                        console.print("[bright_red]\nNiste uneli dobar format vremena.[/]\n")
                        continue
                    pronadjene_karte = set()
                    for id, podaci in sve_karte.items():
                        sifra_termina = podaci["Šifra termina"]
                        if (pocetak_novi <= datetime.strptime((svi_termini_projekcija[sifra_termina]["Početak projekcije"]), '%H:%M').time() 
                            and datetime.strptime((svi_termini_projekcija[sifra_termina]["Kraj projekcije"]), '%H:%M').time() <= kraj_novi):
                            pronadjene_karte.add(id)


                    karte_za_ispis.intersection_update(pronadjene_karte)
                    promenjeno = True
                    continue

                if  i == "6":
                    status_karte = input("Unesite status karte (PRODATA/REZERVISANA): ").lower().strip()

                    if status_karte == "x":
                        console.print("[bright_red]\nOTKAZANO.[/]\n")
                        continue
                        
                    pronadjene_karte = set()
                    for id, podaci in sve_karte.items():
                        if status_karte.upper() == podaci["Status karte"]:
                            pronadjene_karte.add(id)

                    karte_za_ispis.intersection_update(pronadjene_karte)
                    promenjeno = True
                    continue

            trazene_karte = {}
            
            if promenjeno:
                for id, podaci in sve_karte.items():
                    if "VALIDNA" == podaci["Validnost"] and id in karte_za_ispis:
                        trazene_karte[id] = podaci
                
                if len(trazene_karte) == 0:
                    console.print("[bright_red]\nNema odgovarajućeg podatka pretrage.\n[/]")
                else:
                    pregled_karata(trazene_karte, svi_termini_projekcija, "", svi_korisnici, True)
            break