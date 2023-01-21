from django.db import models
from django.utils.timezone import now

#Car Make Model
class CarMake(models.Model):
    name  = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=100)

    def __str__(self) :
        return 'Name: '+self.name+' Description: '+self.description

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
    make=models.ManyToManyField(CarMake)

    def __str__(self):
        return "Model : "+self.name+", "+self.make+","+self.year


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
