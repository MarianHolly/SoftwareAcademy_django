from django.contrib import admin
from django.urls import path

from viewer.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    # path('movies/', movies, name='movies'),
    # path('movies/', MoviesView.as_view(), name='movies'),
    # path('movies/', MoviesTemplateView.as_view(), name='movies'),
    path('movies/', MoviesListView.as_view(), name='movies'),
    path('movie/<int:pk>/', MovieDetailsView.as_view(), name='movie'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<int:pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<int:pk>/', MovieDeleteView.as_view(), name='movie_delete'),

    path('creators/', CreatorListView.as_view(), name='creators'),
    path('creator/<int:pk>/', CreatorDetailsView.as_view(), name='creator'),
    path('creator/create/', CreatorCreateView.as_view(), name='creator_create'),
    path('creator/update/<int:pk>/', CreatorUpdateView.as_view(), name='creator_update'),
    path('creator/delete/<int:pk>/', CreatorDeleteView.as_view(), name='creator_delete'),

    path('genres/', GenresListView.as_view(), name='genres'),
    path('genre/<int:pk>/', GenreDetailsView.as_view(), name='genre'),
    path('genre/create/', GenreCreateView.as_view(), name='genre_create'),
    path('genre/update/<int:pk>/', GenreUpdateView.as_view(), name='genre_update'),
    path('genre/delete/<int:pk>/', GenreDeleteView.as_view(), name='genre_delete'),

    path('countries/', CountriesListView.as_view(), name='countries'),
    path('country/<int:pk>/', CountryDetailsView.as_view(), name='country'),
]
