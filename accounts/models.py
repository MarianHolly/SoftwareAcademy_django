from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField, CASCADE, DateField, Model, TextField, ManyToManyField


# Create your models here.
class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    date_of_birth = DateField(null=True, blank=True)
    biography = TextField(null=True, blank=True)
    phone = TextField(null=True, blank=True)

    class Meta:
        ordering = ['user__username']

    def __repr__(self):
        return f"Profile(user={self.user})"

    def __str__(self):
        return self.user.username
