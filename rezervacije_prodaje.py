from datetime import datetime, timedelta
from validacija_entiteta import *
from pretrage_ispisi_entiteta import pregled_karata
from prettytable import *
from rich.console import Console
console = Console()

def generisanje_sedista(red, kolona):
    sedista = [[chr(65 + j) for j in range(kolona)] for i in range(red)]
    return sedista

def prikaz_sedista(sedista): 
    for i, red in enumerate(sedista):
        print(f"Red {i + 1}: {' '.join(red)}")
    
def zauzimanje_sedista(sedista, sve_sale, svi_termini_projekcija, termin_projekcije):  
    while True:
        print()
        prikaz_sedista(sedista)
        unos = input("\nUnesite željeno sedište (npr. 1-A): ").upper().split("-")
        if "X" in unos:
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        elif len(unos) != 2:
            console.print("[bright_red]\nNEVALIDAN UNOS.[/]")
        else:
            red = unos[0]
            kolona = unos[1]
            if red == "" or kolona == "":
                console.print("[bright_red]\nNEVALIDAN UNOS.[/]")
                continue
            sala = svi_termini_projekcija[termin_projekcije]["Sala"]
            try:
                red = int(red) - 1
            except ValueError:
                console.print("[bright_red]\nRed mora biti broj.[/]\n")
                continue
            if red < 0:
                console.print("[bright_red]\nNe postoji taj red.[/]")
                continue
            if red >= int(sve_sale[sala]["Broj redova"]):
                console.print("[bright_red]\nNe postoji taj red.[/]\n")
            elif ord(kolona) - 65 >= int(sve_sale[sala]["Broj kolona"]):
                console.print("[bright_red]\nNe postoji ta kolona.[/]\n")
            elif sedista[red][ord(kolona) - 65] == "X":
                console.print("[bright_red]\nZAUZETO.[/]")
            else:
                sedista[red][ord(kolona) - 65] = "X"
                svi_termini_projekcija[termin_projekcije]["Sedišta"] = sedista
                return ("-").join(unos)
            
def oslobadjanje_sedista(sedista, mesto):
    red = int(mesto[0]) - 1 
    kolona = ord(mesto[1]) - 65
    sedista[red][kolona] = mesto[1]

def popuni_zauzeta_mesta(svi_termini_projekcija, sve_karte):
    for sifra_karte, podaci in sve_karte.items():
        if podaci["Validnost"] == "NEVALIDNA":
            continue
        sifra_termina = podaci["Šifra termina"]
        termin = svi_termini_projekcija[sifra_termina]
        sedista = termin["Sedišta"]
        izabrano_sediste = podaci["Sedište"]
        izabrano_sediste = izabrano_sediste.split("-")
        red = izabrano_sediste[0]
        kolona = izabrano_sediste[1]
        sedista[int(red) - 1][ord(kolona) - 65] = "X"

def rezervacija_karata(sve_karte, svi_termini_projekcija, sve_sale, trenutni_korisnik, svi_korisnici, prodavac=False):
    while True:
        if prodavac:
            trenutni_korisnik = input("Unesite ime i prezime neregistrovanog kupca ili korisničko ime registrovanog kupca: ").strip()
            if trenutni_korisnik.lower() == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                break
            trenutni_korisnik = trenutni_korisnik.split(" ")
            if (len(trenutni_korisnik) == 1) and (trenutni_korisnik[0] not in svi_korisnici.keys()):
                console.print("[bright_red]\nUneto korisničko ime nije u sistemu.[/]\n")
                continue
            elif (len(trenutni_korisnik) == 1) and (trenutni_korisnik[0] in svi_korisnici.keys()):
                uloga = "Registrovani kupac"
            else:
                uloga = "Neregistrovani kupac"
            trenutni_korisnik = (" ").join(trenutni_korisnik)
        termin_projekcije = validacija_termina(svi_termini_projekcija)
        if termin_projekcije == None:
            return
        sedista = svi_termini_projekcija[termin_projekcije]["Sedišta"]
        while True:
            if len(sve_karte.keys()) == 0:
                id_karte = 1000
            else:
                id_karte = max(sve_karte.keys()) + 1
            izabrano_sediste = zauzimanje_sedista(sedista, sve_sale, svi_termini_projekcija, termin_projekcije)
            if izabrano_sediste == None:
                return
            sve_karte[id_karte] = {
                "Korisnik": trenutni_korisnik,
                "Šifra termina": termin_projekcije,
                "Sedište": izabrano_sediste,
                "Datum prodaje": datetime.today().strftime('%d.%m.%Y.'),
                "Status karte": "REZERVISANA",
                "Validnost": "VALIDNA",
                "Prodavac": "",
                "Cena karte": "",
                "Uloga": uloga if prodavac else "Registrovani kupac"
            }
            
            with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                for id_karte, podaci in sve_karte.items():
                    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                        str(id_karte), podaci["Korisnik"],podaci["Šifra termina"],
                        podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                        podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                    )
            
            console.print("[green3]\nKarta uspešno rezervisana![/]")
            print("ID karte:", id_karte)
            print()

