from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50, default='Porsche')
    description = models.CharField(null=False, max_length=400, default='Porsche is the best.')

    def __str__(self):
        return 'Name: ' + self.name + ' \nDescription: ' + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SPORT = 'sport'
    SUV = 'suv'
    OTHERS = 'others'
    CAR_CHOICES = [(SPORT, "Sport"), (SUV, 'SUV'), (OTHERS, 'Others')]
    carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Porsche')
    dealerid = models.IntegerField(null=True)
    cartype = models.CharField(null=False, max_length=20, choices= CAR_CHOICES, default=SPORT)
    year = models.DateField(null=True, default=now)

    def __str__(self):
        return 'Name ' + self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, id, short_name, full_name, address, city, zip, st, lat, lng, state):
        # Dealer id
        self.id = id
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer zip
        self.zip = zip
        # Dealer state
        self.state = state
        # Dealr short state
        self.st = st
        # Location lat
        self.lat = lat
        # Location lng
        self.lng = lng
        self.idx = 0

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review
