from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms.fields import DateField, DateInput, CharField, Textarea
from django.forms.widgets import PasswordInput
from .models import Profile


# Registrácia nového užívateľa
class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2']

        labels = {
            'username': 'Užívateľské meno',
            'first_name': 'Meno',
            'last_name': 'Priezvisko',
            'email': 'E-mail',
        }

    password1 = CharField(widget=PasswordInput(attrs={'placeholder': 'Heslo'}), label='Heslo')
    password2 = CharField(widget=PasswordInput(attrs={'placeholder': 'Heslo znovu'}), label='Heslo znovu')
    date_of_birth = DateField(widget=DateInput(attrs={'type': 'date'}), label='Datum narodenia', required=False)
    biography = CharField(widget=Textarea, label='Biografia', required=False)
    phone = CharField(label='Telefon', required=False)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit) # vytvoriť uživateľa

        # vytvoriť Profil
        date_of_birth = self.cleaned_data.get('date_of_birth')
        biography = self.cleaned_data.get('biography')
        phone = self.cleaned_data.get('phone')
        profile = Profile(
            user=user,
            date_of_birth=date_of_birth,
            biography=biography,
            phone=phone,
        )

        if commit:
            profile.save()
        return user