from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include

from accounts.views import *
from api.views import *
from viewer.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    # path('movies/', movies, name='movies'),
    # path('movies/', MoviesView.as_view(), name='movies'),
    # path('movies/', MoviesTemplateView.as_view(), name='movies'),
    path('movies/', MoviesListView.as_view(), name='movies'),
    # path('movie/<int:pk>/', MovieDetailsView.as_view(), name='movie'),

    path('movie/<int:pk>/', movie, name='movie'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('movie/update/<int:pk>/', MovieUpdateView.as_view(), name='movie_update'),
    path('movie/delete/<int:pk>/', MovieDeleteView.as_view(), name='movie_delete'),
    path('movie/filter/', movie_filter, name='movie_filter'),

    path('series/', SeriesListView.as_view(), name='series'),
    path('series/<int:pk>/', SeriesDetailView.as_view(), name='series_detail'),
    path('series/create/', SeriesCreateView.as_view(), name='series_create'),
    path('series/update/<int:pk>/', SeriesUpdateView.as_view(), name='series_update'),
    path('series/delete/<int:pk>/', SeriesDeleteView.as_view(), name='series_delete'),

    path('episode/<int:pk>/', EpisodeDetailView.as_view(), name='episode'),
    path('episode/watchlist/<int:pk>/', watchlist_episode, name='watchlist_episode'),
    path('episode/create/', EpisodeCreateView.as_view(), name='episode_create'),
    path('episode/update/<int:pk>/', EpisodeUpdateView.as_view(), name='episode_update'),
    path('episode/delete/<int:pk>/', EpisodeDeleteView.as_view(), name='episode_delete'),

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
    path('country/create/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),

    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('search/', search, name='search'),

    path('watchlist/<int:pk>/', watchlist, name='watchlist'),

    path('images/', ImageListView.as_view(), name='images'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image'),
    path('image/create/', ImageCreateView.as_view(), name='image_create'),
    path('image/update/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),
    path('image/delete/<int:pk>/', ImageDeleteView.as_view(), name='image_delete'),

    # ====================== ACCOUNTS
    # LOGIN pomocou LoginView - vyžaduje definovať template v 'registration/login.html'
    # path('accounts/login/', LoginView.as_view(), name='login'),

    # Preddefinovať akúkoľvek cestu
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    # DJANGO provides urls
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),

    # API
    path('nameday/', name_day, name='nameday'),
    path('api/movies/', Movies.as_view(), name='api_movies'),
    path('api/movie/<int:pk>/', MovieDetail.as_view(), name='api_movie'),
    path('api/creators/', Creators.as_view(), name='api_creators'),
    path('api/creator/<int:pk>/', CreatorDetail.as_view(), name='api_creator'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
