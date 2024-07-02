import implementacija_korisnika
import serijalizacija_korisnika
import serijalizacija_entiteta
import implementacija_entiteta
import pretrage_ispisi_entiteta
import rezervacije_prodaje
import izvestavanje
from rich.console import Console
console = Console()
from datetime import datetime


def dobrodoslica():
    console.print("\n\n[magenta]############################################################################[/]", style = "bold")
    console.print("[magenta]##########################[/] Dobro došli u bioskop! [magenta]##########################[/]", style = "bold")
    console.print("[magenta]############################[/] Radno vreme: 10-22 [magenta]############################[/]", style = "bold")
    console.print("[magenta]############################################################################[/]\n", style = "bold")
    
def izlazak():
    console = Console()
    console.print("\n[magenta]############################################################################[/]", style = "bold")
    console.print("[magenta]#################[/] Hvala što ste koristili našu aplikaciju! [magenta]#################[/]", style = "bold")
    console.print("[magenta]############################################################################[/]\n", style = "bold")
    exit()
    
if __name__ == "__main__":
    svi_korisnici = {}
    serijalizacija_korisnika.ucitaj_sve_korisnike(svi_korisnici)
    trenutni_korisnik = []
    
    svi_filmovi = {}
    serijalizacija_entiteta.ucitaj_filmove(svi_filmovi)
    
    sve_sale = {}
    zauzeta_sedista = []
    serijalizacija_entiteta.ucitaj_sve_sale(sve_sale)

    sve_projekcije = {}
    serijalizacija_entiteta.ucitaj_sve_projekcije(sve_projekcije, svi_filmovi)
    serijalizacija_entiteta.sacuvaj_projekcije(sve_projekcije)

    svi_termini_projekcija = {}
    serijalizacija_entiteta.ucitaj_sve_termine_projekcije(svi_termini_projekcija, sve_projekcije, sve_sale)
    
    datum_generisanja = serijalizacija_entiteta.ucitaj_datum_generisanja(svi_termini_projekcija)

    sve_karte = {}
    serijalizacija_entiteta.ucitaj_sve_karte(sve_karte, svi_termini_projekcija)
    rezervacije_prodaje.popuni_zauzeta_mesta(svi_termini_projekcija, sve_karte)
    
    dobrodoslica()

    while True:
        try:
            posetilac = len(trenutni_korisnik) == 0

            if posetilac:
                print("Nalazite se u meniju za neregistrovane korisnike. Izaberite opciju.")
                print("    [1]  Prijava")
                print("    [2]  Registracija")
                print("    [3]  Pregled dostupnih filmova")
                print("    [4]  Pretraga filmova")
                print("    [5]  Termini projekcija")
                print("    [x]  Izlazak iz aplikacije\n")
            else:
                uloga = svi_korisnici[trenutni_korisnik[0]]["Uloga"]
                console.print("[bright_magenta]Prijavljeni ste kao:[/] {} ({})".format(trenutni_korisnik[0], uloga.lower()))

                if uloga == "Menadžer":
                    print("    [0]  Odjava")
                    print("    [1]  Registracija novih zaposlenih")
                    print("    [2]  Unos, izmena i promena statusa filmova")
                    print("    [3]  Unos, izmena i promena statusa bioskopskih projekcija")
                    print("    [4]  Generisanje termina bioskopskih projekcija")
                    print("    [5]  Izveštavanje")
                    print("    [6]  Izmena ličnih podataka")
                    print("    [7]  Pregled dostupnih filmova")
                    print("    [8]  Pretraga filmova")
                    print("    [9]  Termini projekcija")
                    print("    [x]  Izlazak iz aplikacije\n")

                elif uloga == "Prodavac":
                    print("    [0]  Odjava")
                    print("    [1]  Rezervacija karata")
                    print("    [2]  Pregled karata")
                    print("    [3]  Poništavanje rezervisanih/prodatih karata")
                    print("    [4]  Pretraga karata")
                    print("    [5]  Direktna prodaja karata")
                    print("    [6]  Prodaja rezervisane karte")
                    print("    [7]  Izmena karte")
                    print("    [8]  Poništavanje rezervacije pola sata pre početka projekcije")
                    print("    [9]  Izmena ličnih podataka")
                    print("    [10] Pregled dostupnih filmova")
                    print("    [11] Pretraga filmova")
                    print("    [12] Termini projekcija")
                    print("    [x]  Izlazak iz aplikacije\n")
                else:
                    # kupac
                    print("    [0]  Odjava")
                    print("    [1]  Rezervacija karata")
                    print("    [2]  Pregled rezervisanih karata")
                    print("    [3]  Poništavanje rezervacije karata")
                    print("    [4]  Izmena ličnih podataka")
                    print("    [5]  Pregled dostupnih filmova")
                    print("    [6]  Pretraga filmova")
                    print("    [7]  Termini projekcija")
                    print("    [x]  Izlazak iz aplikacije\n")

            izbor = input("Biram: ").lower().strip()
            print()
            if izbor == "x":
                izlazak()

