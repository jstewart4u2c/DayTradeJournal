from django.urls import path
from . import views

app_name = 'trade_journal'
urlpatterns = [
    path('', views.home, name='home'),

]