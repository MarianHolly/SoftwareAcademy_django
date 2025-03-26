from django.shortcuts import render
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, CreateView, DeleteView

from viewer.forms import MovieForm, MovieModelForm, CreatorModelForm, GenreModelForm
from viewer.models import Creator, Movie, Genre, Country


# Create your views here.
def home(request):
    return render(request, 'home.html')


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


class MovieDetailsView(DetailView):
    template_name = 'movie.html'
    model = Movie
    context_object_name = 'movie'


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


class MovieCreateView(CreateView):
    template_name = 'form.html' # šablóna formulára pre vytvorenie
    form_class = MovieModelForm # trieda formulára pre validáciu a uloženie
    success_url = reverse_lazy('movies') # kam presmerovať po úspešnom vytvorení

    def form_invalid(self, form):
        print("Formulár nie je validný.")
        return super().form_invalid(form)


class MovieUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = MovieModelForm
    model = Movie # model, ktorý sa upravuje - automaticky predvyplní formulár existujúcimi dátami
    success_url = reverse_lazy('movies')

    def form_invalid(self, form):
        print("Formulár nie je validný.")
        return super().form_invalid(form)


class MovieDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Movie
    success_url = reverse_lazy('movies')


#todo: ======================== CREATORS ========================


class CreatorListView(ListView):
    template_name = 'creators.html'
    model = Creator
    context_object_name = 'creators'


class CreatorDetailsView(DetailView):
    template_name = 'creator.html'
    model = Creator
    context_object_name = 'creator'


class CreatorCreateView(CreateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    success_url = reverse_lazy('creators')

    def form_invalid(self, form):
        print("Formulár 'CreatorModelForm' nie je valídny.")
        return super().form_invalid(form)


class CreatorUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = CreatorModelForm
    model = Creator
    success_url = reverse_lazy('creators')

    def form_invalid(self, form):
        print("Formulár 'CreatorModelForm' nie je valídny.")
        return super().form_invalid(form)


class CreatorDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Creator
    success_url = reverse_lazy('creators')


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
        print("Validáčný problém s formulárom: 'GenreCreateView'")
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
    pass


class CountryUpdateView(UpdateView):
    pass


class CountryDeleteView(DeleteView):
    pass

