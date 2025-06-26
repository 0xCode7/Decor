from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    cart = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.user.username
