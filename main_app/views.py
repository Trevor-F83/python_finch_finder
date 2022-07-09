
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Finch
from .forms import FeedingForm

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
    # instnatiate FeedingForm to be rendered in template
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', { 
        #include finch and feeding_form 
        'finch': finch, 'feeding_form': feeding_form
    })

def add_feeding(request, finch_id):
  # create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id)  

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