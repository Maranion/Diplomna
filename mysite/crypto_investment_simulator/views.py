from datetime import date
from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import csv, os, json
from requests import Request, Session
import pprint

url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
parameters = {
    'convert': 'USD'
}
headers = {
    'Accepts': 'aplication/json',
    'X-CMC_PRO_API_KEY': 'd41b0196-6e67-4d76-8f93-f0bab44492a7'
}
session = Session()
session.headers.update(headers)

response = session.get(url,params=parameters)
#pprint.pprint(json.loads(response.text
MAX_COINS = 100



# --- COINMARKETCAP DATA EXTRACTION ---

def get_labels(num,list):

    list.append(json.loads(response.text)['data'][num]['symbol'].lower())
    list.append(json.loads(response.text)['data'][num]['slug'].title())
    list.append(json.loads(response.text)['data'][num]['symbol'])

    return(list)


def get_price(num,list):

    value = json.loads(response.text)['data'][num]['quote']['USD']['price']
    if value < 0.1:
        list.append(round(value,8))
        return(list)
    
    list.append(round(value,2))
    return(list)


def get_market_data(num, list):

    list.append(round(json.loads(response.text)['data'][num]['quote']['USD']['percent_change_24h'],2))
    list.append(round(json.loads(response.text)['data'][num]['quote']['USD']['market_cap']/1000000000,2))
    
    return(list)


def get_data():
    coin_list =[]

    for num in range(0,MAX_COINS):

        coin = [num+1]
        
        coin = get_labels(num,coin)
        coin = get_price(num,coin)
        coin = get_market_data(num,coin)

        coin_list.append(coin)

    return coin_list

# ----------------------------------------    

coins_list = ['test.csv']


def convert_data(value):
    fixed_value = []
    for x in value:
        x = float(x)
        fixed_value.append(x)

    return fixed_value

def rm_hours(target):
    outcome = []
    for x in target:
        x = x.replace(" 04:00:00", "")
        x = x.replace("-","/")
        outcome.append(x)


    return outcome

def yearly_data(csv_reader):
    x = 0
    rows = []
    for row in csv_reader:
        if x%10 == 0 and x <= 365:
            rows.append(row)
        x += 1
    
    return rows

def monthly_data(csv_reader):
    x = 0
    rows = []
    for row in csv_reader:
        if x >= 31:
            break

        rows.append(row)
        x += 1
    
    return rows

def all_data(csv_reader):
    rows = []
    x = 0
    for row in csv_reader:
        if x%10 == 0:
            rows.append(row)
        x += 1

    return rows

def get_from_csv(path, type):
    csv_file = open(path)
    csv_reader = csv.reader(csv_file)

    header = next(csv_reader)
    
    if type == '1y':
        rows = yearly_data(csv_reader)

    elif type == '1m':
        rows = monthly_data(csv_reader)

    elif type == 'all':
        rows = all_data(csv_reader)
    
    csv_file.close()
    
    return rows

def extract_csv_data(path,type):
    data = get_from_csv(path,type)

    date = [row[0] for row in data]
    value = [row[1] for row in data]
    date = rm_hours(date)
    value = convert_data(value)

    return date, value


def index(request):
    template = loader.get_template('index.html')
    get_data()
    return HttpResponse(template.render())


def individual_coin(request):
    template = loader.get_template('individual_coin.html')

    for coin in coins_list:
        data = extract_csv_data(f'{os.getcwd()}\\{coin}','1m')

    label = data[0]
    label.reverse()
    
    value = data[1]
    value.reverse()
    context = {
        'label' : label,
        'value' : value,
    }

    return HttpResponse(template.render(context))

def coins(request):
    template = loader.get_template('coins.html')
    coin_list = get_data()
    context = {
        'coin_list' : coin_list
    }

    return HttpResponse(template.render(context))