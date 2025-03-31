from django.contrib import admin
from django.contrib.admin import ModelAdmin

from viewer.models import Country, Creator, Genre, Movie, Review


class MovieAdmin(ModelAdmin):

    # ListView
    @staticmethod
    def cleanup_description(modeladmin, request, queryset):
        queryset.update(description=None)

    ordering = ['title' ,'released_date']
    list_display = ['title', 'title_en', 'released_date']
    list_display_links = ['title', 'title_en' ,'released_date']
    list_per_page = 10
    list_filter = ['genres', 'countries']
    actions = ['cleanup_description']

    # FormView
    fieldsets = [
        (None, {
            'fields': [
                'title', 'title_en'
            ]
        }),
        ('External Information', {
            'fields': [
                'genres', 'countries', 'released_date', 'length'
            ]
        }),
        ('Creators', {
            'fields': [
                'directors', 'actors'
            ]
        }),
        ('User Information', {
            'fields': [
                'description'
            ]
        }),
        ('Internal Information', {
            'fields': [
                'created', 'updated'
            ]
        })
    ]
    readonly_fields = ['created', 'updated']


class CreatorAdmin(ModelAdmin):
    @staticmethod
    def cleanup_bio(modeladmin, request, queryset):
        queryset.update(biography=None)

    ordering = ['surname' ,'name']
    list_display = ['surname', 'name', 'country']
    list_display_links = ['surname', 'name' ,'country']
    list_per_page = 15
    actions = ['cleanup_bio']

    fieldsets = [
        ('Celé meno', {
            'fields': [
                'name', 'surname'
            ],
        }),
        ('Ďalšie informácie o tvorcovi', {
            'fields': [
                'date_of_birth', 'date_of_death', 'country'
            ]
        }),
        ('Biografia', {
            'fields': ['biography']
        }),
        ('Informácie o zázname', {
            'fields': ['created', 'updated']
        })
    ]
    readonly_fields = ['created', 'updated']



# Register your models here.
admin.site.register(Country)
admin.site.register(Creator, CreatorAdmin)
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)