# Neregistrovani korisnik:               
            if posetilac:
                if izbor == "1":
                    implementacija_korisnika.prijava(svi_korisnici, trenutni_korisnik)
                elif izbor == "2":
                    implementacija_korisnika.registracija(svi_korisnici)
                elif izbor == "3":
                    pretrage_ispisi_entiteta.ispis_filmova(svi_filmovi)
                elif izbor == "4":
                    pretrage_ispisi_entiteta.pretraga_filmova(svi_filmovi)
                elif izbor == "5":
                    pretrage_ispisi_entiteta.pretraga_termina_projekcija(svi_termini_projekcija)
                else:
                    console.print("[bright_red]NEVALIDAN IZBOR.[/]\n")

            else:
                if izbor == "0":
                    implementacija_korisnika.odjava(trenutni_korisnik)
                    continue
# Menadžer:
                if uloga == "Menadžer":
                    if izbor == "1":
                        while True:
                            print("    [1]  Prodavac")
                            print("    [2]  Menadžer")
                            print("    [x]  Otkazivanje")
                            registrujem = input("\nKoga želite da registrujete? ").strip().lower()
                            print()
                            if registrujem == "x":
                                console.print("[bright_red]\nOTKAZANO.[/]\n")
                                break
                            elif registrujem == "1":
                                implementacija_korisnika.registracija(svi_korisnici, "Prodavac")
                                break
                            elif registrujem == "2":
                                implementacija_korisnika.registracija(svi_korisnici, "Menadžer")
                                break
                            else:
                                console.print("[bright_red]\nNEVALIDAN IZBOR.[/]\n")

                    elif izbor == "2":
                        while True:
                            print("    [1]  Unos novih filmova")
                            print("    [2]  Izmena filmova")
                            print("    [3]  Promena statusa filmova")
                            print("    [x]  Otkazivanje")
                            biram = input("\nBiram: ").strip().lower()
                            if biram == "x":
                                console.print("[bright_red]\nOTKAZANO.[/]\n")
                                break
                            elif biram == "1":
                                implementacija_entiteta.unos_novih_filmova(svi_filmovi)
                                break
                            elif biram == "2":
                                implementacija_entiteta.izmena_filmovi(svi_filmovi)
                                break
                            elif biram == "3":
                                implementacija_entiteta.brisanje_filmova(svi_filmovi)
                                serijalizacija_entiteta.ucitaj_sve_projekcije(sve_projekcije, svi_filmovi)
                                serijalizacija_entiteta.sacuvaj_projekcije(sve_projekcije)
                                break
                            else:
                                console.print("[bright_red]NEVALIDAN IZBOR.[/]\n")

                    elif izbor == "3":
                        while True:
                            print("    [1]  Unos novih projekcija")
                            print("    [2]  Izmena projekcija")
                            print("    [3]  Promena statusa projekcija")
                            print("    [x]  Otkazivanje")
                            biram = input("\nBiram: ").strip().lower()
                            if biram == "x":
                                console.print("[bright_red]\nOTKAZANO.[/]\n")
                                break
                            elif biram == "1":
                                implementacija_entiteta.unos_novih_projekcije(sve_projekcije, sve_sale)
                                break
                            elif biram == "2":
                                implementacija_entiteta.izmena_projekcija(sve_projekcije, svi_filmovi, sve_sale)
                                break
                            elif biram == "3":
                                implementacija_entiteta.brisanje_projekcija(sve_projekcije)
                                break
                            else:
                                console.print("[bright_red]NEVALIDAN IZBOR.[/]\n")
                    elif izbor == "4":
                        if datum_generisanja == "":
                            datum_generisanja = implementacija_entiteta.generisanje_termina_projekcija(sve_projekcije)
                            serijalizacija_entiteta.ucitaj_sve_termine_projekcije(svi_termini_projekcija, sve_projekcije, sve_sale)
                        elif datum_generisanja > datetime.today():
                            console.print("[bright_red]Ne možete generisati termine do sledećeg datuma:[/]", datetime.strftime(datum_generisanja, "%d.%m.%Y."), "\n")
                        else:
                            datum_generisanja = implementacija_entiteta.generisanje_termina_projekcija(sve_projekcije)
                            serijalizacija_entiteta.ucitaj_sve_termine_projekcije(svi_termini_projekcija, sve_projekcije, sve_sale)
                    elif izbor == "5":
                        while True:
                            print("    [a]  Lista prodatih karata za odabran datum prodaje")
                            print("    [b]  Lista prodatih karata za odabran datum termina bioskopske projekcije")
                            print("    [c]  Lista prodatih karata za odabran datum prodaje i odabranog prodavca")
                            print("    [d]  Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) prodaje")
                            print("    [e]  Ukupan broj i ukupna cena prodatih karata za izabran dan (u nedelji) održavanja projekcije")
                            print("    [f]  Ukupna cena prodatih karata za zadati film u svim projekcijama")
                            print("    [g]  Ukupan broj i ukupna cena prodatih karata za izabran dan prodaje i odabranog prodavca")
                            print("    [h]  Ukupan broj i ukupna cena prodatih karata po prodavcima (za svakog prodavca) u poslednjih 30 dana")
                            print("    [x]  Izlazak iz aplikacije")

                            biram = input("\nBiram: ").strip().lower()
                            if biram == "x":
                                console.print("[bright_red]\nOTKAZANO.[/]\n")
                                break
                            elif biram == "a":
                                izvestavanje.izvestaj_a(sve_karte, svi_termini_projekcija)
                                break
                            elif biram == "b":
                                izvestavanje.izvestaj_b(sve_karte, svi_termini_projekcija)
                                break
                            elif biram == "c":
                                izvestavanje.izvestaj_c(sve_karte, svi_termini_projekcija, svi_korisnici)
                                break
                            elif biram == "d":
                                izvestavanje.izvestaj_d(sve_karte)
                                break
                            elif biram == "e":
                                izvestavanje.izvestaj_e(sve_karte, svi_termini_projekcija)
                                break
                            elif biram == "f":
                                izvestavanje.izvestaj_f(sve_karte, svi_termini_projekcija)
                                break
                            elif biram == "g":
                                izvestavanje.izvestaj_g(sve_karte, svi_korisnici)
                                break
                            elif biram == "h":
                                izvestavanje.izvestaj_h(sve_karte, svi_korisnici)
                                break
                            else:
                                console.print("[bright_red]\nNEVALIDAN IZBOR.[/]\n")

                    elif izbor == "6":
                        serijalizacija_korisnika.izmena(svi_korisnici, trenutni_korisnik)
                    elif izbor == "7":
                        pretrage_ispisi_entiteta.ispis_filmova(svi_filmovi)
                    elif izbor == "8":
                        pretrage_ispisi_entiteta.pretraga_filmova(svi_filmovi)
                    elif izbor == "9":
                        pretrage_ispisi_entiteta.pretraga_termina_projekcija(svi_termini_projekcija)
                    else:
                        console.print("[bright_red]NEVALIDAN IZBOR.[/]\n")

