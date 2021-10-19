from django.contrib import admin
from .models import *

# Register your models here.

class FlightAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'model', 'number')

admin.site.register(flightDetail, FlightAdmin)

class AirportAdmin(admin.ModelAdmin):
    list_display = ('ICAO', 'IATA', 'city', 'country')

admin.site.register(Airports, AirportAdmin)
admin.site.register(AirportsNext)
admin.site.register(Customer)
admin.site.register(refrenceBooking)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('departure', 'arrival', 'fromDate', 'fromTime')

admin.site.register(Schedule, ScheduleAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('flightnumber','name','passengerName', 'passengerGender', 'passengerSeatNO')

admin.site.register(Bookings, BookingAdmin)


class FlightAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'model', 'number')