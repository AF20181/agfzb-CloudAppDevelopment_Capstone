from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
#from .models import related models
#from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from . import restapis
from . import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next'))
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state=None):
    context = {}
    if request.method == "GET":
        state = request.GET.get('state', '')
        if state:
            context = {"dealerships": restapis.get_dealers_from_cf('https://3faef1d1.eu-de.apigw.appdomain.cloud/api/get_dealerships?state={0}'.format(state), state)}
            return render(request, 'djangoapp/index.html', context)
        else:
            context = {"dealerships": restapis.get_dealers_from_cf('https://3faef1d1.eu-de.apigw.appdomain.cloud/api/get_dealerships')}
            return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealerid = dealer_id
        context = {
            "reviews": restapis.get_dealer_reviews_by_id_from_cf('https://3faef1d1.eu-de.apigw.appdomain.cloud/api/get_reviews?dealerId={0}'.format(dealerid), dealerid),
            "dealers": restapis.get_dealers_from_cf('https://3faef1d1.eu-de.apigw.appdomain.cloud/api/get_dealerships?id={0}'.format(dealerid),dealerid),
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    if request.method == "GET":
        dealerid = dealer_id
        # Get dealers from the URL
        context = {
            "cars": models.CarModel.objects.all(),
            "dealers": restapis.get_dealers_from_cf('https://3faef1d1.eu-de.apigw.appdomain.cloud/api/get_dealerships?id={0}'.format(dealerid),dealerid),
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            review = dict()
            form = request.POST
            review["dealership"] = dealer_id
            review["name"] = ''+request.user.first_name + ' ' + request.user.last_name+''
            review["review"] =  form["content"]
            review["purchase"] = bool(False)
            if form.get("checkpurchased") == 'on':
                review["purchase"] = bool(True)
            review["purchase_date"] = datetime.strptime(form.get("purchase_date"), "%d/%m/%Y").isoformat()
            car = models.CarModel.objects.get(pk=form["car"])
            review["car_make"] = car.carmake.name
            review["car_model"] = car.name
            review["car_year"] = int(car.year.strftime("%Y"))
            json_payload = {}
            json_payload["review"] = review
            restapis.post_request('https://3faef1d1.eu-de.apigw.appdomain.cloud/api/review',json_payload,dealerID=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("/djangoapp/login")
