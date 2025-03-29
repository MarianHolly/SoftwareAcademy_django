from django.contrib import admin

from viewer.models import Country, Creator, Genre, Movie, Review

# Register your models here.
admin.site.register(Country)
admin.site.register(Creator)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Review)