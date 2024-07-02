import validacija_entiteta
from datetime import *
from prettytable import *
from rich.console import Console
console = Console()

def unos_novih_filmova(svi_filmovi):
    console.print("[magenta3]\nOBAVEŠTENJE:[/] Projekcije i termini projekcija ovog filma, kao i karte,")
    print("             biće dostupni nakon unosa projekcija za ovaj film i generisanja termina.\n")
    if len(svi_filmovi.keys()) == 0:
        ids = 1000
    else:
        ids = max(svi_filmovi.keys()) + 1
    
    print("ID ovog filma je:", ids)
    print('Da biste prekinuli proces unosa novog filma, u bilo kom trenutku unesite "x".')
    ime_filma = validacija_entiteta.validacija_ime_filma()
    if ime_filma == "x":
        return
    zanr_film = validacija_entiteta.validacija_zanr_filma()
    if zanr_film == "x":
        return
    trajanje_filma = validacija_entiteta.validacija_trajanje_filma()
    if trajanje_filma == "x":
        return
    reziseri_filma = validacija_entiteta.validacija_ime_rezisera()
    if reziseri_filma.lower() == "x":
        return
    glumci_filma = validacija_entiteta.validacija_ime_glumca()
    if glumci_filma.lower() == "x":
        return
    poreklo_filma = validacija_entiteta.validacija_poreklo_filma()
    if poreklo_filma.lower() == "x":
        return
    godina_filma = validacija_entiteta.validacija_godina_filma()
    if godina_filma == "x":
        return
    opis_filma = validacija_entiteta.validacija_opis()
    if opis_filma.lower() == "x":
        return
    validnost = "VALIDNO"

    svi_filmovi[ids] = {
        "Ime": ime_filma,
        "Žanr": zanr_film,
        "Trajanje": trajanje_filma,
        "Režiseri": reziseri_filma,
        "Glavne uloge": glumci_filma,
        "Zemlja porekla": poreklo_filma,
        "Godina proizvodnje": godina_filma,
        "Opis": opis_filma,
        "Validnost": validnost
        }
    
    fajl = open("Svi entiteti/filmovi.txt", "a", encoding="utf8")

    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(ids, ime_filma, zanr_film, trajanje_filma, reziseri_filma, glumci_filma, poreklo_filma, godina_filma, opis_filma, validnost))

    fajl.close()
    console.print("[green3]\nUspešan unos novog filma.\n[/]")

def unos_novih_projekcije(sve_projekcije, sve_sale):
    console.print("[magenta3]\nOBAVEŠTENJE:[/] Termini nove projekcije, kao i karte, biće dostupni")
    print("             nakon generisanja novih termina projekcija.\n")
    if len(sve_projekcije.keys()) == 0:
        ids = 1000
    else:
        ids = max(sve_projekcije.keys()) + 1
    print("ID ove projekcije je:", ids)
    print('Da biste prekinuli proces unosa nove projekcije, u bilo kom trenutku unesite "x".')
    sala = validacija_entiteta.validacija_sale(sve_sale)
    if sala.lower() == "x":
        return
    film, trazeno_trajanje, id_filma = validacija_entiteta.validacija_film()
    if film == "x":
        return
    pocetak, kraj = validacija_entiteta.validacija_vremena(trazeno_trajanje)
    if pocetak == "x":
        return
    dani = validacija_entiteta.validacija_dan()
    if dani == "x":
        return
    cena_karte = validacija_entiteta.validacija_cena_karte()
    if cena_karte == "x":
        return
    validnost = "VALIDNO"
    id_filma = int(id_filma)
    sve_projekcije[ids] = {
        "Sala": sala,
        "Početak": pocetak,
        "Kraj": kraj,
        "Dani": dani,
        "ID filma": id_filma,
        "Film": film,
        "Cena karte": cena_karte,
        "Validnost": validnost
        }
    
    fajl = open("Svi entiteti/projekcije.txt", "a", encoding="utf8")

    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(ids, sala, pocetak, kraj, dani, id_filma, film, cena_karte, validnost))

    fajl.close()
    
    console.print("[green3]\nUspešan unos nove projekcije.\n[/]")

