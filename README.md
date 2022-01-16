# DRS-Projekat-Tim1

Implementirati projekat koji simulira međunarodni platni promet i on-line račun za lične uplate.

Implementacija treba da sadrži 3 komponente:

1.	Korisnički interfejs (UI)
2.	Servis za obradu zahteva I podataka (Engine)
3.	Bazu podataka (DB)

## Korisnički interfejs (UI)

Korisnički interfejs je Flask web aplikacija koja treba da opsluži korisnika u interakciji sa platnim prometom. 

Akcije koje treba podržati na korisničkom interfejsu su:

1.	Registracija novog korisnika
2.	Logovanje postojećeg korisnika
3.	Izmena korisničkog profila
4.	Pregled stanja
5.	Ubacivanje sredstava putem platne kartice na on-line račun
6.	Pregled istorije transakcija sa mogućnošću sortiranja I filtriranja
7.	Iniciranje nove transakcije drugom korisniku
	a)	Koji ima otvoren on-line racun
    b)	Na racun u banci
8.	Izbor valute – sa osvežavanjem kursne liste sa interneta
9.	Zamena valute

Korisnik se registruje unoseći:
1.	Ime
2.	Prezime
3.	Adresa
4.	Grad
5.	Država
6.	Broj telefona
7.	Email
8.	Lozinka

Korisnike se loguje putem:
1.	Email
2.	Lozinka

Novi korisnik ima stanje 0. On tada treba da zatraži verifikaciju naloga. Za verifikaciju je potrebno da unese svoju platnu karticu i biće mu skinuto 1$. Nakon toga korisnik može da uplati sredstva sa kartice na svoj on-line racun.

Test platna kartica:

Broj: 4242 4242 4242 4242
Ime: <Ime Korisnika>
Datum isteka kartice: 02/23
Sigurnosni kod: 123

Korisnik inicira transakciju drugom korisniku unoseći podatke o računu korisnika u banci ili njegovoj email adresi ukoliko drugi korisnik ima registrovan nalog.

Kad se inicira transakcija, ona treba da se obradi na strani Engine-a. Transakcija ima stanja:

1.	U obradi
2.	Obrađeno
3.	Odbijeno

Potrebno vreme da se transakcija odobri je 2min. Za to vreme sistem mora da bude sposoban da odgovori na ostale zahteve.

Konverzija valute se vrši po principu da korisnik uplaćuje sa kartice na on-line racun u Dinarima. Kursna lista se dovlači sa eksternog API-a kursne liste. Nakon dobijanja liste, korisnik bira valutu i iznos. Nakon uspešne konverzije korisnik ima novo stanje u novoj valuti. Korisnik moze da ima neogranicen broj valuta I stanja racuna u valutama.


## Servis za obradu zahteva I podataka (Engine)

Engine je servis implementiran kao flask API aplikacija. Engine ima svoje endpointe koje prikazuje eksternom svetu (UI aplikaciji) za koriscenje. UI deo poziva endpointe Engine-a radi obrade raznih zahteva I podataka. Pri tome samo Engine komunicira sa bazom, a UI sa Engine-om.

## Bazapodataka (DB)

Baza podataka je u komunikaciji sa Engine-om za svrhu skladištenja podataka o aplikaciji. U bazi se skladište svi esencijalno bitni podaci za rad aplikacije. 

Model baze kao I tip baze (NoSQL, SQL) je proizvoljan.


## Način ocenjivanja

1.	Aplikacija je funkcionalna I postoji Flask aplikacija – 51 poen
	a.	Aplikacija se sastoji od 1 aplikacije bez baze koja je potpuno funkcionalna
2.	Implementiran Engine kao posebna Flask aplikacija gde UI komunicira sa Engine-om putem API-a – 10 poena
3.	Implementirana je baza sa kojom komunicira Engine – 9 poena
4.	Korišćenje niti prilikom implementacije – 10 poena
5.	Korišćenje procesa prilikom implementacije – 10 poena
6.	Dokerizacija aplikacije I pokretanje na više računara (distribuiran sistem) – 10 poena

•	Deploy aplikacije na Heroku – gratis 5 poena (moguće samo ako je svih 6 tačaka implementirano)
  
___
Milan Stevanović PR128-2018

Nevena Panić PR43-2018

Mario Vrević PR71-2018

Vuk Milić PR56-2018
