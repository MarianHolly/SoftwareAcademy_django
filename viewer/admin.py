from django.contrib import admin

from viewer.models import Country, Creator, Genre, Movie


# Register your models here.
admin.site.register(Country)
admin.site.register(Creator)
admin.site.register(Genre)
admin.site.register(Movie)
