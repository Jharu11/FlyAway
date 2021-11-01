from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Aircraft)
admin.site.register(Airport)
admin.site.register(Customer)
admin.site.register(Bookings)
admin.site.register(Schedule)
admin.site.register(RefBooking)