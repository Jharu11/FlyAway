from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class flightDetail(models.Model):
    name = models.CharField(max_length=50, blank=False)
    company = models.CharField(max_length=50, blank=False)
    model = models.CharField(max_length=50, blank=False)
    number = models.CharField(max_length=50, blank=False)
    logo = models.ImageField(upload_to='company_logo/')

    def __str__(self):
        return self.name

class Airports(models.Model):
    name = models.CharField(max_length=50, blank=False)
    ICAO = models.CharField(max_length=50, blank=False)
    IATA = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=50, blank=False)
    code = models.IntegerField(blank=False)

    def __str__(self):
        return self.name

class AirportsNext(models.Model):
    name = models.CharField(max_length=50, blank=False)
    ICAO = models.CharField(max_length=50, blank=False)
    IATA = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=50, blank=False)
    code = models.IntegerField(blank=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    status = [
        ('0', '0'),
        ('1', '1'),
    ]
    name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=50, blank=False)
    gender = models.CharField(max_length=50)
    phone = models.IntegerField()
    country = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    code = models.IntegerField()
    verifiedOr = models.CharField(max_length=20, blank=False, choices=status, default="0")
    otp = models.IntegerField()

    def __str__(self):
        return self.name

class Schedule(models.Model):
    fType = [
        ('Partially Refundable', 'Partially Refundable'),
        ('Refundable', 'Refundable')
    ]
    ScheduleId = models.AutoField(primary_key=True)
    details = models.ForeignKey(flightDetail, on_delete=models.CASCADE)
    departure = models.ForeignKey(Airports, on_delete=models.CASCADE)
    arrival = models.ForeignKey(AirportsNext, on_delete=models.CASCADE)
    fromDate = models.DateField()
    toDate = models.DateField()
    fromTime = models.TimeField()
    toTime = models.TimeField()
    fareType = models.CharField(choices=fType, default=None, blank=False, max_length=50)
    farePrice = models.IntegerField(blank=False)
    totalSeats = models.IntegerField(default=180)

    def __str__(self):
        return self.departure.name

class Bookings(models.Model):
    defaultValue = "Not-Confirmed"
    status = [
        ('Cancelled', 'Cancelled'),
        ('Not-Confirmed', 'Not-Confirmed'),
        ('Confirmed', 'Confirmed')
    ]
    title = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Others', 'Others')
    ]
    stat = [
        ('0', '0'),
        ('1', '1'),
    ]
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    flightnumber = models.CharField(max_length=50, blank=False, null=False)
    passengerName = models.CharField(max_length=50, blank=False, null=False)
    passengerGender = models.CharField(choices=title, max_length=50, blank=False, null=False)
    passengerPhone = models.IntegerField(blank=False, null=False)
    passengerEmail = models.CharField(max_length=50, blank=False, null=False)
    passengerSeatNO = models.CharField(max_length=50, blank=True, null=True)
    flight_time = models.CharField(max_length=50, blank=True, null=True)
    flight_date = models.CharField(max_length=50, blank=True, null=True)
    flight_from = models.CharField(max_length=50, blank=True, null=True)
    flight_to = models.CharField(max_length=50, blank=True, null=True)
    transaction = models.CharField(max_length=20, choices=status, default=defaultValue, null=False, blank=False)
    cancellation = models.CharField(max_length=20, blank=False, choices=stat, default="0")
    pnr = models.CharField(max_length=50,blank=True, null=True)
    dateCreated = models.DateTimeField(blank=False, auto_now_add=True)

    def __str__(self):
        return self.passengerName



class refrenceBooking(models.Model):
    transaction_id = models.CharField(max_length=50,blank=False, null=False)
    flight_time = models.CharField(max_length=50, blank=True, null=True)
    flight_from = models.CharField(max_length=50,blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    price = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.transaction_id