def izmena_filmovi(svi_filmovi):
    tabela = PrettyTable()
    tabela.field_names = ["ID", "Film", "Status"]
    for id, film in svi_filmovi.items():
        tabela.add_row([id, film["Ime"], film["Validnost"]])
    print()
    print(tabela)
    print()
    while True:
        ids = input("Unesite ID filma kojeg želite da izmenite: ")
        if ids.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        elif int(ids) not in svi_filmovi.keys():
            console.print("[bright_red]\nID filma nije ispravan, pokušajte ponovo.[/]\n")
            
        else:
            print("\nUkoliko želite da prekinete proces izmene podataka, unesite x.")
            while True:
                print("    [1] Žanr")
                print("    [2] Trajanje (min)")
                print("    [3] Režiser")
                print("    [4] Glavne uloge")
                print("    [5] Zemlja porekla")
                print("    [6] Godina proizvodnje")
                print("    [7] Opis")
                print("    [x] Otkazivanje\n")
                izmena_cega = input("Šta želite da promenite? ").strip().lower()
                ids = int(ids)
                if izmena_cega.lower() == "x":
                    console.print("[bright_red]\nOTKAZANO.[/]\n")
                    return
                elif izmena_cega == "1":
                    print("Trenutni žanr:", svi_filmovi[ids]["Žanr"])
                    while True:
                        novi_zanr = validacija_entiteta.validacija_zanr_filma()
                        if novi_zanr == "x" or novi_zanr == "X":
                            return
                        elif novi_zanr == svi_filmovi[ids]["Žanr"]:
                            console.print("[bright_red]\nNovi žanr ne sme biti isti kao trenutni.[/]\n")
                        else:
                            svi_filmovi[ids]["Žanr"] = novi_zanr
                            break
                    break

                elif izmena_cega == "2":
                    print("Trenutno trajanje (min):", svi_filmovi[ids]["Trajanje"])
                    while True:
                        novo_trajanje = validacija_entiteta.validacija_trajanje_filma()
                        if novo_trajanje == "x" or novo_trajanje == "X":
                            return
                        elif novo_trajanje == svi_filmovi[ids]["Trajanje"]:
                            console.print("[bright_red]\nNovo trajanje ne sme biti isto kao trenutno.[/]\n")
                        else:
                            svi_filmovi[ids]["Trajanje"] = novo_trajanje
                            break
                    break
                
                elif izmena_cega == "3":
                    print("Trenutni režiseri:", svi_filmovi[ids]["Režiseri"])
                    while True:
                        novi_reziseri = validacija_entiteta.validacija_ime_rezisera()
                        if novi_reziseri == "x" or novi_reziseri == "X":
                            return
                        elif novi_reziseri == svi_filmovi[ids]["Režiseri"]:
                            console.print("[bright_red]\nNovi režiseri ne smeju biti isti kao trenutni.[/]\n")
                        else:
                            svi_filmovi[ids]["Režiseri"] = novi_reziseri
                            break
                    break

                elif izmena_cega == "4":
                    print("Trenutne glavne uloge:", svi_filmovi[ids]["Glavne uloge"])
                    while True:
                        nove_uloge = validacija_entiteta.validacija_ime_glumca()
                        if nove_uloge == "x" or nove_uloge == "X":
                            return
                        elif nove_uloge == svi_filmovi[ids]["Glavne uloge"]:
                            console.print("[bright_red]\nNove glavne uloge ne smeju biti iste kao trenutne.[/]\n")
                        else:
                            svi_filmovi[ids]["Glavne uloge"] = nove_uloge
                            break
                    break

                elif izmena_cega == "5":
                    print("Trenutna zemlja porekla:", svi_filmovi[ids]["Zemlja porekla"])
                    while True:
                        nova_zemlja = validacija_entiteta.validacija_poreklo_filma()
                        if nova_zemlja == "x" or nova_zemlja == "X":
                            return
                        elif nova_zemlja == svi_filmovi[ids]["Zemlja porekla"]:
                            console.print("[bright_red]\nNova zemlja porekla ne sme biti ista kao trenutna.[/]\n")
                        else:
                            svi_filmovi[ids]["Zemlja porekla"] = nova_zemlja
                            break
                    break

                elif izmena_cega == "6":
                    print("Trenutna godina proizvodnje:", svi_filmovi[ids]["Godina proizvodnje"])
                    while True:
                        nova_godina = validacija_entiteta.validacija_trajanje_filma()
                        if nova_godina == "x" or nova_godina == "X":
                            return
                            
                        elif nova_godina == svi_filmovi[ids]["Godina proizvodnje"]:
                            console.print("[bright_red]\nNova godina proizvodnje ne sme biti ista kao trenutna.[/]\n")
                        else:
                            svi_filmovi[ids]["Godina proizvodnje"] = nova_godina
                            break
                    break

                elif izmena_cega == "7":
                    print("Trenutni opis:", svi_filmovi[ids]["Opis"])
                    while True:
                        novi_opis = validacija_entiteta.validacija_opis()
                        if novi_opis == "x" or novi_opis == "X":
                            return
                            
                        elif novi_opis == svi_filmovi[ids]["Opis"]:
                            console.print("[bright_red]\nNovi opis ne sme biti isti kao trenutni.[/]\n")
                        else:
                            svi_filmovi[ids]["Opis"] = novi_opis
                            break
                    break

                else:
                    console.print('[bright_red]\nNEVALIDAN UNOS.[/]\n')

            fajl = open("Svi entiteti/filmovi.txt", "w", encoding="utf8")

            for ids, podaci in svi_filmovi.items():
                ime_filma = podaci["Ime"]
                zanr_film = podaci["Žanr"]
                trajanje_filma = podaci["Trajanje"]
                reziseri_filma = podaci["Režiseri"]
                glumci_filma = podaci["Glavne uloge"]
                poreklo_filma = podaci["Zemlja porekla"]
                godina_filma = podaci["Godina proizvodnje"]
                opis_filma = podaci["Opis"]
                validnost = podaci["Validnost"]

                fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(ids, ime_filma, zanr_film, trajanje_filma, reziseri_filma, glumci_filma, poreklo_filma, godina_filma, opis_filma, validnost))

            fajl.close()
            console.print("[green3]\nUspešno ste izmenili podatke filma.\n[/]")

