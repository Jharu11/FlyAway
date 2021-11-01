from typing import cast
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
from uuid import uuid4
import os
import string
import random


class Airport(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    ICAO = models.CharField(max_length=50, blank=False, null=False)
    code = models.CharField(max_length=20, blank=False, null=False)
    country = models.CharField(max_length=50, blank=False, null=False)
    address = models.CharField(max_length=50, blank=False, null=False)
    IATA = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name

class Aircraft(models.Model):

    def path_and_rename(instance, filename):
        upload_to = 'aircraft/image'
        name = filename.split('.')[-1]
        filename = '{}.{}.{}'.format(uuid4().hex,instance.company,name)

        return os.path.join(upload_to, filename)

    company = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to=path_and_rename)
    seats = models.IntegerField(blank=False, null=False)
    number = models.CharField(max_length=50, blank=False, null=False)
    model = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.company

class Customer(models.Model):

    def rename_file(instance, filename):
        upload_to="customer/image"
        name = filename.split('.')[-1]
        filename = '{}.{}.{}'.format(uuid4().hex,instance.fname,name)

        return os.path.join(upload_to, filename)

    status = [
        ('0', '0'),
        ('1', '1'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=50, blank=True)
    lname = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=rename_file, blank=True)
    dob = models.CharField(max_length=50, blank=True)
    phone = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True)
    verifiedOr = models.CharField(max_length=20, blank=False, choices=status, default="0")
    otp = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.user.username

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        

class Schedule(models.Model):
    fType = [
        ('Partially Refundable', 'Partially Refundable'),
        ('Refundable', 'Refundable')
    ]
    ScheduleId = models.AutoField(primary_key=True)
    details = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    where_from = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='where_from')
    where_to = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='where_to')
    fromDate = models.DateField()
    toDate = models.DateField()
    fromTime = models.TimeField()
    toTime = models.TimeField()
    fareType = models.CharField(choices=fType, default=None, blank=False, max_length=50)
    farePrice = models.IntegerField(blank=False)
    totalSeats = models.IntegerField(default=180)
    slug = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.where_from.name

@receiver(pre_save,sender=Schedule)
def create_scheduleSlug(instance, sender, **kwargs):
    a = str(instance.ScheduleId)
    b = str(instance.details.company)
    c = str(instance.where_from.code)
    instance.slug = slugify(a+b+c)

class Bookings(models.Model):
    
    title = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms')
    ]
    stat = [
        ('0', '0'),
        ('1', '1'),
    ]
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.CharField(max_length=255, blank=False, null=False)
    passengerFName = models.CharField(max_length=50, blank=False, null=False)
    passengerLName = models.CharField(max_length=50, blank=False, null=False)
    passengerSeatNO = models.CharField(max_length=50, blank=True, null=True)    
    cancellation = models.CharField(max_length=20, blank=False, choices=stat, default="0")
    pnr = models.CharField(max_length=50,blank=True, null=True)
    dateCreated = models.DateTimeField(blank=False, auto_now_add=True)

    def __str__(self):
        return self.passengerFName

class RefBooking(models.Model):
    defaultValue = "Not"
    status = [
        ('Cancelled', 'Cancelled'),
        ('Not', 'Not'),
        ('Confirmed', 'Confirmed')
    ]
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    pnr = models.CharField(max_length=50,blank=False, null=False)
    transaction = models.CharField(max_length=20, choices=status, default=defaultValue, null=False, blank=False)
    transactionId = models.CharField(max_length=20, null=False, blank=False)
    dateCreated = models.DateTimeField(blank=False, auto_now_add=True)