# Prodavac:
                elif uloga == "Prodavac":
                    if izbor == "1":
                        rezervacije_prodaje.rezervacija_karata(sve_karte, svi_termini_projekcija, sve_sale, trenutni_korisnik[0], svi_korisnici, True)
                    elif izbor == "2":
                        pretrage_ispisi_entiteta.pregled_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik[0], svi_korisnici, True)
                    elif izbor == "3":
                        rezervacije_prodaje.ponistavanje_karte(sve_karte, svi_termini_projekcija, trenutni_korisnik[0], svi_korisnici, True)
                    elif izbor == "4":
                        pretrage_ispisi_entiteta.pretraga_karata(sve_karte, svi_termini_projekcija, svi_korisnici)
                    elif izbor == "5":
                        rezervacije_prodaje.direktna_prodaja(svi_termini_projekcija, svi_korisnici, sve_sale, sve_karte, trenutni_korisnik[0])
                    elif izbor == "6":
                        rezervacije_prodaje.prodaja_rezervisanih_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik, svi_korisnici)
                    elif izbor == "7":
                        rezervacije_prodaje.izmena_karata(sve_karte, svi_korisnici, svi_termini_projekcija, sve_sale)
                    elif izbor == "8":
                        rezervacije_prodaje.automatsko_ponistavanje(sve_karte, svi_termini_projekcija)
                    elif izbor == "9":
                        serijalizacija_korisnika.izmena(svi_korisnici, trenutni_korisnik)
                    elif izbor == "10":
                        pretrage_ispisi_entiteta.ispis_filmova(svi_filmovi)
                    elif izbor == "11":
                        pretrage_ispisi_entiteta.pretraga_filmova(svi_filmovi)
                    elif izbor == "12":
                        pretrage_ispisi_entiteta.pretraga_termina_projekcija(svi_termini_projekcija)
                    else:
                        console.print("[bright_red]NEVALIDAN IZBOR.[/]\n")