def ponistavanje_karte(sve_karte, svi_termini_projekcija, trenutni_korisnik, svi_korisnici, prodavac=False):
    if prodavac:
        karta = pregled_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik, svi_korisnici, True)
        moguce_sifre = []
        for id, podaci in sve_karte.items():
            if podaci["Validnost"] == "VALIDNA":
                korisnik = podaci["Korisnik"]
                moguce_sifre.append(str(id))
    else:
        karta = pregled_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik, svi_korisnici)
        korisnik = trenutni_korisnik
        moguce_sifre = []
        for id, podaci in sve_karte.items():
            korisnik = podaci["Korisnik"]
            if korisnik == trenutni_korisnik:
                moguce_sifre.append(str(id))

    if karta == None:
        return
    while True:
        unos = input("Šifra karte koju poništavate: ")
        if unos.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        
        if unos not in moguce_sifre:
            console.print("[bright_red]\nNEVALIDAN UNOS.[/]\n")
            continue

        print('Ukoliko želite da poništite rezervaciju karte, unesite "DA", u suprotnom unesite "x".')
        izbor = input("Biram: ").lower()
        if izbor == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break

        elif izbor == "da":
            with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                if prodavac:
                    for id_karte, podaci in sve_karte.items():
                        if str(id_karte) == unos:
                            podaci["Validnost"] = "NEVALIDNA"
                            oslobadjanje_sedista(svi_termini_projekcija[podaci["Šifra termina"]]["Sedišta"], podaci["Sedište"].split("-"))
                        
                        fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                            int(id_karte), podaci["Korisnik"], podaci["Šifra termina"],
                            podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                            podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                        )
                else:
                    for id_karte, podaci in sve_karte.items():
                        if str(id_karte) == unos and trenutni_korisnik == podaci["Korisnik"]:
                            podaci["Validnost"] = "NEVALIDNA"
                            oslobadjanje_sedista(svi_termini_projekcija[podaci["Šifra termina"]]["Sedišta"], podaci["Sedište"].split("-"))
                
                        fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                            int(id_karte), podaci["Korisnik"], podaci["Šifra termina"],
                            podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                            podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                        )

            console.print("[green3]\nUspešno ste poništili kartu.\n[/]")
            
        else:
            console.print("[bright_red]\nNEVALIDAN UNOS.[/]\n")
               
