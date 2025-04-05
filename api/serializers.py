from django.template.defaultfilters import length
from rest_framework.serializers import ModelSerializer

from viewer.models import Movie, Creator


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'title_en', 'length', 'description',
                  'released_date', 'genres', 'countries',
                  'actors', 'directors']
        #fields = '__all__'


class CreatorSerializer(ModelSerializer):
    class Meta:
        model = Creator
        fields = '__all__'