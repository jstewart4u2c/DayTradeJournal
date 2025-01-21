from django.urls import path
from . import views

app_name = 'journal'
urlpatterns = [
    path('', views.home, name='home'),
    path('analysis/', views.analysis, name='analysis'),
    path('calendar/', views.calendar, name='calendar'),
    path('logout/', views.user_logout, name='logout'),

]
