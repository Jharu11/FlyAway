from django.urls import path
from . import views as assets
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', assets.index, name="index"),
    path('flight/', assets.flights, name="flights"),
    path('flight-details/<str:arg>/<str:trav>/', assets.summary, name="summary"),
    path('Myprofile/<str:name>/', assets.profile, name="profile"),
    path('login/', assets.loginUser, name="loginUser"),
    path('register/', assets.signUp, name="signUp"),
    path('enter-user/', assets.addPassenger, name="addPassenger"),
    path('success/', assets.success, name="success"),
    path('origin/', assets.origin, name="origin"),
    path('verify/<str:arg>', assets.verify, name="verify"),
    path('check/', assets.check, name="check"),
    path('resend/<str:arg>/', assets.resend, name="resend"),
    path('bookings/', assets.bookings, name="bookings"),
    path('viewTicket/<str:pnr>/', assets.viewTicket, name="viewTicket"),
    path('error/', assets.error, name="error"),


    # password reset

    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'), 
    path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('reset-password/complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]
