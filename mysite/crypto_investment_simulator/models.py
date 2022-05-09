from email.policy import default
from multiprocessing.dummy import Array
from statistics import mode
from unicodedata import name
from django.db import models
from matplotlib import container
from django.contrib.postgres.fields import ArrayField


class Wallets(models.Model):

    user_name = models.CharField(max_length=20)
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