def brisanje_filmova(svi_filmovi):
    console.print("[magenta3]\nOBAVEŠTENJE:[/] Termini obrisanog filma, kao i karte, biće obrisani")
    print("             nakon isteka prethodno generisanih termina projekcija.")
    print("             Do tada će kupovina karata za termine ovog filma biti moguća.")
    tabela = PrettyTable()
    tabela.field_names = ["ID", "Film", "Status"]
    for id, film in svi_filmovi.items():
        tabela.add_row([id, film["Ime"], film["Validnost"]])
    print()
    print(tabela)
    print()
    ids = input("Unesite ID filma čiji status želite da promenite: ")
    if ids.lower() == "x":
        console.print("[bright_red]\nOTKAZANO.[/]\n")
        return
    elif int(ids) not in svi_filmovi.keys():
        console.print('[bright_red]\nID nije ispravan, pokušajte ponovo.[/]\n')
    else:
        ids = int(ids)
        print("Trenutni status:", svi_filmovi[ids]["Validnost"])
        while True:
            nova_validnost = input('Ukoliko želite da promenite status filma, unesite "DA": ')
            if nova_validnost == "x" or nova_validnost == "X":
                return
            elif not nova_validnost.lower() == "da":
                print('Unesite "DA" ili "x" za otkazivanje.')
            else:
                if svi_filmovi[ids]["Validnost"] == "VALIDNO":
                    svi_filmovi[ids]["Validnost"] = "NEVALIDNO"
                else:
                    svi_filmovi[ids]["Validnost"] = "VALIDNO"
                break
            break
        fajl = open("Svi entiteti/filmovi.txt", "w", encoding="utf8")

        for ids, podaci in svi_filmovi.items():
            ime_filma = podaci["Ime"]
            zanr_film = podaci["Žanr"]
            trajanje_filma = podaci["Trajanje"]
            reziseri_filma = podaci["Režiseri"]
            glumci_filma = podaci["Glavne uloge"]
            poreklo_filma = podaci["Zemlja porekla"]
            godina_filma = podaci["Godina proizvodnje"]
            opis_filma = podaci["Opis"]
            validnost = podaci["Validnost"]

            fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(ids, ime_filma, zanr_film, trajanje_filma, reziseri_filma, glumci_filma, poreklo_filma, godina_filma, opis_filma, validnost))

        fajl.close()
        console.print("[green3]\nUspešno ste promenili status filma.\n[/]")
    