def prodaja_rezervisanih_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik, svi_korisnici):
    while True:
        moguce_sifre = []
        for id, podaci in sve_karte.items():
            if podaci["Status karte"] == "REZERVISANA" and podaci["Validnost"] == "VALIDNA":
                sifra_termina = podaci["Šifra termina"]
                moguce_sifre.append(str(id))
        if len(moguce_sifre) == 0:
            console.print("[bright_red]\nNema rezervisanih karata.[/]\n")
            return
        unos = input("Šifra karte koju prodajete: ")
        if unos.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        
        if unos not in moguce_sifre:
            console.print("[bright_red]\nNEVALIDAN UNOS.[/]\n")
            continue

        print('Ukoliko želite da prodate karte, unesite "DA", u suprotnom unesite "x".')
        izbor = input("Biram: ").lower()
        if izbor == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break

        elif izbor == "da":
            with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                for id_karte, podaci in sve_karte.items():
                    if str(id_karte) == unos:
                        sifra_termina = podaci["Šifra termina"]
                        cena_karte = float(svi_termini_projekcija[sifra_termina]["Cena karte"])
                        dan_projekcije = svi_termini_projekcija[sifra_termina]["Dan projekcije"]
                        kor_ime = podaci["Korisnik"]
                        if dan_projekcije == "utorak":
                            cena_karte = float(cena_karte) - 50.0
                        if dan_projekcije == "subota" or dan_projekcije == "nedelja":
                            cena_karte = float(cena_karte) + 50.0
                        if podaci["Uloga"] == "Registrovani kupac":
                            uloga = svi_korisnici[kor_ime]["Uloga"]
                            if uloga == "Kupac":
                                lista_datuma = []
                                for id, info in sve_karte.items():
                                    if info["Korisnik"] == kor_ime:
                                        datum_prve_kupovine = info["Datum prodaje"] 
                                        datum_prve_kupovine_novi = datetime.strptime(datum_prve_kupovine, "%d.%m.%Y.")
                                        lista_datuma.append(datum_prve_kupovine_novi)

                                if (float(svi_korisnici[kor_ime]["Lojalnost"]) > 5000.0) and (min(lista_datuma) + timedelta(days=365) >= datetime.today()):
                                    cena_karte = 0.9 * cena_karte

                        id2 = id_karte
                        podaci["Status karte"] = "PRODATA"
                        podaci["Cena karte"] = cena_karte 
                        podaci["Prodavac"] = trenutni_korisnik[0]
                    
                    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                        int(id_karte), podaci["Korisnik"], podaci["Šifra termina"],
                        podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                        podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                    )
            
            if sve_karte[int(unos)]["Uloga"] == "Registrovani kupac":
                korisnik = sve_karte[int(unos)]["Korisnik"]
                fajl = open("Svi entiteti/korisnici.txt", "w", encoding="utf8")
                
                for kor_ime, podaci in svi_korisnici.items():
                    uloga = podaci["Uloga"]
                    lozinka = podaci["Lozinka"]
                    ime = podaci["Ime"]
                    prezime = podaci["Prezime"]
                    lojalnost = podaci["Lojalnost"]
                    if kor_ime == korisnik:
                        if min(lista_datuma) + timedelta(days=365) < datetime.today():
                            lojalnost = 0.0
                        lojalnost = float(lojalnost) + float(cena_karte)
                        podaci["Lojalnost"] = lojalnost
                        
                    if uloga == "Kupac":   
                        fajl.write("{}|{}|{}|{}|{}|{}\n".format(kor_ime, lozinka, ime, prezime, uloga, lojalnost))

                fajl.close()
            
            console.print("[green3]\nKarta uspešno prodata![/]")
            print("ID karte:", id2)
            print()
        else:
            console.print("[bright_red]\nNEVALIDAN UNOS.[/]\n")

