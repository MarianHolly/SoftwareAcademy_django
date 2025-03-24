from django.db.models import Model, CharField


# Create your models here.
class Genre(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Žánre'

    def __repr__(self):
        return f"Genre(name={self.name})"

    def __str__(self):
        return self.name


class Country(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    flag = CharField(max_length=4, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Krajiny"

    def __repr__(self):
        return f"Country(name={self.name}, flag={self.flag}"

    def __str__(self):
        return f"{self.name} {self.flag}"