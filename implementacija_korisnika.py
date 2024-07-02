import validacija_korisnika
from rich.console import Console
console = Console()

def prijava(svi_korisnici, trenutni_korisnik):  
    from pwinput import pwinput
    print('Ukoliko želite da prekinete proces prijave, unesite "x".')
    while True:
        kor_ime = input("Unesite korisničko ime: ").strip()

        if kor_ime.lower() == "x": 
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        
        elif not kor_ime in svi_korisnici.keys():
            console.print("[bright_red]\nTo korisničko ime ne postoji.\n[/]")
        
        else:
            break
    
    while True:
        lozinka = pwinput("Unesite lozinku: ", "*").strip()
        if lozinka.lower() == "x": 
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        elif lozinka != svi_korisnici[kor_ime]["Lozinka"]:
            console.print("[bright_red]\nUneli ste pogrešnu lozinku.\n[/]")
        else:
            print()
            break
    
    trenutni_korisnik.append(kor_ime)
    
def odjava(trenutni_korisnik):
    odjavljeni_korisnik = trenutni_korisnik.pop()
    console.print("[green3]Uspešno ste se odjavili iz naloga:[/]", odjavljeni_korisnik)
    print()

def registracija(svi_korisnici, uloga="Kupac"):
    print('Ukoliko želite da prekinete proces registracije, unesite "x".')
    while True:
        kor_ime = input("Unesite korisničko ime: ").strip()
        if len(kor_ime) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.\n[/]")
        elif kor_ime.lower() == "x": 
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            return
        elif kor_ime in svi_korisnici.keys():
            console.print("[bright_red]\nKorisničko ime je zauzeto.\n[/]")
        elif "|" in kor_ime:
            console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena!\n[/]")
        elif " " in kor_ime:
            console.print("[bright_red]\nKorisničko ime mora biti spojeno ili odvojeno specijalnim karakterima.\n[/]")
        else:
            break

    lozinka = validacija_korisnika.validacija_lozinke()
    if lozinka.lower() == "x":
        return
    ime = validacija_korisnika.validacija_ime()
    if ime.lower() == "x":
        return
    prezime = validacija_korisnika.validacija_prezime()
    if prezime.lower() == "x":
        return
    lojalnost = 0.0
    svi_korisnici[kor_ime] = {
        "Lozinka": lozinka,
        "Ime": ime,
        "Prezime": prezime,
        "Uloga": uloga,
        "Lojalnost": lojalnost
    }

    if uloga == "Menadžer":
        ime_fajla = "menadzeri.txt"
        lojalnost = ""
    elif uloga == "Prodavac":
        ime_fajla = "prodavci.txt"
        lojalnost = ""
    else: 
        ime_fajla = "korisnici.txt"

    fajl = open("Svi entiteti/" + ime_fajla, "a", encoding="utf8")

    fajl.write("{}|{}|{}|{}|{}|{}\n".format(kor_ime, lozinka, ime, prezime, uloga, lojalnost))

    fajl.close()
    console.print("[green3]\nUspešna registracija.[/]\n")
    print("Prijavite se za više mogućnosti.\n")