def direktna_prodaja(svi_termini_projekcija, svi_korisnici, sve_sale, sve_karte, trenutni_korisnik):
    while True:
        sifra_termina = validacija_termina(svi_termini_projekcija)
        if sifra_termina == None:
            break
        korisnik = input("Unesite ime i prezime neregistrovanog kupca ili korisničko ime registrovanog kupca: ").strip()
        if korisnik.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        korisnik = korisnik.split(" ")
        if (len(korisnik) == 1) and (korisnik[0] not in svi_korisnici.keys()):
            console.print("[bright_red]\nUneto korisničko ime nije u sistemu.[/]\n")
    
            continue
        elif (len(korisnik) == 1) and (korisnik[0] in svi_korisnici.keys()):
            uloga = "Registrovani kupac"
        else:
            uloga = "Neregistrovani kupac"
        korisnik = (" ").join(korisnik)
        
        sedista = svi_termini_projekcija[sifra_termina]["Sedišta"]
        while True:
            if len(sve_karte.keys()) == 0:
                id_karte = 1000
            else:
                id_karte = max(sve_karte.keys()) + 1
            izabrano_sediste = zauzimanje_sedista(sedista, sve_sale, svi_termini_projekcija, sifra_termina)
            if izabrano_sediste == None:
                break

            print('Ukoliko želite da prodate karte, unesite "DA", u suprotnom unesite "x".')
            izbor = input("Biram: ").lower()
            if izbor == "x":
                console.print("[bright_red]\nOTKAZANO.[/]\n")
                oslobadjanje_sedista(sedista, izabrano_sediste.split("-"))
                break

            elif izbor == "da":
                cena_karte = float(svi_termini_projekcija[sifra_termina]["Cena karte"])
                dan_projekcije = svi_termini_projekcija[sifra_termina]["Dan projekcije"]

                sve_karte[id_karte] = {
                    "Korisnik": korisnik,
                    "Šifra termina": sifra_termina,
                    "Sedište": izabrano_sediste,
                    "Datum prodaje": datetime.strftime(datetime.today(), "%d.%m.%Y."),
                    "Status karte": "PRODATA",
                    "Validnost": "VALIDNA",
                    "Prodavac": trenutni_korisnik,
                    "Cena karte": cena_karte,
                    "Uloga": uloga
                }

                if dan_projekcije == "utorak":
                    cena_karte = float(cena_karte) - 50.0
                if dan_projekcije == "subota" or dan_projekcije == "nedelja":
                    cena_karte = float(cena_karte) + 50.0
                if uloga == "Registrovani kupac":
                    uloga2 = svi_korisnici[korisnik]["Uloga"]
                    if uloga2 == "Kupac":
                        lista_datuma = []
                        for id, info in sve_karte.items():
                            if info["Korisnik"] == korisnik:
                                datum_prve_kupovine = info["Datum prodaje"] 
                                datum_prve_kupovine_novi = datetime.strptime(datum_prve_kupovine, "%d.%m.%Y.")
                                lista_datuma.append(datum_prve_kupovine_novi)

                        if (float(svi_korisnici[korisnik]["Lojalnost"]) > 5000.0) and (min(lista_datuma) + timedelta(days=365) >= datetime.today()):
                            cena_karte = 0.9 * cena_karte
                
                sve_karte[id_karte]["Cena karte"] = cena_karte

                with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                    for id_karta, podaci in sve_karte.items():
                        
                        fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                            int(id_karta), podaci["Korisnik"], podaci["Šifra termina"],
                            podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                            podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                        )
                
                if sve_karte[id_karte]["Uloga"] == "Registrovani kupac":
                    korisnik = sve_karte[id_karte]["Korisnik"]
                    fajl = open("Svi entiteti/korisnici.txt", "w", encoding="utf8")
                    
                    for kor_ime, podaci in svi_korisnici.items():
                        uloga3 = podaci["Uloga"]
                        lozinka = podaci["Lozinka"]
                        ime = podaci["Ime"]
                        prezime = podaci["Prezime"]
                        lojalnost = podaci["Lojalnost"]
                        if kor_ime == korisnik:
                            if min(lista_datuma) + timedelta(days=365) < datetime.today():
                                lojalnost = 0.0
                            lojalnost = float(lojalnost) + float(cena_karte)
                            podaci["Lojalnost"] = lojalnost
                            
                        if uloga3 == "Kupac":   
                            fajl.write("{}|{}|{}|{}|{}|{}\n".format(kor_ime, lozinka, ime, prezime, uloga3, lojalnost))

                    fajl.close()
                
                console.print("[green3]\nKarta uspešno prodata![/]")
                print("ID karte:", id_karte)
                print()
            else:
                console.print("[bright_red]\nNEVALIDAN UNOS.[/]\n")
                oslobadjanje_sedista(sedista, izabrano_sediste.split("-"))

