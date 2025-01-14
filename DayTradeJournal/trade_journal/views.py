from django.shortcuts import render


# Create your views here.
def home(request):
    hello = 'Hello World!'

    return render(request, 'journal/home.html',  {'hello': hello})