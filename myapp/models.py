from django.db import models
from django.contrib.auth import validators
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import tempfile
from gtts import gTTS
from django.core.files import File
import os
from audio import settings
from django.contrib.auth.models import User
from io import BytesIO
from gtts import gTTS
from googletrans import Translator, constants
from pprint import pprint
from gtts import gTTS
from pdf2docx import parse
from googletrans import Translator, constants
from pprint import pprint
import docxpy

LANGUAGE_CHOICES = (
('hi', 'hi'),
('ml', 'ml'),
('ta', 'ta'),
('te', 'te'),
('kn', 'kn'),
)


MEMBERSHIP_CHOICES = (
('Premium', 'pre'),
('Free', 'free')
)

# Create your models here.
class Document(models.Model):
    document = models.FileField()
    user = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    language = models.CharField(
    choices=LANGUAGE_CHOICES, default='hi',
    max_length=30
      )
    created_on = models.DateTimeField(
    auto_now_add = True
      )

    
class Audio(models.Model):

    audio = models.FileField(upload_to='audio/')
    document_audio = models.ForeignKey(Document,related_name='user_document_Audio', on_delete=models.CASCADE, null = True, blank = True)





























class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=11, null=True, blank=True)
    desc = models.TextField()
    cr_date = models.DateField()

    def __str__(self):
        return self.name

# class Word(models.Model):
#     word = models.CharField(max_length=200)
#     audio = models.FileField(upload_to='audio/', blank=True)

#     def save(self, *args, **kwargs):
#         print(self.word)
#         audio = gTTS(text=self.word, lang='en', slow=True)

#         with tempfile.TemporaryFile(mode='wb') as f:
#             audio.write_to_fp(f)
#             file_name = '{}.mp3'.format(self.word)
#             self.audio.save(file_name, File(file=f))

#         super(Word, self).save(*args, **kwargs)


class Membership(models.Model):
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(
    choices=MEMBERSHIP_CHOICES, default='Free',
    max_length=30
      )
    price = models.IntegerField(default=0)

    def __str__(self):
       return self.membership_type

class UserMembership(models.Model):
    user = models.OneToOneField(User,     related_name='user_membership', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    def __str__(self):
       return self.user.username

class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    def __str__(self):
      return self.user_membership.user.username

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)