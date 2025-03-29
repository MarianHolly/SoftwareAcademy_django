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

10.03

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

11.-12.03

#### Formuláre
- Vytvorenie formulárov pre manipuláciu s dátami
- `ModelForm` je špeciálny typ formulára v Django, ktorý automaticky generuje formulárové polia podľa modelu.
- Umožňuje jednoduché vytváranie formulárov priamo z existujúcich modelov. Zjednodušuje validáciu a ukladanie dát.
- Kľúčové komponenty formulára: 
  - **trieda Meta** 
    - model (určuje, ktorý model sa použije ako základ formulára)
    - fields (definuje, ktoré polia z modelu budú zahrnuté do formulára)
    - labels (labels: umožňuje prepísať pôvodné menovky polí)
  - **validačné metódy**
    - špeciálne metódy pre validáciu konkrétnych polí pred celkovou validáciou (kontrola dátumov)
    - globálna validácia (clean()) pre validáciu závislostí medzi viacerými poľami
- Prispôsobenie vzhľadu formulárov pomocou CSS a widgetov

12.03

#### Filtrovanie

#### Vyhľadávanie

24.03

#### Autentikácia
- registracia - login, logout - zmena hesla - reset hesla
- definovat login a zmeniť / upraviť template
- predefinocat user logout - z formulara na odkaz
- vytvorit prihlasovanie
- vytvorit profil z user - OneToOneField
- registracny formular vybrali len niektore polozky z user
- pridat polozky = rozsirenie formularu
- @atomic save method - okrem vytvorit užívatela, aj vytvorit profil
- templats - podla prihlasenia zobrazovať prvky na stranke

- 25.03

#### Autorizácia
- PermissionRequiredMixins
- 403 Page - vytvorit vlastnu template for chybovu hlasku
- permission based - template prvky zobrazovat (permission_required)
- tvorenie skupin v admin (editory, creators,...)
- django umoznuje testovanie oprávnení

- Review feature
- spracovanie formularu a ulozenie na spravne miesto






