
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Finch

# from django.http import HttpResponse

# #Define home view
# def home(request):
#     return HttpResponse('<h1>Yo. It works.</h1>')

from django.shortcuts import render

def home(request):
    '''
    this is where we return a response
    in most cases we  would render a template
    and we'll need some data for that template
    '''
    # return HttpResponse('<h1> Hello World </h1>')
    return render(request, 'home.html')

# Create your views here.

def about(request):
    return render(request, 'about.html')


# Add the Cat class & list and view function below the imports
# class Finch:  # Note that parens are optional if not inheriting from another class
#   def __init__(self, name, type, description, age):
#     self.name = name
#     self.type = type
#     self.description = description
#     self.age = age

# finches = [
#   Finch('Tuna', 'Blue Finch', 'It is, in fact, blue', 3),
#   Finch('Loud', 'Saffron Finch', 'Not made from actual Saffron', 1),
#   Finch('Raven', 'Strawberry Finch', 'Not a raven, nor made of strawberrys, but is red!', 4)
# ]


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches' : finches})    

def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', { 'finch' : finch })

# the CUDs in CRUD. __all__ replaces ['name', 'breed', 'description', 'age'] 
class FinchCreate(CreateView):
    model = Finch
    fields = '__all__'
    # success_url = '/finches/'

class FinchUpdate(UpdateView):
    model = Finch
    fields = ['type', 'description', 'age']

class FinchDelete(DeleteView):
    model = Finch
    success_url = '/finches/'        