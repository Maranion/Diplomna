from django.db import models


class one_day_value(models.Model):
    date = models.DateTimeField('date of change')
    close_value = models.FloatField()
    symbol = models.CharField(max_length=12)
