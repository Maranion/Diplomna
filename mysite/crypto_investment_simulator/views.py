from datetime import date
from locale import currency
from multiprocessing.sharedctypes import Value
import re
import string
from traceback import print_tb
from urllib import response
#from cv2 import redirectError
from django import template
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import csv, os, json
from matplotlib.pyplot import flag
from matplotlib.style import context, use
from requests import Request, Session, request
import pprint
from django.shortcuts import redirect

from .models import Wallets

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from decimal import Decimal




    
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
parameters = {
    'convert': 'USD'
}
headers = {
    'Accepts': 'aplication/json',
    'X-CMC_PRO_API_KEY': 'd41b0196-6e67-4d76-8f93-f0bab44492a7'
}
SESSION = Session()
SESSION.headers.update(headers)


    

#pprint.pprint(json.loads(response.text
MAX_COINS = 100
DOLLARS = 'USD'
DOLLAR_PRICE = 1.0

# --- COINMARKETCAP DATA EXTRACTION ---

def get_labels(num,list,response):

    list.append(json.loads(response.text)['data'][num]['symbol'].lower())
    list.append(json.loads(response.text)['data'][num]['slug'].title())
    list.append(json.loads(response.text)['data'][num]['symbol'])

    return(list)


def get_price(num,list,response):

    value = json.loads(response.text)['data'][num]['quote']['USD']['price']
    if value < 0.1:
        list.append(round(value,8))
        return(list)
    
    list.append(round(value,2))
    return(list)


def get_market_data(num, list,response):

    list.append(round(json.loads(response.text)['data'][num]['quote']['USD']['percent_change_24h'],2))
    list.append(round(json.loads(response.text)['data'][num]['quote']['USD']['market_cap']/1000000000,2))
    
    return(list)


def get_data():
    coin_list =[]
    response = SESSION.get(url,params=parameters)

    for num in range(0,MAX_COINS):

        coin = [num+1]
        
        coin = get_labels(num,coin,response)
        coin = get_price(num,coin,response)
        coin = get_market_data(num,coin,response)

        coin_list.append(coin)

    return coin_list

def get_coin(num):
    response = SESSION.get(url,params=parameters)

    num = int(num)
    coin = [num]
        
    coin = get_labels(num-1,coin,response)
    coin = get_price(num-1,coin,response)
    coin = get_market_data(num-1,coin,response)

    return coin

# ----------------------------------------    


def logout_user(request):

    #logout(request)
    delete_all_wallets()
    return redirect('login')


