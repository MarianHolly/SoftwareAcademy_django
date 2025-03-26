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

![ER_DIAGRAM](./files/er_diagram.png)

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

05.03

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

06.03

#### ORM modely
- Model predstavuje tabuľku v databáze a definuje sa v `models.py`
- Každý model je Python trieda, ktorá dedí od `django.db.models.Model`
- Polia modelov definujú stĺpce v databáze (CharField, IntegerField, DateField, atď.)
- Relácie medzi modelmi sa definujú pomocou ForeignKey, ManyToManyField, OneToOneField
- Modely môžu obsahovať metadáta, metódy a vlastnosti

#### Migrácie
- Migrácie slúžia na správu zmien v schéme databázy
- Vytvorenie migrácie: `python manage.py makemigrations`
- Aplikovanie migrácie: `python manage.py migrate`
- Migrácie umožňujú viesť históriu zmien v databáze
- Pomocou migrácie môžeme pridávať, meniť alebo mazať tabuľky a stĺpce
- Migrácie sa dajú vrátiť späť pomocou `python manage.py migrate app_name 0001`

#### Admin panel
- Django poskytuje automaticky generovaný admin panel
- Vytvorenie super užívateľa `python manage.py createsuperuser`
- Zaregistrovať modely do `admin.py` v aplikácií
- Registrácia modelov v `admin.py` pre zobrazenie v admin paneli

#### Shell
- Interaktívny Python shell s načítaným Django projektom: `python manage.py shell`
- Možnosť manipulácie s dátami bez webového rozhrania
- Testovanie ORM dotazov a operácií s modelmi
- Import modelov a práca s nimi priamo v shelli

Uložiť a načítať (DUMP/LOAD)
- Data môžeme exportovať z databáze `python manage.py dumpdata viewer --output fixtures.json`
- Data môžeme importovať do databázy `python manage.py loaddata fixtures.json`

07.03

#### Queries - dotazy
- Django ORM poskytuje API pre prácu s databázou
- Základné operácie: `objects.all()`, `objects.get()`, `objects.filter()`, `objects.exclude()`
  - `Movie.objects.filter(genres__name="Drama")`
  - `Movie.objects.filter(genres__name="Drama", released_date__year=1999)` 
- Porovnávacie operátory: `__exact`, `__contains`, `__startswith`, `__gt`, `__lt`, atď.
- Reťazenie dotazov (chaining): `Movie.objects.filter(rok__gt=2000).exclude(zanre__nazov="Horor")`
- Agregačné funkcie: `Count`, `Avg`, `Sum`, `Min`, `Max`
- Taktiež môžeme vytvoriť, editovať a vymazať z databazy
  - `Genre.objects.create(name='Dokument')`
  - `Movie.objects.filter(released_date__year=1994).update(length=123)`
  - `Genre.objects.get(name="Dokument").delete()`

#### Templates - šablóny
- Šablóny definujú vzhľad stránok v Django aplikácii
- Umiestnené v adresároch `templates` v aplikáciách
- Šablónový jazyk Django Template Language (DTL)
- Základné konštrukcie: premenné `{{ premenna }}`, bloky `{% block content %}`, podmienky `{% if %}`, cykly `{% for %}`
- Filtre pre formátovanie hodnôt: `{{ nazov|upper }}`, `{{ datum|date:"d.m.Y" }}`
- Dedičnosť šablón pomocou `{% extends "base.html" %}` a `{% block %}

#### Class-based views
- Zobrazenia implementované ako triedy namiesto funkcií
- Dedenie z tried ako `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`
- Jednoduchšie zdieľanie kódu medzi zobrazeniami
- Lepšie možnosti rozšírenia a prispôsobenia
- Jednoduchšia práca s formulármi a CRUD operáciami

#### Formuláre
- Vytvorenie formulárov pre manipuláciu s dátami
- Použitie `ModelForm` pre automatické generovanie formulárov z modelov
- Validácia vstupných dát
- Spracovanie formulárov v zobrazeniach
- Prispôsobenie vzhľadu formulárov pomocou CSS a widgetov
- Implementácia vlastných validačných metód