def izmena_karata(sve_karte, svi_korisnici, svi_termini_projekcija, sve_sale):
    print("Ukoliko želite da prekinete proces izmene podataka, unesite x.")
    moguce_karte = set(list(sve_karte.keys()))
    while True:
        pronadjene_karte = set()
        ids = input("Unesite šifru termina projekcije: ").upper()
        if ids.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        for id_karte, podaci in sve_karte.items():
            if podaci["Validnost"] != "VALIDNA":
                continue
            if podaci["Šifra termina"] != ids:
                continue
            pronadjene_karte.add(id_karte)
        if len(pronadjene_karte) == 0:
            console.print("[bright_red]\nID nije ispravan, pokušajte ponovo.[/]\n")
            continue

        moguce_karte.intersection_update(pronadjene_karte)
        break

    while True:
        pronadjene_karte = set()
        ime_prezime = input("Unesite ime i prezime kupca: ").strip().lower()

        if ime_prezime == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return

        for id_karte, podaci in sve_karte.items():
            if podaci["Validnost"] != "VALIDNA":
                continue
            if podaci["Uloga"] == "Registrovani kupac":
                if svi_korisnici[podaci["Korisnik"]]["Ime"].lower() + " " + svi_korisnici[podaci["Korisnik"]]["Prezime"].lower() != ime_prezime:
                    continue
            if podaci["Uloga"] == "Neregistrovani kupac":
                if ime_prezime != podaci["Korisnik"].lower():
                    continue
            pronadjene_karte.add(id_karte)

        if len(pronadjene_karte) == 0:
            console.print("[bright_red]\nNema karte na to ime, pokušajte ponovo.[/]\n")
            continue

        moguce_karte.intersection_update(pronadjene_karte)
        break

    while True:
        pronadjene_karte = set()
        broj_sedista = input("Unesite broj sedišta (npr. 1-A): ").strip().upper()

        if broj_sedista.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        for id_karte, podaci in sve_karte.items():
            if podaci["Validnost"] != "VALIDNA": 
                continue
            if podaci["Sedište"] != broj_sedista:
                continue
            pronadjene_karte.add(id_karte)

        if len(pronadjene_karte) == 0:
            console.print("[bright_red]\nNema karte sa tim sedištem, pokušajte ponovo.[/]\n")
            continue
                
        moguce_karte.intersection_update(pronadjene_karte)
        break
    
    id_karte = list(moguce_karte)
    if len(id_karte) == 0:
        console.print("[bright_red]\nNema karte sa tim podacima.[/]\n")
        return
    id_karte = id_karte[0]
    

    print("\nIzaberite podatak koji želite da izmenite.")
    while True:
        print("    [1] Termin projekcije")
        print("    [2] Ime i prezime kupca")
        print("    [3] Sedište u sali")
        print("    [x] Otkazivanje")
        biram = input("\nBiram: ").strip().lower()
        if biram == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return

        elif biram == "1":
            while True:
                novi_ids = input("Unesite šifru novog termina projekcije: ").upper()
                if novi_ids.lower() == "x":
                    console.print("[bright_red]\nOTKAZANO.[/]\n")
                    return
                if novi_ids not in svi_termini_projekcija.keys():
                    console.print("[bright_red]\nŽeljeni termin projekcije nije u sistemu.[/]\n")
                    continue
                if svi_termini_projekcija[novi_ids]["Validnost"] == "NEVALIDNO":
                    console.print("[bright_red]\nŽeljeni termin projekcije nije validan.[/]\n")
                    continue
                if novi_ids == ids:
                    console.print("[bright_red]\nNovi i stari termin projekcije ne smeju biti isti.[/]\n")
                    continue
                if novi_ids[:-2] != ids[:-2]:
                    console.print("[bright_red]\nMorate izabrati istu projekciju.[/]\n")
                    continue
                       
                oslobadjanje_sedista(svi_termini_projekcija[ids]["Sedišta"], broj_sedista.split("-"))
                novo_sediste = zauzimanje_sedista(svi_termini_projekcija[novi_ids]["Sedišta"], sve_sale, svi_termini_projekcija, novi_ids)
                with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                    for id, podaci in sve_karte.items():
                        if int(id) == int(id_karte):
                            podaci["Sedište"] = novo_sediste
                            podaci["Šifra termina"] = novi_ids
                        fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                            int(id), podaci["Korisnik"], podaci["Šifra termina"],
                            podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                            podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                        )
                console.print("[green3]\nUspešno ste izmenili kartu[/]", str(id_karte), "\n")
                break


        elif biram == "2":
            trenutni_korisnik = sve_karte[id_karte]["Korisnik"]
            while True:
                novi_korisnik = input("Unesite ime i prezime neregistrovanog kupca ili korisničko ime registrovanog kupca: ").strip()
                if novi_korisnik.lower() == "x":
                    console.print("[bright_red]\nOTKAZANO.[/]\n")
                    break
                if trenutni_korisnik == novi_korisnik:
                    console.print("[bright_red]\nNovi i stari korisnik ne smeju biti isti.[/]\n")
                    continue
                novi_korisnik = novi_korisnik.split(" ")
                if (len(novi_korisnik) == 1) and (novi_korisnik[0] not in svi_korisnici.keys()):
                    console.print("[bright_red]\nUneto korisničko ime nije u sistemu.[/]\n")
                    continue
                elif (len(novi_korisnik) == 1) and (novi_korisnik[0] in svi_korisnici.keys()):
                    uloga = "Registrovani kupac"
                else:
                    uloga = "Neregistrovani kupac"
                novi_korisnik = (" ").join(novi_korisnik)
                dan_projekcije = svi_termini_projekcija[ids]["Dan projekcije"]

                with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                    for id, podaci in sve_karte.items():
                        if id == id_karte:
                            trenutni_korisnik = podaci["Korisnik"]
                            if podaci["Status karte"] == "PRODATA":
                                if podaci["Uloga"] == "Registrovani kupac":
                                    svi_korisnici[trenutni_korisnik]["Lojalnost"] = float(svi_korisnici[trenutni_korisnik]["Lojalnost"]) - float(podaci["Cena karte"])
                                cena_karte = float(svi_termini_projekcija[ids]["Cena karte"])
                                if dan_projekcije == "utorak":
                                    cena_karte = float(cena_karte) - 50.0
                                if dan_projekcije == "subota" or dan_projekcije == "nedelja":
                                    cena_karte = float(cena_karte) + 50.0
                                if uloga == "Registrovani kupac":
                                    uloga2 = svi_korisnici[novi_korisnik]["Uloga"]
                                    if uloga2 == "Kupac":
                                        lista_datuma = []
                                        for id2, info in sve_karte.items():
                                            if info["Korisnik"] == novi_korisnik:
                                                datum_prve_kupovine = info["Datum prodaje"] 
                                                datum_prve_kupovine_novi = datetime.strptime(datum_prve_kupovine, "%d.%m.%Y.")
                                                lista_datuma.append(datum_prve_kupovine_novi)

                                            if (float(svi_korisnici[novi_korisnik]["Lojalnost"]) > 5000.0) and (min(lista_datuma) + timedelta(days=365) >= datetime.today()):
                                                cena_karte = 0.9 * cena_karte
                                    
                                podaci["Cena karte"] = cena_karte 
                            podaci["Uloga"] = uloga
                            podaci["Korisnik"] = novi_korisnik
                        

                        fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                            int(id), podaci["Korisnik"], podaci["Šifra termina"],
                            podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                            podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                        )

                    fajl = open("Svi entiteti/korisnici.txt", "w", encoding="utf8")
                    
                    for kor_ime, podaci in svi_korisnici.items():
                        uloga = podaci["Uloga"]
                        lozinka = podaci["Lozinka"]
                        ime = podaci["Ime"]
                        prezime = podaci["Prezime"]
                        lojalnost = podaci["Lojalnost"]
                        cena_karte = sve_karte[id_karte]["Cena karte"]
                        if kor_ime == novi_korisnik and uloga == "Kupac":
                            if sve_karte[id_karte]["Status karte"] == "PRODATA":
                                if min(lista_datuma) + timedelta(days=365) < datetime.today():
                                    lojalnost = 0.0
                                lojalnost = float(lojalnost) + float(cena_karte)
                        if uloga == "Kupac":
                            fajl.write("{}|{}|{}|{}|{}|{}\n".format(kor_ime, lozinka, ime, prezime, uloga, lojalnost))

                    fajl.close()
                console.print("[green3]\nUspešno ste izmenili kartu[/]", str(id_karte), "\n")
                break
            break
            
        elif biram == "3":
            oslobadjanje_sedista(svi_termini_projekcija[ids]["Sedišta"], broj_sedista.split("-"))
            novo_sediste = zauzimanje_sedista(svi_termini_projekcija[ids]["Sedišta"], sve_sale, svi_termini_projekcija, ids)
            with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
                for id, podaci in sve_karte.items():
                    if int(id) == int(id_karte):
                        podaci["Sedište"] = novo_sediste
                    fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                        int(id), podaci["Korisnik"], podaci["Šifra termina"],
                        podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                        podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                    )
            console.print("[green3]\nUspešno ste izmenili kartu[/]", str(id_karte), "\n")
            break

        else:
            console.print('[bright_red]\nNEVALIDAN UNOS.[/]\n')
        