# Kupac:
                elif uloga == "Kupac":
                    if izbor == "1":
                        rezervacije_prodaje.rezervacija_karata(sve_karte, svi_termini_projekcija, sve_sale, trenutni_korisnik[0], svi_korisnici)
                    elif izbor == "2":
                        pretrage_ispisi_entiteta.pregled_karata(sve_karte, svi_termini_projekcija, trenutni_korisnik[0], svi_korisnici)
                    elif izbor == "3":
                        rezervacije_prodaje.ponistavanje_karte(sve_karte, svi_termini_projekcija, trenutni_korisnik[0], svi_korisnici)
                    elif izbor == "4":
                        serijalizacija_korisnika.izmena(svi_korisnici, trenutni_korisnik)
                    elif izbor == "5":
                        pretrage_ispisi_entiteta.ispis_filmova(svi_filmovi)
                    elif izbor == "6":
                        pretrage_ispisi_entiteta.pretraga_filmova(svi_filmovi)
                    elif izbor == "7":
                        pretrage_ispisi_entiteta.pretraga_termina_projekcija(svi_termini_projekcija)
                    else:
                        console.print("[bright_red]NEVALIDAN IZBOR.[/]\n")

        except KeyboardInterrupt:
            console.print("[bright_red]\n\nKeyboardInterrupt[/] uhvaćen. Izbacujemo Vas iz aplikacije. Prijatan dan!")
            izlazak()