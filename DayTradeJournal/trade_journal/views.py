from django.shortcuts import render


# Create your views here.
def home(request):
    hello = 'Hello World!'
    context = {
        'hello': hello
    }
    return render(request, 'journal/base.html', context)