def automatsko_ponistavanje(sve_karte, svi_termini_projekcija):
    for id_karte, podaci in sve_karte.items():
        if podaci["Status karte"] == "REZERVISANA" and podaci["Validnost"] == "VALIDNA":
            pocetak = svi_termini_projekcija[podaci["Šifra termina"]]["Početak projekcije"]
            datum = svi_termini_projekcija[podaci["Šifra termina"]]["Datum projekcije"]
            format_str = f"{datum} {pocetak}"
            pocetak_novi = datetime.strptime(format_str, "%d.%m.%Y. %H:%M")
            if pocetak_novi - timedelta(minutes=30) <= datetime.now():
                podaci["Validnost"] = "NEVALIDNA"
                oslobadjanje_sedista(svi_termini_projekcija[podaci["Šifra termina"]]["Sedišta"], podaci["Sedište"].split("-"))

    with open("Svi entiteti/karte.txt", "w", encoding="utf8") as fajl:
        for id_karte, podaci in sve_karte.items():
            fajl.write("{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(
                        int(id_karte), podaci["Korisnik"], podaci["Šifra termina"],
                        podaci["Sedište"], podaci["Datum prodaje"], podaci["Status karte"], 
                        podaci["Validnost"], podaci["Prodavac"], podaci["Cena karte"], podaci["Uloga"])
                )
    console.print("[green3]Uspešno ste poništili rezervisane karte za termine projekcija koji počinju za najviše 30 minuta.[/]\n")