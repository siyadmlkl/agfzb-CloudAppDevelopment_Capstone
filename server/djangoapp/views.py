from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarModel,DealerReview
from .restapis import get_dealers_from_cf, get_dealers_for_id,get_dealers_for_st,get_reviews,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

#url for dealership
urld = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/dealership-package/get-dealership-async"

#url for get review
urlr = 'https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/review-package/get-reviews'

#url for post review
urlp = "https://au-syd.functions.appdomain.cloud/api/v1/web/cc316789-97d4-4c05-8fa7-ffb7de77acbd/review-package/post-review"

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
       # Get dealers from the URL
        dealerships = get_dealers_from_cf(urld)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html',{"dealerships":dealerships})

#get delaers by state
def get_dealerships_by_st(request, state):
    if request.method == "GET":
       # Get dealers from the URL
        dealerships = get_dealers_for_st(urld,state)
        return render(request, 'djangoapp/index.html',{"dealerships":dealerships})
       

#Get dealers by id    
def get_dealerships_by_id(request, id):
    if request.method == "GET":
      # Get dealers from the URL
        dealerships = get_dealers_for_id(urld,id)
        models=CarModel.objects.all().values()
        return render(request, 'djangoapp/postreview.html',{"dealerships":dealerships,"models":models,"id":id})

#View for reviews
def get_dealer_reviews_from_cf(request, dealership):
     if request.method == "GET":
        review=[]
        review = get_reviews(urlr,dealership)
        return render(request, 'djangoapp/review.html', {'review':review})


def get_review(request,dealer):
    dealership_name = ''
    reviews = get_reviews(urlr,dealer)
    id=dealer
    dealership_name = get_dealers_for_id(urld,dealer)[0].full_name
 
    return render(request, 'djangoapp/dealer_details.html',{'reviews':reviews,
                                                                                                'dealership_name':dealership_name,
                                                                                                'id':id})


#View for posting review
def add_review(request,dealership):
    dealership_name = get_dealers_for_id(urld,dealership)[0].full_name
   
    models = CarModel.objects.all().values()
    id=dealership

    if request.method=='POST':
        json_review={}
        dealership= id
        purchase_date = request.POST['purchase_date']
       
        car_model= request.POST['car_model']
        car_make="Ford"
        car_year=CarModel.objects.filter(name=car_model).values()
        print(car_year)
        if request.POST['purchase']:
            purchase= "Yes"
        else:
            purchase= "No"
        review_= request.POST['review']
        name = dealership_name
        #name=request.user.username
        review = DealerReview(dealership=dealership,name=name,purchase=purchase,car_make=car_make,\
                                review=review_, purchase_date=purchase_date,car_year='2020',car_model=car_model,sentiment='na')
        json_= review.__dict__
        json_review['review']=json_
        r = post_request(urlp,json_review)

        reviews = get_reviews(urlr,dealership)
        dealership_name = get_dealers_for_id(urld,dealership)[0].full_name
        return render(request, 'djangoapp/dealer_details.html',{'reviews':reviews,
                                                                                                    'dealership_name':dealership_name,
                                                                                                    'id':dealership})
            
        
    
    return render(request, 'djangoapp/add_review.html',{'dealership_name':dealership_name,
                                                                                                    'models':models,'id':dealership})


