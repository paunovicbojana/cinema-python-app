from prettytable import PrettyTable
from datetime import *
from pretrage_ispisi_entiteta import pretraga_termina_projekcija
from rich.console import Console
console = Console()

def validacija_ime_filma():
    while True:
        validno_ime_filma = input("Unesite ime filma: ").strip()
        if validno_ime_filma.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        elif "|" in validno_ime_filma:
           console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena![/]\n")
        elif len(validno_ime_filma )== 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        else:
            break

    return validno_ime_filma

def validacija_zanr_filma():
    zanrovi = [
        "Biografski", "Drama", "Avantura", "Kriminalistički",
        "Triler", "Ratni", "Romantika", "Akcija", "Sci-Fi",
        "Komedija", "Fantazija", "Horor", "Misterija", "Mjuzikl",
        "Animirani", "Western", "Sportski"
    ]

    tabela = PrettyTable()
    tabela.field_names = ["Broj", "Žanrovi"]

    for indeks, zanr_film in enumerate(zanrovi, start=1):
        tabela.add_row([indeks, zanr_film])
    print()
    print(tabela)

    while True:
        validni_zanr_filma = input("Unesite brojeve žanrova odvojene razmacima: ").lower().strip()
        if validni_zanr_filma == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        izlaz = []

        try:
            izabrano = [int(i) for i in validni_zanr_filma.split()]
        except ValueError:
            console.print("[bright_red]\nUnesite brojeve.[/]\n")
            continue

        for broj in izabrano:
            if 1 <= broj <= len(zanrovi):
                if zanrovi[broj - 1] not in izlaz:
                    izlaz.append(zanrovi[broj - 1])
            else:
                console.print("[bright_red]\nNiste uneli validan broj žanra.\n[/]")
                break
        else:
            return "/".join(izlaz)

def validacija_trajanje_filma():
    while True:
        validno_trajanje_filma = input("Unesite trajanje filma u minutima: ").strip()
        if validno_trajanje_filma.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        try:
            validno_trajanje_filma = int(validno_trajanje_filma)
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]\n")
            continue
        if validno_trajanje_filma <= 0:
            console.print("[bright_red]\nTrajanje filma mora biti pozitivan celi broj veći od nule.[/]\n")
            continue
        break

    return validno_trajanje_filma

def validacija_godina_filma():
    while True:
        validna_godina_filma = input("Unesite godinu proizvodnje filma bez tačke: ").strip()
        if validna_godina_filma.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        try:
            validna_godina_filma = int(validna_godina_filma)
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]\n")
            continue
        if validna_godina_filma < 1895 or validna_godina_filma > 2024:
            console.print("[bright_red]\nGodina proizvodnje filma mora biti pozitivan celi broj veći od 1895 i manji od 2024.[/]\n")
            continue
        break

    return validna_godina_filma

def validacija_ime_glumca():
    while True:
        validno_ime_glumca = input("Unesite imena glavnih glumaca odvojena zarezom: ").strip()
        if validno_ime_glumca.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        elif "|" in validno_ime_glumca:
           console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena![/]\n")
        elif len(validno_ime_glumca) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        else:
            break

    return validno_ime_glumca

def validacija_poreklo_filma():
    while True:
        poreklo_filma = input("Unesite jednu ili više zemalja proizvodnje odvojenih kosom crtom (/): ").strip()
        poreklo_filma = poreklo_filma.split("/")
        izlaz = []
        for zemlja in poreklo_filma:
            zemlja = zemlja.title()
            izlaz.append(zemlja)
            if zemlja.lower() == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                return "x"
            if len(zemlja) == 0:
                console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
                break
        else:
            return "/".join(izlaz)

def validacija_opis():
    while True:
        validni_opis = input("Unesite opis filma: ").strip()
        if validni_opis.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        elif "|" in validni_opis:
           console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena![/]\n")
        elif len(validni_opis) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        else:
            break

    return validni_opis

