from django.db import models
from django.utils.timezone import now
import json

#Car Make Model
class CarMake(models.Model):
    name  = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=100)

    def __str__(self) :
        return self.name

#Car Models Model
class CarModel(models.Model):
    Sedan = 'sedan'
    SUV = 'suv'
    Wagon = 'wagon'
    choices = [(Sedan,'Sedan'),(SUV,'SUV'),(Wagon,'Wagon')]
    name=models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=False)
    type = models.CharField(null=False,choices=choices, max_length=20)
    year=models.DateField()
    make=models.ManyToManyField(CarMake, related_name='Makes')

    def __str__(self):
        return self.name

#Dealer object class
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Name: " + self.full_name


# Dealer review class
class DealerReview():
    def __init__(self, dealership, name, purchase, review,sentiment, car_year, car_make,car_model,purchase_date):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.car_year= car_year
        self.car_model = car_model
        self.car_make = car_make
        self.sentiment=sentiment
        self.purchase_date = purchase_date

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)