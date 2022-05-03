from email.policy import default
from multiprocessing.dummy import Array
from statistics import mode
from unicodedata import name
from django.db import models
from matplotlib import container
from django.contrib.postgres.fields import ArrayField


class Wallet(models.Model):
    name = models.CharField(max_length=20)
    key = ArrayField(models.CharField(max_length=100), blank=True)
    value = ArrayField(models.CharField(max_length=100), blank=True)


class Post(models.Model):
    name = models.CharField(max_length=200)
    tags = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return self.name