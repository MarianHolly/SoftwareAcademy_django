from django.shortcuts import render

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from viewer.models import Creator, Movie


# Create your views here.
def home(request):
    return render(request, 'home.html')

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


class CreatorListView(ListView):
    template_name = 'creators.html'
    model = Creator
    context_object_name = 'creators'


class CreatorDetailsView(DetailView):
    template_name = 'creator.html'
    model = Creator
    context_object_name = 'creator'