# LOGIN VIEW -----
def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')

    template = loader.get_template('login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "bad kitty")

    return HttpResponse(template.render())

# REGISTER VIEW -----
def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    template = loader.get_template('register.html')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #user = form.cleaned_data.get('username')
            #print(user)hhh
            messages.success(request, 'acc was .')

            return redirect('login')


    context = {'form' : form }
    return HttpResponse(template.render(context))


# INDEX VIEW -----
@login_required(login_url='login')
def index(request):
    template = loader.get_template('index.html')
    
    if check_user_wallet(request) is None:
        create_user_wallet(request)


    return HttpResponse(template.render())




# ----- buy functionality
def get_wallet(request):

    wallet = Wallets.objects.get(user_name=f'{request.user}')
    return wallet
###

def overlap_check(wallet, coin):
    
    keys = wallet.key
    keys = keys.split()

    value = wallet.value
    value = value.split()

    try:
        i = keys.index(coin)
        return True

    except ValueError:
        return False

###
        #value[i] = Decimal(value[i])+ convert_currency(price, money)
        #new_value = ''
        #for v in value:
        #    new_value = f'{new_value} {v}'
        #wallet.value = new_value
###
def convert_to_coin(price, ammount):
    return ammount / Decimal(price)

def convert_to_num(ammount):
    
    try:
       ammount = Decimal(ammount)
       return ammount

    except ValueError:
        print('Value can\'t cointain letters or spaces')
        return False


###
def list_to_string(list):

    str = ''
    for ele in list:
        str = f'{str} {ele}'

    return str

###
def save_wallet(wallet):
        Wallets.objects.filter(user_name=wallet.user_name).delete()
        wallet.save() 

### ADDING VALUES TO THE WALLET
def add_existing(wallet, coin, price, money):
    keys = (wallet.key).split()
    values = (wallet.value).split()

    i = keys.index(coin)
    values[i] = Decimal(values[i]) + convert_to_coin(price, money)

    keys = list_to_string(keys)
    values = list_to_string(values)

    wallet = Wallets(user_name=wallet.user_name, key = keys, value=values)
    save_wallet(wallet) 


def add_new(wallet, coin, price, money):
    wallet.key = f'{wallet.key} {coin}'
    wallet.value = f'{wallet.value} {convert_to_coin(price, money)}'
    save_wallet(wallet)

### ------------------------------------------------

def buy_coin(request, coin, price, money):
    wallet = get_wallet(request)
    wallet_add(wallet, coin, price, money)


def wallet_add(wallet, coin, price, money):
    print(f'overlap check - {overlap_check(wallet, coin)}')
    if overlap_check(wallet, coin):
        add_existing(wallet, coin, price, money)
    else:
        add_new(wallet, coin, price, money)
    
#    wallet.key = f'{wallet.key} {coin}'
#    money = convert_currency(price, money)
#    wallet.value = f'{wallet.value} {money}'
#    Wallets.objects.filter(user_name=f'{request.user}').delete()
#    wallet.save()

# INDIVIDUAL COIN VIEW ---------------------------------------------------------
@login_required(login_url='login')
def individual_coin(request):

    if request.method == "POST":
        if request.POST.get('buy_btn'):

            ammount = request.POST.get('money_val')
            ammount = convert_to_num(ammount)
            if ammount:
                coin = request.POST.get('hidden_value')
                price = request.POST.get('hidden_value2')
                buy_coin(request, coin, price, ammount)

            else:
                print('wrong format (0.00)')
        elif request.POST.get('sell_btn'):

            ammount = request.POST.get('money_val')
            ammount = convert_to_num(ammount)
            if ammount:
                coin = request.POST.get('hidden_value')
                price = request.POST.get('hidden_value2')
                
                if check_ownership(get_wallet(request), coin):
                    sell_coin(request, coin, price, ammount)
                    wallet_print(request)
                else:
                    print('can\'t sell what you dont have')
                

        wallet_print(request)
    
    template = loader.get_template('individual_coin.html')
    coin = get_coin(SESSION.coin)
    context = {
        'coin' : coin
    }
    return HttpResponse(template.render(context))

# SELLL FUNCTIONALITY -------------------
def sell_coin(request, coin, price, ammount):
    wallet = get_wallet(request)

    if check_ownership(wallet, coin):
        money = convert_to_money(wallet,coin,price,ammount)
        if money:
            wallet = remove_coin(wallet,coin,ammount)
            wallet_add(wallet,DOLLARS,DOLLAR_PRICE,money)
            

###
def remove_coin(wallet,coin,ammount):
    keys = (wallet.key).split()
    values = (wallet.value).split()

    i = (wallet.key).split()
    i = i.index(coin)
    
    values[i] = Decimal(values[i]) - ammount
    if values[i] == 0.0:
        keys.remove(keys[i])
        values.remove(values[i])
 
    values = list_to_string(values)
    keys = list_to_string(keys)
    
    wallet = Wallets(user_name=wallet.user_name, key = keys, value=values)
    save_wallet(wallet) 
    return wallet

###
    
###
def check_ammount(wallet,coin,ammount):
    i = (wallet.key).split()
    i = i.index(coin)
    #ammount if hund
    coins_owned = (wallet.value).split()
    coins_owned = coins_owned[i]
    
    if Decimal(coins_owned) < ammount:
        return False
    else:
        return True

###
def convert_to_money(wallet,coin,price,ammount):
    if check_ammount(wallet,coin,ammount):
        return ammount*Decimal(price)
    else:
        return False
###
def check_ownership(wallet, coin):
    keys = (wallet.key).split()
    try:
        keys.index(coin)
        print('mens')

        return True
    except ValueError:
        print('nis')
        return False

####


# end --------------------------------------------------------------------------
# COINS VIEW -----
@login_required(login_url='login')
def coins(request):
    if request.POST.get('b_s_button'):
        info = request.POST.get('b_s_button')
        SESSION.coin = info
        return redirect('individual_coin')

 
    template = loader.get_template('coins.html')
    coin_list = get_data()
    context = {
        'coin_list' : coin_list
    }

    return HttpResponse(template.render(context))


# < DATABASE WORKINGS > ----------------------------

def check_user_wallet(request):
    user = f'{request.user}'
    wallets = Wallets.objects.all()
    for wallet in wallets:
        #print(f'wal-{wallet.user_name} --- {user}')
        if f'{wallet.user_name}' == user:
            return wallet

    return None

def create_user_wallet(request):
    wallet = Wallets(user_name=request.user,key='',value='')
    wallet.save()
    print(f'CREATED WALLET FOR - {request.user}')

def delete_all_wallets():
    a =Wallets.objects.all()
    for ana in a:
        Wallets.objects.filter(user_name=f'{ana.user_name}').delete()
    print('done? vvv')
    play('nig')

def wallet_print(request):
    wallet = Wallets.objects.get(user_name=f'{request.user}')
    print('vvvvvvvv')
    print(f'{wallet.user_name} - {wallet.key} - {wallet.value}')

# END ---------------------------------------


def play(request):
    user = Wallets.objects.all()
    #k = Wallets(user_name='tete2',key='btv btc',value='123.123 45.45')
    #k.save()

    print(Wallets.objects.all())
    for obj in user:
        #if obj.user_name == 'tete2':
        #   obj.key = f'{obj.key} nig'
        print(f'{obj.user_name} - {obj.key} - {obj.value}')

    #print(request.user)
