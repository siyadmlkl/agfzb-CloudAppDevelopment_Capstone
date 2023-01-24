from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarModel,DealerReview
from .restapis import get_dealers_from_cf, get_dealers_for_id,get_dealers_for_st,get_review
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

#About view
def about(request):
    return render(request, 'djangoapp/about.html')


# Contact us
def contact(request):
    return render(request,'djangoapp/contact.html')

#Login view
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp')
        else:
            return redirect('/djangoapp')
    else:
        return redirect('/djangoapp')

#logout
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('/djangoapp')

#User registration
def registration_request(request):
    if request.method == 'GET':
        return render(request,'djangoapp/registration.html')
    
    elif request.method == 'POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password=request.POST['password']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username,
                                                                        first_name=first_name,
                                                                        last_name=last_name,
                                                                        password=password)
            user.save()
            login(request, user)
            return redirect('/djangoapp')
        else:
            return redirect('/djangoapp')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/dealership-package/get-dealership-async"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html',{"dealerships":dealerships})

#get delaers by state
def get_dealerships_by_st(request, state):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/dealership-package/get-dealership-async"
        # Get dealers from the URL
        dealerships = get_dealers_for_st(url,state)
        return render(request, 'djangoapp/index.html',{"dealerships":dealerships})
       

#Get dealers by id    
def get_dealerships_by_id(request, id):
    if request.method == "GET":
        url = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/dealership-package/get-dealership-async"
        # Get dealers from the URL
        dealerships = get_dealers_for_id(url,id)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html',{"dealerships":dealerships})

#View for reviews
def get_dealer_review(request, dealership):
     if request.method == "GET":
        review=[]
        url = 'https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/review-package/get-reviews'
        review = get_review(url,dealership)
        return render(request, 'djangoapp/review.html', {'review':review})
     
#View for posting review
def post_review(request):
    return render(request, 'djangoapp/postreview.html')

    '''
    review=dict()
    review["time"] = datetime.utcnow().isoformat()
    review["name"]="Kelly"
    review["dealership"] = 11
    review["review"] = "This is a great car dealer"
    review["purchase"]="No"
    json_payload = json.dumps()
    '''