def izmena_projekcija(sve_projekcije, svi_filmovi, sve_sale):
    console.print("[magenta3]\nOBAVEŠTENJE:[/] Termini izmenjene projekcije, kao i karte, biće")
    print("             dostupni nakon generisanja novih termina projekcija.")
    tabela = PrettyTable()
    tabela.field_names = ["ID", "Sala", "Početak", "Kraj", "Dani održavanja", "Ime filma", "Cena karte", "Validnost"]
    for id, projekcija in sve_projekcije.items():
        tabela.add_row([id, projekcija["Sala"], projekcija["Početak"], projekcija["Kraj"], projekcija["Dani"], projekcija["Film"], projekcija["Cena karte"], projekcija["Validnost"]])
    print()
    print(tabela)
    print()
    ids = input("Unesite ID projekcije koju želite da izmenite: ")
    if ids.lower() == "x":
        console.print("[bright_red]\nOTKAZANO.[/]\n")
        return
    elif int(ids) not in sve_projekcije.keys():
        console.print('[bright_red]\nID nije ispravan, pokušajte ponovo.[/]\n')
    else:
        print("\nUkoliko želite da prekinete proces izmene podataka, unesite x.")
        while True:
            print("    [1] Sala")
            print("    [2] Početak projekcije")
            print("    [3] Dani održavanja")
            print("    [4] Film")
            print("    [5] Cena karte")
            print("    [x] Otkazivanje\n")
            izmena_cega = input("Šta želite da promenite? ").strip().lower()
            ids = int(ids)
            if izmena_cega.lower() == "x":
                console.print("[bright_red]\nOTKAZANO[/]\n")
                return
            elif izmena_cega == "1":
                print("Trenutna sala:", sve_projekcije[ids]["Sala"])
                while True:
                    nova_sala = validacija_entiteta.validacija_sale(sve_sale)
                    if nova_sala == "x" or nova_sala == "X":
                        return
                    elif nova_sala == sve_projekcije[ids]["Sala"]:
                        console.print('[bright_red]\nNova sala ne sme biti ista kao trenutna.[/]\n')
                        
                    else:
                        sve_projekcije[ids]["Sala"] = nova_sala
                        break
                break

            elif izmena_cega == "2":
                print("Trenutni početak projekcije:", sve_projekcije[ids]["Početak"])
                while True:
                    id_film = int(sve_projekcije[ids]["ID filma"])
                    trazeno_trajanje = svi_filmovi[id_film]["Trajanje"]
                    novi_pocetak, novi_kraj = validacija_entiteta.validacija_vremena(trazeno_trajanje)
                    if novi_pocetak == "x" or novi_pocetak == "X":
                        return
                    elif novi_pocetak == sve_projekcije[ids]["Početak"]:
                        console.print('[bright_red]\nNovi početak projekcije ne sme biti isti kao trenutni.[/]\n')
                    else:
                        sve_projekcije[ids]["Početak"] = novi_pocetak
                        sve_projekcije[ids]["Kraj"] = novi_kraj
                        break
                break

            elif izmena_cega == "3":
                print("Trenutni dani projekcije:", sve_projekcije[ids]["Dani"])
                while True:
                    novi_dani = validacija_entiteta.validacija_dan()
                    if novi_dani == "x" or novi_dani == "X":
                        return
                    elif novi_dani == sve_projekcije[ids]["Dani"]:
                        console.print('[bright_red]\nNovi dani projekcije ne smeju biti isti kao trenutni.[/]\n')
                    else:
                        sve_projekcije[ids]["Dani"] = novi_dani
                        break
                break

            elif izmena_cega == "4":
                print("Trenutni film:", sve_projekcije[ids]["Film"])
                while True:
                    novi_film = validacija_entiteta.validacija_film()
                    if novi_film == "x" or novi_film == "X":
                        return
                    elif novi_film == sve_projekcije[ids]["Film"]:
                        console.print('[bright_red]\nNovi film ne sme biti isti kao trenutni.[/]\n')
                    else:
                        sve_projekcije[ids]["Film"] = novi_film
                        break
                break

            elif izmena_cega == "5":
                print("Trenutna osnovna cena karte:", sve_projekcije[ids]["Cena karte"])
                while True:
                    nova_cena = validacija_entiteta.validacija_cena_karte()
                    if nova_cena == "x" or nova_cena == "X":
                        return
                    elif nova_cena == sve_projekcije[ids]["Cena karte"]:
                        console.print('[bright_red]\nNova osnovna cena karte ne sme biti isti kao trenutna.[/]\n')
                    else:
                        sve_projekcije[ids]["Cena karte"] = nova_cena
                        break
                break

            else:
                console.print('[bright_red]\nNEVALIDAN UNOS.[/]\n')

        fajl = open("Svi entiteti/projekcije.txt", "w", encoding="utf8")

        for ids, podaci in sve_projekcije.items():
            sala = podaci["Sala"]
            pocetak = podaci["Početak"]
            kraj = podaci["Kraj"]
            dani = podaci["Dani"]
            id_filma = podaci["ID filma"]
            film = podaci["Film"]
            cena_karte = podaci["Cena karte"]
            validnost = podaci["Validnost"]

            fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(ids, sala, pocetak, kraj, dani, id_filma, film, cena_karte, validnost))

        fajl.close()
        console.print("[green3]\nUspešno ste izmenili projekciju.\n[/]")

