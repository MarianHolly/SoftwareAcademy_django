import datetime

from django.db import IntegrityError
from django.test import TestCase

from viewer.models import *


class MovieModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        movie = Movie.objects.create(
            title="Názov filmu",
            title_en="Anglický názov filmu",
            length=123,
            description="Popis filmu",
            released_date=datetime.date(2000, 1, 1),
        )

        genre_comedy = Genre.objects.create(name="Komedia")
        movie.genres.add(genre_comedy)

        country_cz = Country.objects.create(name="Česko", flag="cz")
        movie.countries.add(country_cz)

        director = Creator.objects.create(
            name="Ján",
            surname="Novák",
            country=country_cz,
            date_of_birth=datetime.date(1975, 1, 1),
            biography="Životopis"
        )
        movie.directors.add(director)

        actor = Creator.objects.create(
            name="Anton",
            surname="Šimek",
            country=country_cz,
            date_of_birth=datetime.date(1969, 3, 1),
            biography="Životopis"
        )
        movie.actors.add(actor)

        movie.save()

    def setUp(self):
        print("-"*80)

    def test_title(self):
        movie = Movie.objects.get(id=1)
        print(f"test_title: '{movie.title}'")
        self.assertEqual(movie.title, "Názov filmu")

    def test_movie_countries_count(self):
        movie = Movie.objects.get(id=1)
        number_of_countries = len(movie.countries.all())
        print(f"test_movie_countries_count: {number_of_countries}")

    def test_movie_countries(self):
        movie = Movie.objects.get(id=1)
        number_of_countries = len(movie.countries.all())
        print(f"test_movie_countries: {number_of_countries}")

    def test_movie_repr(self):
        movie = Movie.objects.get(id=1)
        print(f"test_movie_repr: {movie.__repr__()}")
        self.assertEqual(movie.__repr__(),
                         "Movie(title_orig=Názov filmu, released_year=2000)")

    def test_genre_unique(self):
        """try:
            Genre.objects.create(name="Komedia")
        except IntegrityError as e:
            print(f"ERROR: {e}")"""
        comedy_count = Genre.objects.filter(name="Komedia").count()
        print(f"test_genre_unique: {comedy_count}")
        self.assertEqual(comedy_count, 1)