def validacija_ime_rezisera():
    while True:
        validno_ime_rezisera = input("Unesite imena režisera odvojena zarezom: ").strip()
        if validno_ime_rezisera.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        elif "|" in validno_ime_rezisera:
           console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena![/]\n")
        elif len(validno_ime_rezisera) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        else:
            break

    return validno_ime_rezisera

def validacija_sale(sve_sale):
    tabela = PrettyTable()
    tabela.field_names = ["Sala"]
    for sala in sve_sale.keys():
        tabela.add_row([sala])
    print()
    print(tabela)
    while True:  
        sala_filma = input("\nUnesite željenu salu: ").upper().strip()

        if sala_filma == "X":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        elif "|" in sala_filma:
            console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena![/]\n")
        elif len(sala_filma) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        elif sala_filma not in sve_sale.keys():
            console.print("[bright_red]\nNiste uneli salu sa spiska dostupnih sala.[/]")
        else:
            break

    return sala_filma

def validacija_vremena(trazeno_trajanje):
    from datetime import datetime, time
    while True:
        pocetak = input("Unesite željeni početak projekcije (npr. 10:00): ").lower().strip()
        try:
            if pocetak == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                return "x", "x"
            otvaranje = "10:00"
            zatvaranje = "22:00"
            zatvaranje_novi = datetime.strptime(zatvaranje, '%H:%M').time()
            otvaranje_novi = datetime.strptime(otvaranje, '%H:%M').time()
            pocetak_novi = datetime.strptime(pocetak, '%H:%M').time()
            
            if pocetak_novi < otvaranje_novi:
                console.print("[bright_red]\nBioskop se otvara u 10:00.[/]\n")
            elif pocetak_novi > zatvaranje_novi:
                console.print("[bright_red]\nBioskop se zatvara u 22:00.[/]\n")
            
            pocetak_novi = datetime.strptime(pocetak, '%H:%M')
            trazeno_trajanje_novi = timedelta(minutes=int(trazeno_trajanje))
            kraj_novi = pocetak_novi + trazeno_trajanje_novi
            zatvaranje = datetime.strptime("22:00", '%H:%M')
            if kraj_novi >= zatvaranje:
                console.print("[bright_red]\nBioskop se zatvara u 22:00, izaberite raniji početak projekcije.[/]\n")

            else:
                vreme_sa_dodatkom = kraj_novi + timedelta(minutes=30)
                zaokruzeno_vreme = zaokruzi_na_30_min(vreme_sa_dodatkom)
                if zaokruzeno_vreme > zatvaranje:
                    console.print("[bright_red]\nBioskop se zatvara u 22:00, izaberite raniji početak projekcije.[/]\n")
                else:
                    print("Kraj filma je u", zaokruzeno_vreme.strftime('%H:%M'))
                    return pocetak, zaokruzeno_vreme.strftime('%H:%M')

        except ValueError or UnboundLocalError:
            console.print("[bright_red]\nNiste uneli dobar format vremena.\n[/]")

def zaokruzi_na_30_min(vreme):
    zaokruzeno_vreme = vreme - (vreme.minute % 30) * timedelta(minutes=1)
    return zaokruzeno_vreme

def validacija_dan():
    dani = [
        "ponedeljak",
        "utorak",
        "sreda",
        "četvrtak",
        "petak",
        "subota",
        "nedelja"
    ]

    while True:
        dan_filma = input("\nUnesite dane održavanja projekcije odvojene zarezom (ponedeljak-nedelja): ").lower().strip()
        izlaz = []
        dan_filma = dan_filma.split(",")
        for dan in dan_filma:
            dan = dan.strip()
            izlaz.append(dan)
            if dan == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                return "x"
            if dan not in dani:
                console.print("[bright_red]\nNiste uneli dostupan dan.[/]")
                break
        else:
            return ", ".join(izlaz)

