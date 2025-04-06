import datetime
import os
import requests

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Avg
from django.db.models.expressions import result
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, CreateView, DeleteView

from accounts.models import Profile
from movies.settings import DEBUG
from viewer.forms import MovieForm, MovieModelForm, CreatorModelForm, GenreModelForm, CountryModelForm, ReviewModelForm, \
    ImageModelForm
from viewer.mixins import StaffRequiredMixin
from viewer.models import Creator, Movie, Genre, Country, Review, Image, Series, SeriesEpisode


# Create your views here.
def home(request):
    context = {
        'latest_movies': Movie.objects.all().order_by('-created')[:3],
        'latest_creators': Creator.objects.all().order_by('-created')[:3],
        'latest_reviews': Review.objects.all().order_by('-created')[:3],
    }
    return render(request, 'home.html', context)


#todo: ======================== MOVIES ========================


# Rôzne spôsoby ako vytvoriť views

"""def movies(request):
    return render(request, 'movies.html', {'movies': Movie.objects.all()})"""

"""class MoviesView(View):
    def get(self, request):
        return render(request, 'movies.html', {'movies': Movie.objects.all()})"""

"""class MoviesTemplateView(TemplateView):
    template_name = 'movies.html'
    extra_context = {'movies': Movie.objects.all()}"""


class MoviesListView(ListView):
    template_name = 'movies.html'
    model = Movie
    # Pozor, do template sa posielajú data pod názvom 'object_list'
    # Preto to premenujema na 'movies'
    context_object_name = 'movies'
    paginate_by = 20

    def get_queryset(self):
        movies_ = Movie.objects.exclude(id__in=SeriesEpisode.objects.values_list('id', flat=True))
        return movies_


class MovieDetailsView(DetailView):
    template_name = 'movie.html'
    model = Movie
    context_object_name = 'movie'


def movie(request, pk):
    if Movie.objects.filter(id=pk).exists():
        movie_ = Movie.objects.get(id=pk)
        profile_ = None
        if request.user.is_authenticated:
            profile_ = Profile.objects.get(user=request.user)

        if request.method == 'POST':
            # spracovanie formularu
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            # ak od užívatela máme review - tak ho aktualizujeme
            if Review.objects.filter(movie=movie_, reviewer=Profile.objects.get(user=request.user)).exists():
                user_review = Review.objects.get(movie=movie_, reviewer=profile_)
                user_review.rating = rating
                user_review.comment = comment
                user_review.save()
            else:
                Review.objects.create(
                    movie=movie_,
                    reviewer=profile_,
                    rating=rating,
                    comment=comment)

        rating_avg = movie_.reviews.aggregate(Avg('rating'))['rating__avg']
        rating_count = movie_.reviews.filter(rating__isnull=False).count()

        context = {'movie': movie_,
                   'review_form': ReviewModelForm,
                   'rating_avg': rating_avg,
                   'rating_count': rating_count,
                   'profile': profile_}
        return render(request, 'movie.html', context)
    return redirect('movies')


#todo: ======================== FORM - CREATE, EDIT, DELETE ========================


"""class MovieCreateView(FormView):
    template_name = 'form.html'
    form_class = MovieForm

    # Bez využitie dedičnosti
    def form_valid(self, form):
        result = super().form_valid(form)
        cleaned_data = form.cleaned_data
        Movie.objects.create(
            title=cleaned_data['title'],
            title_en=cleaned_data['title_en'],
        ) # vytvoriť novy objekt z prijatých dát
        return result

    def form_invalid(self, form):
        print("Formulár nie je validný.")"""


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html' # šablóna formulára pre vytvorenie
    form_class = MovieModelForm # trieda formulára pre validáciu a uloženie
    success_url = reverse_lazy('movies') # kam presmerovať po úspešnom vytvorení
    permission_required = 'viewer.add_movie'

    def form_invalid(self, form):
        print("Formulár nie je validný.")
        return super().form_invalid(form)


class MovieUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    model = Movie # model, ktorý sa upravuje - automaticky predvyplní formulár existujúcimi dátami
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.change_movie'

    def form_invalid(self, form):
        print("Formulár nie je validný.")
        return super().form_invalid(form)


class MovieDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('movies')
    permission_required = 'viewer.delete_movie'


#todo: ======================== CREATORS ========================


class CreatorListView(ListView):
    template_name = 'creators.html'
    model = Creator
    context_object_name = 'creators'
    paginate_by = 5


class CreatorDetailsView(DetailView):
    template_name = 'creator.html'
    model = Creator
    context_object_name = 'creator'


class CreatorCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.add_creator'

    def form_invalid(self, form):
        print("Formulár 'CreatorModelForm' nie je valídny.")
        return super().form_invalid(form)


class CreatorUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    model = Creator
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.change_creator'

    def form_invalid(self, form):
        print("Formulár 'CreatorModelForm' nie je valídny.")
        return super().form_invalid(form)


