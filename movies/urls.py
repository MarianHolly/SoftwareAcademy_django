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
    path('creators/', CreatorListView.as_view(), name='creators'),
    path('creator/<int:pk>/', CreatorDetailsView.as_view(), name='creator'),
]
