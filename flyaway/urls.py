from django.urls import path
from .import views as assets

urlpatterns = [
    path('', assets.index, name='index'),
    path('login/', assets.login, name='login'),
    path('logout/', assets.logout, name='logout'),
    path('signup/', assets.signup, name='signup'),
    path('verify/<str:user>', assets.verify, name='verify'),
    path('flights/', assets.flights, name='flights'),
    path('myBookings/', assets.bookings, name='bookings'),
    path('preview/<str:departure>/<int:pk>/<str:arrival>/<int:seats>/', assets.preview, name='preview'),
    path('payment/<str:arriv>/<str:arrivfrom>/<str:price>/<str:ftime>/', assets.payment, name='payment'),
    path('success/', assets.success, name='success'),
    path('autosuggest/', assets.autosuggest, name='autosuggest'),
    path('checkout/', assets.checkout, name='checkout'),
    path('fetch/', assets.fetch, name='fetch'),
    path('viewTicket/<str:pnr>', assets.viewTicket, name='viewTicket'),
    path('cancellation/<str:pnr>', assets.cancellation, name='cancellation'),
]