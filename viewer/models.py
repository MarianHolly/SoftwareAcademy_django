from importlib.metadata import requires

from django.db.models import DateField, DateTimeField, CharField, ForeignKey, IntegerField, ManyToManyField, Model, \
    SET_NULL, TextField, CASCADE, ImageField

from accounts.models import Profile


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


class Creator(Model):
    name = CharField(max_length=32, null=True, blank=True)
    surname = CharField(max_length=32, null=True, blank=True)
    country = ForeignKey(Country, null=True, blank=True, on_delete=SET_NULL, related_name='creators')
    date_of_birth = DateField(null=True, blank=True)
    date_of_death = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['surname', 'name', 'date_of_birth']
        verbose_name_plural = "Tvorcovia"

    def __repr__(self):
        return f"Creator(name={self.name}, surname={self.surname}, date_of_birth={self.date_of_birth})"

    def __str__(self):
        if self.date_of_birth:
            return f"{self.name} {self.surname} ({self.date_of_birth.year})"
        return f"{self.name} {self.surname}"

    def full_name(self):
        return f"{self.name} {self.surname}"

    def age(self):
        if self.date_of_birth:
            end_date = self.date_of_death or date.today()
            return (end_date.year - self.date_of_birth.year -
                    ((end_date.month, end_date.day) < (self.date_of_birth.month, self.date_of_birth.day)))
        return None


class Movie(Model):
    title = CharField(max_length=64, null=False, blank=False)
    title_en = CharField(max_length=64, null=True, blank=True)
    genres = ManyToManyField(Genre, blank=True, related_name='movies')
    countries = ManyToManyField(Country, blank=True, related_name='movies')
    length = IntegerField(null=True, blank=True)
    actors = ManyToManyField(Creator, blank=True, related_name='acting')
    directors = ManyToManyField(Creator, blank=True, related_name='directing')
    description = TextField(null=True, blank=True)
    released_date = DateField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    in_watchlist = ManyToManyField(Profile, blank=True, related_name='watchlist')

    class Meta:
        ordering = ['title', 'released_date']
        verbose_name_plural = "Filmy"

    def __repr__(self):
        return f"Movie(title_orig={self.title}, released_year={self.released_date.year})"

    def __str__(self):
        return f"{self.title} ({self.released_date.year})"

    def length_format(self):
        # Prevod dĺžky filmu z minút na formát h:m
        if self.length:
            hours = self.length // 60
            minutes = self.length % 60
            return f"{hours}:{minutes:02}"
        return None

    def released_date_format(self):
        if self.released_date:
            return (f"{self.released_date.day}. "
                    f"{self.released_date.month}. "
                    f"{self.released_date.year}")
        return None


class Review(Model):
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False, blank=False, related_name='reviews')
    reviewer = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=False, related_name='reviews')
    rating = IntegerField(null=True, blank=True) # 1-5 hviezdičiek
    comment = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __repr__(self):
        return (f"Review(movie={self.movie}), "
                f"reviewer={self.reviewer}, "
                f"rating={self.rating}, "
                f"comment={self.comment[:20]}, ")

    def __str__(self):
        return f"{self.reviewer} = {self.movie} - {self.rating}"


class Image(Model):
    image = ImageField(upload_to='images/', default=None, null=False, blank=False)
    movie = ForeignKey(Movie, on_delete=CASCADE, null=False, blank=False, related_name='images')
    creators = ManyToManyField(Creator, blank=True, related_name='images')
    description = TextField(null=True, blank=True)

    def __repr__(self):
        return f"Image (image={self.image})"

    def __str__(self):
        return f"Image: {self.image}"


class SeriesEpisode(Movie):
    season = IntegerField(null=False, blank=False)
    episode = IntegerField(null=False, blank=False)
    series = ForeignKey("Series", on_delete=CASCADE, null=False, blank=False, related_name='episodes')

    class Meta:
        ordering = ['series__title', 'season', 'episode']
        verbose_name_plural = "Seriálové epizódy"

    def __repr__(self):
        return f"Episode(title={self.title}, season={self.season}, episode={self.episode})"

    def __str__(self):
        return f"{self.series.title} - {self.title} - S{self.season:02d}E{self.episode:02d}"


class Series(Model):
    title = CharField(max_length=64, null=False, blank=False)
    title_en = CharField(max_length=64, null=True, blank=True)
    description = TextField(null=True, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Seriály"

    def __repr__(self):
        return f"Series(title={self.title})"

    def __str__(self):
        return f"{self.title}"
