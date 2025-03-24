## Django Project - Filmová aplikácia

**Filmová aplikácia**

- Zobrazenie zoznamu filmov
- Zobrazenie detailov filmu (názov, žáner, ...)
- Správa filmov v databáze: pridanie, úprava, mazanie
- Zobrazenie zoznamu hercov a režisérov (tvorcovia)
- Zobrazenie detailu (biografia) herca/režiséra
- Správa tvorcov v databáze: pridanie, úprava, mazanie
- Filtrovanie podľa žánru, krajiny, režiséra, herca, roku
- Hľadanie - Filmy, herci, režiséri

-----

### Databáza

- [x] Genre
  - [x] name (String) 

- [x] Country
  - [x] name (String) 
  - [x] flag (Image?) 

- [x] Creator
  - [x] name (String)
  - [x] surname (String)
  - [x] country (-> Country)
  - [x] date_of_birth (Date)
  - [x] date_of_death (Date)
  - [x] biography (String) 
  - [ ] awards (n:m -> ??)
  - [x] acting (n:m -> Movie)
  - [x] directing (n:m -> Movie) 

- [x] Movie
  - [x] title_orig (String)
  - [x] title_cz (String)
  - [x] genres (n:m -> Genre)
  - [x] countries (n:m -> Country)
  - [x] length (Integer)
  - [x] actors (n:m -> Creator)
  - [x] directors (n:m -> Creator)
  - [x] description (String)
  - [x] released_date (Date)
  - [ ] rating (Float)
  - [ ] images (1:n -> ??)
  - [ ] video_url (String)

- [ ] Review
  - [ ] reviewer (-> User) 
  - [ ] movie (-> Movie)
  - [ ] rating (Integer, 1-5 hvězdiček)
  - [ ] comment (String) 
  - [ ] created (DateTime)
  - [ ] updated (DateTime) 

- [ ] User (default from Django)

-----

### Základy Djanga

#### Vytvorenie projektu
- Django projekt sa vytvára príkazom `django-admin startproject názov_projektu`
- Vytvorí sa základná adresárová štruktúra s konfiguračnými súbormi
- Hlavný konfiguračný súbor `settings.py` obsahuje nastavenia celého projektu
- Súbor `urls.py` definuje hlavné URL mapovanie aplikácie
- Súbor `wsgi.py` slúži na komunikáciu s webovým serverom

#### Návrh funkcionality
- Identifikácia hlavných funkcií aplikácie (pridávanie, editácia, zobrazenie filmov a tvorcov)
- Určenie vzťahov medzi entitami (filmy, tvorcovia, žánre, atď.)

#### Návrh databázy
- Identifikácia tabuliek (Film, Tvorca, Žáner, atď.)
- Definícia atribútov pre každú tabuľku (názov filmu, rok vydania, atď.)
- Určenie vzťahov medzi tabuľkami (ManyToMany, ForeignKey, OneToOne)

#### Vytvorenie aplikácie
- V rámci projektu môžeme vytvoriť viacero aplikácií príkazom `python manage.py startapp názov_aplikácie`
- Každá aplikácia je samostatný balík s vlastnou funkcionalitou
- Aplikáciu treba registrovať v `INSTALLED_APPS` v súbore `settings.py`
- Aplikácia obsahuje súbory ako `models.py`, `views.py`, `urls.py`, `admin.py`, `apps.py` a adresár `templates`




