from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.core.validators import MaxLengthValidator, EmailValidator

class Student(AbstractUser):
    username = models.CharField(max_length=9, blank=False, validators=[MaxLengthValidator(9)], unique=True, error_messages={"unique": "This ID has already been used.", 'blank': "This field cannot be blank."})
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Please enter a valid email address.")],
        error_messages={
            'unique': "This email address is already in use.",
            'blank': "This field cannot be blank."
        }
    )
    password = models.CharField(max_length=15, blank=False, validators=[MaxLengthValidator(128)])

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        if not self.email and self.username:
            self.email = f"{self.username}@students.eui.edu.eg"
        super().save(*args, **kwargs)
