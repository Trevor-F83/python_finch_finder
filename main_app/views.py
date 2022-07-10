
from distutils.log import error
from multiprocessing import context
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

from .models import Finch, Toy, Photo
from .forms import FeedingForm

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'finchfindertrevor1'
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



@login_required
def finches_index(request):
    finches = Finch.objects.filter(user=request.user)
    return render(request, 'finches/index.html', {'finches': finches})    

@login_required
def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    # instnatiate FeedingForm to be rendered in template
    toys_finch_doesnt_have = Toy.objects.exclude(id__in = finch.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'finches/detail.html', { 
        #include finch and feeding_form 
        'finch': finch, 'feeding_form': feeding_form,
        'toys': toys_finch_doesnt_have
    })

@login_required
def add_feeding(request, finch_id):
  # create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the finch_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.finch_id = finch_id
    new_feeding.save()
  return redirect('detail', finch_id=finch_id) 

@login_required 
def assoc_toy(request, finch_id, toy_id):
  # Note that you can pass a toy's id instead of the whole object
  Finch.objects.get(id=finch_id).toys.add(toy_id)
  return redirect('detail', finch_id=finch_id)

@login_required
def assoc_toy_delete(request, finch_id, toy_id):
  Finch.objects.get(id=finch_id).toys.remove(toy_id)
  return redirect('detail', finch_id=finch_id) 

@login_required
def add_photo(request, finch_id):
    #collect photo file data
    photo_file = request.FILES.get('photo-file', None)
    #conditional logid determines if file is present
    if photo_file:
    #if present, create reference to the boto3 collection
        s3 = boto3.client('s3')
        #create unique id for each photo
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        #upload pfoto file to aws s3
        try: 
        #if successful
            s3.upload_fileobj(photo_file, BUCKET, key)
        #take exchange url & save it to database
            url = f"{S3_BASE_URL}{BUCKET}/{key}"        
            #1) create photo instance with photo model & provide finch_id as foreign key value
            photo = Photo(url=url, finch_id=finch_id)
            #2) save photo instance to database
            photo.save()
        except Exception as error:
            print("Error uploading photo: ", error)
                 #print error messsage
            return redirect('detail', finch_id=finch_id)
    #redirect user to origin page
    return redirect('detail', finch_id=finch_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid info'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# the CUDs in CRUD. __all__ replaces ['name', 'breed', 'description', 'age'] 
class FinchCreate(LoginRequiredMixin, CreateView):
    model = Finch
    fields = '__all__'
    # success_url = '/finches/'

class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['name', 'type', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch
    success_url = '/finches/'   

class ToyList(LoginRequiredMixin, ListView):
  model = Toy
  template_name = 'toys/index.html'

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy
  template_name = 'toys/detail.html'

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'color']


class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']


class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'     