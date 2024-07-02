from rich.console import Console
console = Console()

def validacija_lozinke():
    def sadrzi_broj(n):
        return any(broj.isdigit() for broj in n)

    while True:
        validna_lozinka = input("Unesite lozinku (duža od 6 karaktera sa bar jednom cifrom): ").strip()
        if validna_lozinka.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        if len(validna_lozinka) < 6:
            console.print("[bright_red]\nVaša lozinka nije duža od 6 karaktera.[/]\n")
        
        elif not sadrzi_broj(validna_lozinka):
            console.print("[bright_red]\nVaša lozinka ne sadrži broj.[/]\n")

        elif "|" in validna_lozinka:
           console.print("[bright_red]\nUpotreba karaktera | nije dozvoljena![/]\n")

        elif " " in validna_lozinka:
            console.print("[bright_red]\nLozinka mora biti spojena ili odvojena specijalnim karakterima.[/]\n")

        else:
            break

    return validna_lozinka

def validacija_ime():
    def sadrzi_broj(n):
        return any(karakter.isnumeric() for karakter in n)
    def sadrzi_spec_karaktere(n):
        return any(not karakter.isalnum() for karakter in n)

    while True:
        validno_ime = input("Unesite ime: ").strip()
        if validno_ime.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        elif sadrzi_broj(validno_ime) or sadrzi_spec_karaktere(validno_ime):
            console.print("[bright_red]\nUps... Niste uneli ime.[/]\n")
        elif len(validno_ime) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        else:
            break

    return validno_ime

def validacija_prezime():
    def sadrzi_broj(n):
        return any(karakter.isnumeric() for karakter in n)
    def sadrzi_spec_karaktere(n):
        return any(not karakter.isalnum() for karakter in n)
    
    while True:
        validno_prezime = input("Unesite prezime: ").strip()
        if validno_prezime.lower() == "x":
            console.print("[bright_red]\nOTKAZANO.[/]\n")
            break
        if sadrzi_broj(validno_prezime) or sadrzi_spec_karaktere(validno_prezime):
            console.print("[bright_red]\nUps... Niste uneli prezime.[/]\n")
        elif len(validno_prezime) == 0:
            console.print("[bright_red]\nPolje ne sme biti prazno.[/]\n")
        else:
            break

    return validno_prezime