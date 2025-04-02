import datetime

from django.test import TestCase

from viewer.forms import CreatorModelForm, MovieModelForm
from viewer.models import Country, Creator, Genre


class CreatorFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name="Česko", flag="🇨🇿")
        Country.objects.create(name="Slovensko", flag="🇸🇰")

    def test_creator_form_is_valid(self):
        form = CreatorModelForm(
            data={
                'name': '     martin    ',
                'surname': '    novák ',
                'country': '1',
                'date_of_birth': '1965-02-12',
                'date_of_death': '2001-05-05',
                'biography': '         testovaci text pre biografiu. '
            }
        )
        self.assertTrue(form.is_valid())

    def test_creator_form_name_is_invalid(self):
        form = CreatorModelForm(
            data={
                'name': '         ',
                'surname': '     ',
                'country': '1',
                'date_of_birth': '1965-02-12',
                'date_of_death': '2001-05-05',
                'biography': '         testovaci text pre biografiu. '
            }
        )
        self.assertFalse(form.is_valid())

    def test_creator_form_date_of_bith_is_invalid(self):
        form = CreatorModelForm(
            data={
                'name': '     martin    ',
                'surname': '    novák ',
                'country': '1',
                'date_of_birth': '2036-02-12',
                'date_of_death': '2001-05-05',
                'biography': '         testovaci text pre biografiu. '
            }
        )
        self.assertFalse(form.is_valid())


class MovieFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country_cz = Country.objects.create(name="Česko", flag="🇨🇿")
        country_sk = Country.objects.create(name="Slovensko", flag="🇸🇰")

        Genre.objects.create(name="Drama")
        Genre.objects.create(name="Komedia")

        Creator.objects.create(
            name="Arnošt",
            surname="Novák",
            country=country_cz,
            date_of_birth=datetime.date(1975, 12, 10),
            biography="Režisér několika filmů."
        )

        Creator.objects.create(
            name="Bedřich",
            surname="Slováček",
            country=country_cz,
            date_of_birth=datetime.date(1969, 11, 5),
            biography="Skvělý herec"
        )

        Creator.objects.create(
            name="Cyril",
            surname="Novotný",
            country=country_sk,
            date_of_birth=datetime.date(1945, 3, 15),
            date_of_death=datetime.date(2005, 5, 25),
            biography="Mizerný herec"
        )

    def test_movie_form_is_valid(self):
        form = MovieModelForm(
            data={
                'title': '   samotáři   ',
                'title_en': '',
                'genres': ['1', '2'],
                'countries': ['1', '2'],
                'length': '0',
                'actors': ['2', '3'],
                'directors': ['1'],
                'description': '  popis filmu ',
                'released_date': '2002-02-05'
            }
        )
        self.assertFalse(form.is_valid())
