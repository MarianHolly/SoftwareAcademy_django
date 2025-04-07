import re
from datetime import date

from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.forms import Form, CharField, ModelChoiceField, IntegerField, Textarea, DateField, ModelForm, TextInput, NumberInput

from viewer.models import Country, Genre, Creator, Movie, Review, Image, Series, SeriesEpisode


# Prvý prístup
# Základný formulár (nie modelový), ktorý musí manuálne definovať všetky polia
class MovieForm(Form):
    title = CharField(max_length=64, required=True)
    title_en = CharField(max_length=64, required=False)
    genres = ModelChoiceField(queryset=Genre.objects.all(), required=False)
    countries = ModelChoiceField(queryset=Country.objects.all(), required=False)
    length = IntegerField(min_value=0, required=False)
    actors = ModelChoiceField(queryset=Creator.objects.all(), required=False)
    directors = ModelChoiceField(queryset=Creator.objects.all(), required=False)
    description = CharField(widget=Textarea, required=False)
    released_date = DateField(required=False)


class MovieModelForm(ModelForm):
    class Meta:
        """ Meta trieda definuje metadáta formulára
        - konfiguráciu ako sa má formulár správať a aké dáta má obsahovať. """
        model = Movie
        fields = '__all__'
        # fields = [ 'title', 'description']
        exclude = ['in_watchlist']

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
            'title': {
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

    # Predefinovať konštruktor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # zavolá inicializáciu nadriadenej triedy
        # Pridá CSS triedu 'form-control' pre všetky viditeľné polia (používa sa v Bootstrap)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    # DÔLEŽITÉ -- Formuláre sa najviac oplatí testovať
    def clean_title_orig(self):
        # Metódy s prefixom 'clean_' sa volajú pri validácii formulára.
        initial = self.cleaned_data['title']  # Získa zadanú hodnotu
        return initial.capitalize()  # Vráti hodnotu s prvým písmenom veľkým

    def clean_title_en(self):
        initial = self.cleaned_data['title_en']
        if initial:  # Ak hodnota existuje (nie je prázdna)
            return initial.capitalize()  # Vráti hodnotu s prvým písmenom veľkým
        return initial

    def clean_length(self):
        # Kontroluje, či je dĺžka filmu kladné číslo.
        initial = self.cleaned_data['length']
        if initial is not None and initial <= 0:  # Ak hodnota existuje a je menšia alebo rovná nule
            raise ValidationError("Dĺžka filmu musí byť kladné číslo.")
        return initial


class CreatorModelForm(ModelForm):
    date_of_birth = DateField(required=False,
                              widget=NumberInput(attrs={'type': 'date'}),
                              label='Dátum narodenia')
    date_of_death = DateField(required=False,
                              widget=NumberInput(attrs={'type': 'date'}),
                              label='Dátum úmrtia')

    class Meta:
        model = Creator
        fields = '__all__'

        labels = {
            'name': 'Meno',
            'surname': 'Priezvisko',
            'country': 'Krajina',
            'date_of_birth': 'Dátum narodenia',
            'date_of_death': 'Dátum úmrtia',
            'biography': 'Biografia'
        }

    def clean_name(self):
        initial = self.cleaned_data['name']
        if initial:
            return initial.capitalize()
        return initial

    def clean_surname(self):
        initial = self.cleaned_data['surname']
        if initial:
            return initial.capitalize()
        return initial

    def clean_date_of_birth(self):
        initial = self.cleaned_data['date_of_birth']
        if initial and initial > date.today():
            raise ValidationError('Dátom narodenia nesmie byť v budúcnosti.')
        return initial

    def clean_date_of_death(self):
        initial = self.cleaned_data['date_of_death']
        if initial and initial > date.today():
            raise ValidationError('Dátom úmrtia nesmie byť v budúcnosti.')
        return initial

    def clean_biography(self):
        initial = self.cleaned_data['biography']
        # Rozdelenie textu na vety na základe ., !, ?
        sentences = re.split(r'(?<=[.!?])\s+', initial.strip())
        # Kapitalizácia každej vety a spojenie späť do textu
        return ' '.join(sentence.capitalize() for sentence in sentences if sentence)

    def clean(self):
        cleaned_data = super().clean()
        error_message = ''

        initial_name = cleaned_data.get('name', '')
        initial_surname = cleaned_data.get('surname', '')
        if not initial_name and not initial_surname:
            error_message += "Je nutné zadať meno nebo priezvisko (alebo oboje)."

        initial_date_of_birth = cleaned_data.get('date_of_birth')
        initial_date_of_death = cleaned_data.get('date_of_death')
        if initial_date_of_birth and initial_date_of_death and initial_date_of_death <= initial_date_of_birth:
            error_message += "Dátom úmrtia nesmie byť skôr, ako dátum narodenia."

        if error_message:
            raise ValidationError(error_message)

        return cleaned_data


class GenreModelForm(ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'

        labels = {
            'name': 'Názov'
        }

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()


class CountryModelForm(ModelForm):
    class Meta:
        model = Country
        fields = '__all__'

        labels = {
            'name': 'Názov',
            'flag': 'Vlajka'
        }

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()


class ReviewModelForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        labels = {
            'rating': 'Hodnotenie',
            'comment': 'Komentár'
        }

        rating = IntegerField(min_value=1, max_value=5, required=False)


class ImageModelForm(ModelForm):
    class Meta:
        model = Image
        fields = '__all__'


class SeriesModelForm(ModelForm):
    class Meta:
        model = Series
        fields = '__all__'

        labels = {
            'title': 'Názov',
            'title_en': 'Anglický názov',
            'description': 'Popis'
        }


class EpisodeModelForm(MovieModelForm):

    series = ModelChoiceField(queryset=Series.objects.all(), required=True, label='Serial')
    season = IntegerField(min_value=1, required=False, label='Sezona')
    episode = IntegerField(min_value=1, required=False, label='Epizoda')

    def __init__(self, *args, **kwargs):
        MovieModelForm.__init__(self, *args, **kwargs)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True

        series_episode = SeriesEpisode(
            title=self.cleaned_data['title'],
            title_en=self.cleaned_data['title_en'],
            # genres=self.cleaned_data['genres'],
            # countries=self.cleaned_data['countries'],
            length=self.cleaned_data['length'],
            # actors=self.cleaned_data['actors'],
            # directors=self.cleaned_data['directors'],
            description=self.cleaned_data['description'],
            released_date=self.cleaned_data['released_date'],
            series=self.cleaned_data['series'],
            season=self.cleaned_data['season'],
            episode=self.cleaned_data['episode']
        )

        if commit:
            series_episode.save()
        return series_episode

