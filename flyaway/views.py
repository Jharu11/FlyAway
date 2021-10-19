from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.forms import inlineformset_factory
from django import forms
from .forms import CreateUserForm
from django.contrib import messages
from django.http import Http404, JsonResponse
import json
import datetime
from django.conf import settings
from django.core.mail import send_mail
import random
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

def index(request):
    return render(request, 'flyaway/index.html')

def fetch(request):
    return JsonResponse()

def viewTicket(request, pnr):
    qr = Bookings.objects.filter(pnr=pnr).order_by('id')[:1]
    query = Bookings.objects.filter(pnr=pnr,name=request.user,cancellation=0)
    query2 = query.count()
    price = refrenceBooking.objects.get(transaction_id=pnr)
    context = {
        'query': query,
        'query2': query2,
        'qr': qr,
        'price': price.price,
        'pnr': pnr,
    }
    return render(request, 'flyaway/viewTicket.html', context)

def logout(request):
    user_logout(request)
    return redirect('index')    
    return render(request, 'flyaway/index.html')

def bookings(request):
    datas = Bookings.objects.filter(name=request.user)
    context = {
        'datas': datas,
    }
    return render(request, 'flyaway/mybookings.html', context)

def cancellation(request, pnr):
    if request.method == "POST":
        email = request.user.email
        query = Bookings.objects.filter(id=pnr, name=request.user)

        for query in query:
            query.cancellation = "1"
            query.transaction = "Cancelled"
            query.save()
            print('done')
            send_mail('FlyAway',
            'You have cancelled 1 Ticket. You will get refundable some amount after few working days',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False)

            return redirect('/myBookings/')

            


    context = {
        
    }
    return render(request, 'flyaway/cancellation.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            check = Customer.objects.get(name=username)

            if check.verifiedOr == '1':
                if user is not None:
                    user_login(request, user)
                    return redirect('index')

                else:
                    messages.info(request,'Check Username or Password')
            else:
                otp = str(random.randint(1000,9999))
                
                check.otp = otp
                email = check.email
                check.save()

                send_mail('FlyAway',
                    'Your OTP for verification is ' + str(otp),
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False)
                
                return redirect(verify, "sahgc2a4asashvjfvsc"+username+"hdvfhgvshjh")
                messages.info(request,'Please Verify the User')
        else:
                messages.info(request,'Check Username or Password')

    return render(request, 'flyaway/login.html')

def signup(request):
    form = CreateUserForm()
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully. Check Your Email For Verification.')

            otp = str(random.randint(1000,9999))

            Customer.objects.create(name=username, otp=otp, phone="000000", code="00000", email=email)
            

            send_mail('FlyAway',
            'Your OTP for verification is ' + str(otp),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False)

            return redirect(verify, "sahgc2a4asashvjfvsc"+username+"hdvfhgvshjh")

    context = {'form': form}
    return render(request, 'flyaway/signup.html', context)

def verify(request, user):
    if request.method == "POST":
        b = request.POST.get('otp')
        print(b)
        username = user.replace("sahgc2a4asashvjfvsc","")
        again = username.replace("hdvfhgvshjh","")
        print(again)

        original = Customer.objects.get(name=again)
        a = original.otp
        print(a)

        if int(a) == int(b):
            print("done")
            original.verifiedOr = "1"
            original.save()
            return redirect('login')
        else:
            messages.info(request, "OTP is wrong")

    context = {

    }
    return render(request, 'flyaway/verification.html', context)

def autosuggest(request):
        print(request.GET)
        query_org = request.GET.get('term')
        query = Airports.objects.filter(name__icontains=query_org)
        mylist = []
        mylist += [x.name for x in query]
        return JsonResponse(mylist, safe=False)

def flights(request):
    current = request.user
    trip_from = request.GET['takeoff']
    trip_to = request.GET['landing']
    trip_departure = request.GET['departure']
    travellers = request.GET['passengers']
    details = Schedule.objects.filter(departure__name__icontains=trip_from, arrival__name__icontains=trip_to, fromDate__icontains=trip_departure)
    
    context = {
        'details' : details,
        'trip_from' : trip_from,
        'trip_to' : trip_to,
        'trip_departure' : trip_departure,
        'travellers' : travellers,
        'current' : current,
    }
    return render(request, 'flyaway/flights.html', context)

def preview(request, departure, pk, arrival, seats):
    currentUser = request.user
    details = Schedule.objects.get(ScheduleId=pk)
    prim = details.details.number
    seatcheck = Bookings.objects.filter(flightnumber=prim, flight_time=details.fromTime)
    print(seatcheck.count())
    passengers = seats
    totalfair = passengers*details.farePrice
    multiForm = inlineformset_factory(User, Bookings, fields=['name','flightnumber','passengerName', 'passengerGender', 'passengerPhone', 'passengerEmail', 'passengerSeatNO', 'flight_time', 'flight_date', 'flight_from', 'flight_to'], extra=passengers, widgets={
        'passengerGender': forms.Select(attrs={'class': 'form-control','required': 'required'}),
        'passengerName': forms.TextInput(attrs={'class': 'form-control','required': 'required'}),
        'passengerPhone': forms.TextInput(attrs={'class': 'form-control','required': 'required'}),
        'passengerEmail': forms.TextInput(attrs={'class': 'form-control','required': 'required'}),
        'passengerSeatNO': forms.TextInput(attrs={'class': 'form-control seatNumber', 'readonly': 'readonly'}),
        'flightnumber': forms.TextInput(attrs={'value': prim, 'readonly': 'readonly','class': 'form-control'}), 
        'flight_time': forms.TextInput(attrs={'value': details.fromTime, 'readonly': 'readonly','class': 'form-control'}),
        'flight_date': forms.TextInput(attrs={'value': details.fromDate, 'readonly': 'readonly','class': 'form-control'}),
        'flight_from': forms.TextInput(attrs={'value': details.departure, 'readonly': 'readonly','class': 'form-control'}),
        'flight_to': forms.TextInput(attrs={'value': details.arrival, 'readonly': 'readonly','class': 'form-control'}),
        'name': forms.TextInput(attrs={'value': currentUser, 'readonly': 'readonly','class': 'form-control'}),
        })
                
    formset = multiForm(instance=currentUser, queryset=Bookings.objects.none())
    if request.method == "POST":
        print(request.POST)
        formset = multiForm(request.POST, instance=currentUser)
        print(formset)
        if formset.is_valid():
            print('successfully data stored')
            formset.save()
            return redirect(payment,prim+"sdc641dsfhfadqhdqw57wffwjgqsdguf346", details.departure, "asd68042wq05100wd8wqdi"+str(totalfair)+"999qwvghvff354641644",str( details.fromTime))
        else:
            print('not valid')
    context = {
        'details': details,
        'passengers' : passengers,
        'totalfair' : totalfair,
        'formset' : formset,
        'currentUser': currentUser,
        'time': details.fromTime,
        'from': details.departure,
        'seatcheck': seatcheck,
    }
    return render(request, 'flyaway/preview.html', context)

def success(request):
    context = {}
    return render(request, 'flyaway/success.html', context)

def payment(request, arriv, arrivfrom, price, ftime):
    c = arriv.replace('sdc641dsfhfadqhdqw57wffwjgqsdguf346','')
    a = price.replace('asd68042wq05100wd8wqdi','')
    b = a.replace('999qwvghvff354641644','')
    print(b)
    context = {
        'c' : c,
        'time': ftime,
        'from': arrivfrom,
        'totalfair': b,
    }
    return render(request, 'flyaway/payment.html', context)

def checkout(request):
    transactionId = datetime.datetime.now().timestamp()
    to = request.user.email
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        fdate = data['form']['time']
        ffrom = data['form']['from']
        tprice = data['form']['price']

        refrenceBooking.objects.create(transaction_id=transactionId,flight_time=fdate,flight_from=ffrom,name=customer,price=tprice)

        datas = Bookings.objects.filter(flightnumber=ffrom,flight_time=fdate)

        for datas in datas:
            datas.transaction = "Confirmed"
            datas.pnr = transactionId
            datas.save()

        send_mail('FlyAway',
            'Ticket Confirmed Your PNR number is : '+ str(transactionId),
            settings.EMAIL_HOST_USER,
            [to],
            fail_silently=False)
    print('Data:', request.body)
    return JsonResponse('payment done', safe=False)