def validacija_film():
    with open("Svi entiteti/filmovi.txt", encoding="utf8") as fajl:
        film_lista = []  
        trajanje_lista = []
        id_filma_lista = []
        for linija in fajl:
            linija = linija.strip().split("|")
            if linija[9] != "VALIDNO":
                continue
            film_lista.append(linija[1])  
            trajanje_lista.append(linija[3])
            id_filma_lista.append(linija[0])

    tabela = PrettyTable()
    tabela.field_names = ["Broj", "Ime filma"]

    for indeks, film in enumerate(film_lista, start=1):
        tabela.add_row([indeks, film])
    print()
    print(tabela)
    
    while True:
        validni_film = input("Unesite broj filma: ").lower().strip()
        if validni_film == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x", "x", "x"

        try:
            validni_film = int(validni_film)
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]\n")
            continue

        if 1 <= validni_film <= len(film_lista):
            broj = validni_film - 1
            trazeni_film = film_lista[broj]
            trazeno_trajanje = trajanje_lista[broj]
            id_filma = id_filma_lista[broj]
            return trazeni_film, trazeno_trajanje, id_filma
        else:
            console.print("[bright_red]\nNiste uneli validan broj filma.[/]\n")
        

def validacija_cena_karte():
    while True:
        cena_karte = input("Unesite cenu karte u dinarima (npr. 430.00): ").strip()
        if cena_karte.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return "x"
        try:
            cena_karte = float(cena_karte)
        except ValueError:
            console.print("[bright_red]\nUnesite broj.[/]\n")
            continue
        if cena_karte < 0:
            console.print("[bright_red]\nCena karte mora biti pozitivan broj.\n[/]")
            continue
        break

    return cena_karte

def validacija_termina(svi_termini_projekcija):
    print('Ukoliko znate šifru termina projekcije, izaberite opciju "Unos šifre termina" i unesite je direkno.')
    print('U suprotnom, izaberite opciju "Pretraga" i pretražite dostupne projekcije.')
    print('Izaberite "x" za završetak.')
    while True:
        print("    [1]  Pretraga")
        print("    [2]  Unos šifre termina")
        print("    [x]  Otkazivanje\n")
        izbor = input("Biram: ")
        if izbor.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        elif izbor == "1":
            biram = pretraga_termina_projekcija(svi_termini_projekcija)
            if biram == None:
                break
            while True:
                termin_projekcije = input("Unesite šifru željenog termina projekcije: ").upper()
                
                if termin_projekcije.lower() == "x":
                    console.print("[bright_red]\nOTKAZANO.[/]\n")
                    break
                elif termin_projekcije not in svi_termini_projekcija.keys():
                    console.print("[bright_red]\nIzabrani termin ne postoji. Unesite šifru projekcije ponovo.\n[/]")

                elif svi_termini_projekcija[termin_projekcije]["Validnost"] == "NEVALIDNO":
                    console.print("[bright_red]\nIzabrani termin ne postoji. Unesite šifru projekcije ponovo.\n[/]")
                else:
                    return termin_projekcije
                
        elif izbor == "2":
            while True:
                termin_projekcije = input("Unesite šifru željenog termina projekcije: ").upper()
                
                if termin_projekcije.lower() == "x":
                    console.print("[bright_red]\nOTKAZANO.[/]\n")
                    break
                elif termin_projekcije not in svi_termini_projekcija.keys():
                    console.print("[bright_red]\nIzabrani termin ne postoji. Unesite šifru projekcije ponovo.\n[/]")

                elif svi_termini_projekcija[termin_projekcije]["Validnost"] == "NEVALIDNO":
                    console.print("[bright_red]\nIzabrani termin ne postoji. Unesite šifru projekcije ponovo.\n[/]")
                else:
                    return termin_projekcije
        else:
            console.print("[bright_red]\nNEVALIDAN UNOS.\n[/]")