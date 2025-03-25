from django.forms import Form, CharField, ModelChoiceField, IntegerField, DateField, Textarea, ModelForm

from viewer.models import Country, Genre, Creator


# Prvý prístup
# Základný formulár (nie modelový), ktorý musí manuálne definovať všetky polia
class MovieFormFirst(Form):
    title = CharField(max_length=64, required=True)
    title_en = CharField(max_length=64, required=False)
    genres = ModelChoiceField(queryset=Genre.objects.all(), required=False)
    countries = ModelChoiceField(queryset=Country.objects.all(), required=False)
    length = IntegerField(min_value=0, required=False)
    actors = ModelChoiceField(queryset=Creator.objects.all(), required=False)
    directors = ModelChoiceField(queryset=Creator.objects.all(), required=False)
    description = CharField(widget=Textarea, required=False)
    released_date = DateField(required=False)

class MovieForm(ModelForm):

    class Meta:
        """ Meta trieda definuje metadáta formulára
        - konfiguráciu ako sa má formulár správať a aké dáta má obsahovať. """
        model = Movie
        fields = '__all__'

        # Predefinovať popisy
        labels = {
            'title': 'Názov',
            'title_ed': 'Anglický názov',
            'genres': 'Žáner',
            'countries': 'Krajina',
            'length': 'Dĺžka',
            'actors': 'Herci',
            'directors': 'Režia',
            'description': 'Popis',
            'released_date': 'Dátum premiéry'
        }

        # Definuje pomocné texty vysvetľujúce účel polí
        help_texts = {
            'length': 'Dĺžka filmu má byť v minutách.',
            'description': 'Popis filmu, stručný obsah alebo iné detaily.'
        }

        # Definuje vlastné chybové hlášky pre validáciu
        error_messages = {
            'title_orig': {
                'required': 'Tento údaj je povinný.'
            }
        }

        # Predefinovanie polí s vlastnými nastaveniami
        title = CharField(max_length=64,
                          required=True,  # Pole je povinné
                          widget=TextInput(attrs={'class': 'bg-info'}),  # Vlastné CSS pre pole
                          label="Originálny názov")  # Vlastný popisok (prepíše hodnotu z Meta.labels)

        released_date = DateField(required=False,
                                  widget=NumberInput(attrs={'type': 'date'}),  # Použije sa HTML5 dátumový picker
                                  label="Dátum premiéry")