def brisanje_projekcija(sve_projekcije):
    console.print("[magenta3]\nOBAVEŠTENJE:[/] Termini obrisane projekcije, kao i karte, biće obrisani")
    print("             nakon isteka prethodno generisanih termina projekcija.")
    tabela = PrettyTable()
    tabela.field_names = ["ID", "Sala", "Početak", "Kraj", "Dani održavanja", "Ime filma", "Cena karte", "Validnost"]
    for id, projekcija in sve_projekcije.items():
        tabela.add_row([id, projekcija["Sala"], projekcija["Početak"], projekcija["Kraj"], projekcija["Dani"], projekcija["Film"], projekcija["Cena karte"], projekcija["Validnost"]])
    print()
    print(tabela)
    print()
    ids = input("Unesite ID projekcije čiji status želite da promenite: ")
    if ids.lower() == "x":
        console.print('[bright_red]\nOTKAZANO.[/]\n')
        return
    elif int(ids) not in sve_projekcije.keys():
        console.print('[bright_red]\nID nije ispravan, pokušajte ponovo.[/]\n')
    else:
        ids = int(ids)
        print("Trenutni status:", sve_projekcije[ids]["Validnost"])
        while True:
            nova_validnost = input('Ukoliko želite da promenite status projekcije, unesite "DA": ')
            if nova_validnost == "x" or nova_validnost == "X":
                return
            elif not nova_validnost.lower() == "da":
                print('Unesite "DA" ili "x" za otkazivanje.')
            else:
                if sve_projekcije[ids]["Validnost"] == "VALIDNO":
                    sve_projekcije[ids]["Validnost"] = "NEVALIDNO"
                else:
                    sve_projekcije[ids]["Validnost"] = "VALIDNO"
                break
            break
    
        fajl = open("Svi entiteti/projekcije.txt", "w", encoding="utf8")

        for ids, podaci in sve_projekcije.items():
            sala = podaci["Sala"]
            pocetak = podaci["Početak"]
            kraj = podaci["Kraj"]
            dani = podaci["Dani"]
            id_filma = podaci["ID filma"]
            film = podaci["Film"]
            cena_karte = podaci["Cena karte"]
            validnost = podaci["Validnost"]

            fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(ids, sala, pocetak, kraj, dani, id_filma, film, cena_karte, validnost))

        fajl.close()

        console.print("[green3]\nUspešno ste promenili status projekcije.\n[/]")

