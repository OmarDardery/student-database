from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, EmailValidator
from cloudinary.models import CloudinaryField
from smart_selects.db_fields import ChainedForeignKey

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
    password = models.CharField(blank=False, validators=[MaxLengthValidator(128)])

    USERNAME_FIELD = 'username'
    banned= models.BooleanField(default=False, help_text="Indicates whether the user is banned from the system.")
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        if not self.email and self.username:
            self.email = f"{self.username}@students.eui.edu.eg"
        super().save(*args, **kwargs)

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.IntegerField(blank=False, error_messages={'blank': "This field cannot be blank."})
    TERM_CHOICES = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    ]
    term = models.CharField(max_length=6, choices=TERM_CHOICES)
    def __str__(self):
        return f"{self.year} - {self.get_term_display().capitalize()}"

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False, validators=[MaxLengthValidator(100)], unique=True, error_messages={"unique": "This subject name has already been used.", 'blank': "This field cannot be blank."})
    LEVEL_CHOICES = [
        ('1', 'Level 1'),
        ('2', 'Level 2'),
        ('3', 'Level 3'),
        ('4', 'Level 4'),
        ('5', 'Level 5'),
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    def __str__(self):
        return self.name

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    topic_name = models.CharField(max_length=100, blank=False, validators=[MaxLengthValidator(100)], error_messages={'blank': "This field cannot be blank."})
    def __str__(self):
        return self.topic_name

class Sheets(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sheets')
    sheet_name = models.CharField(max_length=100, blank=False, validators=[MaxLengthValidator(100)], error_messages={'blank': "This field cannot be blank."})
    sheet_file = CloudinaryField(
        'file',
        resource_type='raw',
        blank=False,
        error_messages={'blank': "This field cannot be blank."}
    )
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='sheets')
    topic = ChainedForeignKey(
        Topic,
        chained_field="subject",
        chained_model_field="subject",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        related_name='sheets'
    )
    def __str__(self):
        return self.sheet_name

class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    note_name = models.CharField(max_length=100, blank=False, validators=[MaxLengthValidator(100)], error_messages={'blank': "This field cannot be blank."})
    note_file = CloudinaryField(
        'file',
        resource_type='raw',
        blank=False,
        error_messages={'blank': "This field cannot be blank."}
    )
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='notes')
    topic = ChainedForeignKey(
        Topic,
        chained_field="subject",
        chained_model_field="subject",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        related_name='notes'
    )
    def __str__(self):
        return self.note_name

class Mcq(models.Model):
    id = models.AutoField(primary_key=True)
    posted_by = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mcqs'
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='mcqs')
    topic = ChainedForeignKey(
        Topic,
        chained_field="subject",
        chained_model_field="subject",
        show_all=False,
        auto_choose=True,
        sort=True,
        blank=True,
        null=True,
        related_name='mcqs'
    )
    pending = models.BooleanField(default=False)
    mcq_name = models.CharField(max_length=200, blank=False, validators=[MaxLengthValidator(200)], error_messages={'blank': "This field cannot be blank."})
    mcq_a = models.CharField(max_length=200, blank=False, validators=[MaxLengthValidator(200)], error_messages={'blank': "This field cannot be blank."})
    mcq_b = models.CharField(max_length=200, blank=False, validators=[MaxLengthValidator(200)], error_messages={'blank': "This field cannot be blank."})
    mcq_c = models.CharField(max_length=200, blank=False, validators=[MaxLengthValidator(200)], error_messages={'blank': "This field cannot be blank."})
    mcq_d = models.CharField(max_length=200, blank=False, validators=[MaxLengthValidator(200)], error_messages={'blank': "This field cannot be blank."})
    mcq_choices = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]
    mcq_answer = models.CharField(max_length=1, choices=mcq_choices, blank=False, error_messages={'blank': "This field cannot be blank."})

    def __str__(self):
        return self.mcq_name

class Link(models.Model):
    name = models.CharField(max_length=100, blank=False, validators=[MaxLengthValidator(100)], error_messages={'blank': "This field cannot be blank."})
    description = models.CharField(max_length=300, blank=False, validators=[MaxLengthValidator(300)], error_messages={'blank': "This field cannot be blank."})
    link = models.TextField(blank=False)
    pending = models.BooleanField(default=True)
    posted_by = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='links'
    )
    def __str__(self):
        return self.name

