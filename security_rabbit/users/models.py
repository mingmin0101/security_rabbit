from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
    # add additional fields in here

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username
