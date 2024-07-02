import validacija_korisnika
from rich.console import Console
console = Console()

def izmena(svi_korisnici, trenutni_korisnik):
    print('Ukoliko želite da prekinete proces izmene podataka, unesite "x".')
    while True:
        print("    [1] Lozinka")
        print("    [2] Ime")
        print("    [3] Prezime")
        print("    [x] Otkazivanje\n")
        izmena_cega = input("Šta želite da promenite? ").strip().lower()
        if izmena_cega.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        elif izmena_cega == "1":
            console.print("[dodger_blue2]\nVaša trenutna lozinka je:[/]", svi_korisnici[trenutni_korisnik[0]]["Lozinka"])
            while True:
                nova_lozinka = validacija_korisnika.validacija_lozinke()
                if nova_lozinka.lower() == "x":
                    return
                    
                elif nova_lozinka == svi_korisnici[trenutni_korisnik[0]]["Lozinka"]:
                    console.print("[bright_red]\nNova lozinka ne sme biti ista kao trenutna. Unesite ponovo.[/]\n")
                else:
                    svi_korisnici[trenutni_korisnik[0]]["Lozinka"] = nova_lozinka
                    break
            break

        elif izmena_cega == "2":
            console.print("[dodger_blue2]\nVaše trenutno ime je:[/]", svi_korisnici[trenutni_korisnik[0]]["Ime"])
            while True:
                novo_ime = validacija_korisnika.validacija_ime()
                if novo_ime.lower() == "x":
                    return
                elif novo_ime == svi_korisnici[trenutni_korisnik[0]]["Ime"]:
                    console.print("[bright_red]\nNova vrednost ne sme biti ista kao trenutna. Unesite ponovo.[/]\n")
                else:
                    svi_korisnici[trenutni_korisnik[0]]["Ime"] = novo_ime
                    break
            break

        elif izmena_cega == "3":
            console.print("[dodger_blue2]\nVaše trenutno prezime je:[/]", svi_korisnici[trenutni_korisnik[0]]["Prezime"])
            while True:
                novo_prezime = validacija_korisnika.validacija_prezime()
                if novo_prezime.lower() == "x":
                    return
                elif novo_prezime == svi_korisnici[trenutni_korisnik[0]]["Prezime"]:
                    console.print("[bright_red]\nNova vrednost ne sme biti ista kao trenutna. Unesite ponovo.[/]\n")
                else:
                    svi_korisnici[trenutni_korisnik[0]]["Prezime"] = novo_prezime
                    break
            break
        
        else:
            console.print("[bright_red]\nNEVALIDAN UNOS.[/]\n")

    uloga_trenutnog = svi_korisnici[trenutni_korisnik[0]]["Uloga"]

    if uloga_trenutnog == "Menadžer":
        ime_fajla = "menadzeri.txt"
    elif uloga_trenutnog == "Prodavac":
        ime_fajla = "prodavci.txt"
    else: 
        ime_fajla = "korisnici.txt"

    fajl = open("Svi entiteti/" + ime_fajla, "w", encoding="utf8")

    for kor_ime in svi_korisnici.keys():
        uloga = svi_korisnici[kor_ime]["Uloga"]
        if uloga == uloga_trenutnog:
            lozinka = svi_korisnici[kor_ime]["Lozinka"]
            ime = svi_korisnici[kor_ime]["Ime"]
            prezime = svi_korisnici[kor_ime]["Prezime"]
            lojalnost = svi_korisnici[kor_ime]["Lojalnost"]
            fajl.write("{}|{}|{}|{}|{}|{}\n".format(kor_ime, lozinka, ime, prezime, uloga, lojalnost))

    fajl.close()

    console.print("[green3]\nUspešno ste izmenili podatke.[/]\n")

def ucitaj_sve_korisnike(svi_korisnici):

    def ucitaj_pojedinacno(ime_fajla):
        fajl = open("Svi entiteti/" + ime_fajla, encoding="utf8")

        for linija in fajl:
            linija = linija.replace("\n","").split("|")
            
            svi_korisnici[linija[0]] = {
                "Lozinka": linija[1],
                "Ime": linija[2],
                "Prezime": linija[3],
                "Uloga": linija[4],
                "Lojalnost": linija[5]
            }

    ucitaj_pojedinacno("menadzeri.txt")
    ucitaj_pojedinacno("korisnici.txt")
    ucitaj_pojedinacno("prodavci.txt")