class CreatorDeleteView(#StaffRequiredMixin,
        PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Creator
    success_url = reverse_lazy('creators')
    permission_required = 'viewer.delete_creator'


#todo: ======================== GENRES ========================


class GenresListView(ListView):
    template_name = 'genres.html'
    model = Genre
    context_object_name = 'genres'


class GenreDetailsView(DetailView):
    template_name = 'genre.html'
    model = Genre
    context_object_name = 'genre'


class GenreCreateView(CreateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    success_url = reverse_lazy('genres')

    def form_invalid(self, form):
        print("Validáčný problém s formulárom: 'GenreModelForm'")
        return super().form_invalid(form)


class GenreUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = GenreModelForm
    model = Genre
    success_url = reverse_lazy('genres')


class GenreDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Genre
    success_url = reverse_lazy('genres')


#todo: ======================== COUNTRIES ========================


class CountriesListView(ListView):
    template_name = 'countries.html'
    model = Country
    context_object_name = 'countries'


class CountryDetailsView(DetailView):
    template_name = 'country.html'
    model = Country
    context_object_name = 'country'


class CountryCreateView(CreateView):
    template_name = 'form.html'
    form_class = CountryModelForm
    success_url = reverse_lazy('countries')


class CountryUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = CountryModelForm
    model = Country
    success_url = reverse_lazy('countries')

    def form_invalid(self, form):
        print("Validáčný problém s formulárom: 'CountryModelForm'")
        return super().form_invalid(form)


class CountryDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Country
    success_url = reverse_lazy('countries')


#todo: ======================== SEARCH ========================


def search(request):
    if request.method == 'POST':
        search_string = request.POST.get('search')
        if search_string:
            movies_title = Movie.objects.filter(title__contains=search_string)
            creator_surname = Creator.objects.filter(surname__contains=search_string)
            creator_name = Creator.objects.filter(name__contains=search_string)

            # Google search API
            url = (f"https://www.googleapis.com/customsearch/v1"
                   f"?key={os.getenv('GOOGLE_API_KEY')}"
                   f"&cx={os.getenv('GOOGLE_CX')}"
                   f"&q={search_string}")
            g_request = requests.get(url)
            if DEBUG:
                print(f"g_request: {g_request}")
            g_json = g_request.json()
            # print(f"g_json: {g_json}")
            if DEBUG:
                for g_result in g_json['items']:
                    print(g_result['title'])
                    print(f"\t{g_result['link']}")
                    print(f"\t{g_result['displayLink']}")
                    print(f"\t{g_result['snippet']}")

            context = {'search': search_string,
                       'movies_title': movies_title,
                       'movies_title_en': movies_title_en,
                       'movies_description': movies_description,
                       'movies_genre': movies_genre,
                       'movies_country': movies_country,
                       'creator_name': creator_name,
                       'creator_surname': creator_surname,
                       'creator_biography': creator_biography,
                       'g_json': g_json}
            return render(request, 'search.html', context)
    return render(request, 'home.html')


def movie_filter(request):
    if request.method == 'POST':
        filter_genre = request.POST.get('filter-genre').strip()
        filter_country = request.POST.get('filter-country').strip()
        filter_director = request.POST.get('filter-director').strip()

        filter_year_from = request.POST.get('filter-year-from').strip()
        filter_year_to = request.POST.get('filter-year-to').strip()

        filtered_movies = Movie.objects.all()

        if filter_genre:
            filtered_movies = filtered_movies.filter(genres__name__contains=filter_genre)
        if filter_country:
            filtered_movies = filtered_movies.filter(countries__name__contains=filter_country)
        if filter_director:
            filtered_movies = filtered_movies.filter(directors__surname__contains=filter_director)

        if filter_year_from:
            filtered_movies = filtered_movies.filter(released_date__year__gte=filter_year_from)
        if filter_year_to:
            filtered_movies = filtered_movies.filter(released_date__year__lte=filter_year_to)

        context = {'movies': filtered_movies}
        return render(request, 'movies.html', context)
    return render(request, 'home.html')


class ReviewDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Review
    success_url = reverse_lazy('movies')


#todo: ======================== IMAGES ========================


class ImageListView(ListView):
    template_name = 'images.html'
    model = Image
    context_object_name = 'images'


class ImageDetailView(DetailView):
    template_name = 'image.html'
    model = Image
    context_object_name = 'image'


class ImageCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('images')
    permission_required = 'viewer.add_image'


class ImageUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('images')
    model = Image
    permission_required = 'viewer.change_image'


class ImageDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Image
    success_url = reverse_lazy('images')


def name_day(request):
    month = datetime.date.today().month
    if month < 10:
        month = f"0{month}"
    day = datetime.date.today().day
    if day < 10:
        day = f"0{day}"
    url = f"https://svatky.adresa.info/json?date={day}{month}"
    result_request = requests.get(url)
    result_json = result_request.json()
    name = result_json[0]['name']
    context = {'name': name}
    return render(request, 'nameday.html', context)


def watchlist(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    movie_ = Movie.objects.get(id=pk)

    if movie_ in profile_.watchlist.all():
        profile_.watchlist.remove(movie_)
    else:
        profile_.watchlist.add(movie_)

    return redirect('movie', pk)


def watchlist_episode(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    movie_ = Movie.objects.get(id=pk)

    if movie_ in profile_.watchlist.all():
        profile_.watchlist.remove(movie_)
    else:
        profile_.watchlist.add(movie_)

    return redirect('episode', pk)


#todo: ======================== SERIES ========================


class SeriesListView(ListView):
    template_name = 'series.html'
    model = Series
    context_object_name = 'series'


class SeriesDetailView(DetailView):
    template_name = 'series_detail.html'
    model = Series
    context_object_name = 'series'


class EpisodeDetailView(DetailView):
    template_name = 'episode.html'
    model = SeriesEpisode
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_ = None
        is_in_watchlist = False
        if self.request.user.is_authenticated:
            profile_ = Profile.objects.get(user=self.request.user)
            is_in_watchlist = profile_ in context['movie'].in_watchlist.all()
        context['profile'] = profile_
        context['is_in_watchlist'] = is_in_watchlist
        if DEBUG:
            print(f'context: {context}')
        return context
