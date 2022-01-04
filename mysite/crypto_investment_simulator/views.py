from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import one_day_value
import csv, pandas as pd, os


coins_list = ['gemini_BTCUSD_day.csv', 'gemini_LTCUSD_day.csv']

def open_csv(path):
    csv_file = pd.read_csv(path)
    csv_file['Unix Timestamp'] = pd.to_datetime(csv_file['Unix Timestamp'], unit = 'ms')
    print(csv_file)

def index(request):
    template = loader.get_template('index.html')
    for coin in coins_list:
        open_csv(f'{os.getcwd()}\\{coin}')

    return HttpResponse(template.render())