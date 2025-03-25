from django.forms import Form, CharField, ModelChoiceField, IntegerField, DateField, Textarea, ModelForm
from django.forms.widgets import TextInput, NumberInput

from viewer.models import Country, Genre, Creator, Movie


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
        # exclude = ['released_date']

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
            if initial and initial <= 0:  # Ak hodnota existuje a je menšia alebo rovná nule
                raise ValidationError("Dĺžka filmu musí byť kladné číslo.")
            return initial