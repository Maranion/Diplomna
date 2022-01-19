from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('individual_coin',views.individual_coin, name="individual_coin"),
    path('coins', views.coins, name='coins')
]