def generisanje_ids():
    for i in range(ord("A"), ord("Z") + 1):
        for j in range(ord("A"), ord("Z") + 1):
            yield chr(i) + chr(j)

def mapiraj(n):
        mapa = {}
        sedmica = ["ponedeljak", "utorak", "sreda", "četvrtak", "petak", "subota", "nedelja"]
        for k, dan in enumerate(sedmica):
            mapa[dan] = (7 - n + k) % 7
        return mapa  

def generisanje_termina_projekcija(sve_projekcije):
    while True:
        izbor = input('Ukoliko želite da generišete nove termine projekcija unesite "DA", u suprotnom unesite "x": ')
        if izbor.lower() == "x":
            console.print("[bright_red]\nOTKAZANO[/]\n")
            break
        elif izbor.lower() == "da":
            while True:
                broj_nedelja = input("Unesite broj nedelja za koji želite da generišete nove termine: ")
                if broj_nedelja.lower() == "x":
                    console.print("[bright_red]\nOTKAZANO[/]\n")
                    return ""
                try:
                    broj_nedelja = int(broj_nedelja)
                except ValueError:
                    console.print("[bright_red]\nUnesite broj.[/]\n")
                    continue

                fajl = open("Svi entiteti/termini_projekcija.txt", "a", encoding="utf8")
                for i in range(broj_nedelja):  
                    for sifra_projekcije, podaci in sve_projekcije.items():
                        if podaci["Validnost"] == "NEVALIDNO":
                            continue
                        sad = datetime.now()
                        trenutni_datum = sad + timedelta(weeks=i)
                        generator = podaci["Fabrika"]
                        dani = podaci["Dani"].split(", ")
                        validnost = "VALIDNO"
                        n = trenutni_datum.weekday()
                        mapa = mapiraj(n)
                        for dan in dani:
                            sifra_termina = str(sifra_projekcije) + next(generator)
                            datum_termina = trenutni_datum + timedelta(days=mapa[dan])
                            datum_termina = datetime.strftime(datum_termina,"%d.%m.%Y.")
                            fajl.write("{}|{}|{}\n".format(sifra_termina, datum_termina, validnost))

                fajl.close()
                console.print("[green3]\nUspešno generisanje novih termina projekcija za naredni broj nedelja:[/]", broj_nedelja, "\n")
                datum_sledeci = datetime.today() + timedelta(days=broj_nedelja*7)
                print("Naredno generisanje termina možete obaviti", datetime.strftime(datum_sledeci, "%d.%m.%Y."), "\n")
                return datum_sledeci
            break

        else:
            console.print("[bright_red]\nNEVALIDAN UNOS[/]\n")