from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UpdateUser, RegisterUser
import json
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import string
import random
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from web import forms
# Create your views here.

def index(request):
    form = RegisterUser()
    return render(request, 'flyaway/login.html', {'form': form})



def profile(request, name):
    user = Customer.objects.get(user__username=name)
    form = UpdateUser(instance=user)
    if request.method == "POST":
        
        form = UpdateUser(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            print('update')
        else:
            print('not')
    param = {
        'form': form,
    }
    return render(request, 'flyaway/profile.html', param)



def flights(request):
    flight_from = request.GET['origin']
    flight_to = request.GET['destination']
    travel_date = request.GET['departure']    
    travellers = request.GET['passenger']

    flight_lists = Schedule.objects.filter(where_from__name__icontains=flight_from, where_to__name__icontains=flight_to, fromDate__icontains=travel_date) 
    # if request.GET['arrival']:
    #     return_date = request.GET['arrival']
    #     print('two-way')
    # else:
    #     print('one-way')

    if request.method == "GET":
        flight_from = request.GET['origin']
        flight_to = request.GET['destination']
        travel_date = request.GET['departure']    
        travellers = request.GET['passenger']

        flight_lists = Schedule.objects.filter(where_from__name__icontains=flight_from, where_to__name__icontains=flight_to, fromDate__icontains=travel_date)

    param = {
        'lists': flight_lists,
        'travellers': travellers,
        'flight_from': flight_from,
        'flight_to': flight_to,
        'travel_date': travel_date,
    }
    return render(request, 'flyaway/flights.html', param)

def summary(request, arg, trav):
    lists = Schedule.objects.get(slug=arg)
    total_money = (int(lists.farePrice)*int(trav)) + (int(trav)*200)
    print(total_money)
    param = {
        'list': lists,
        'travellers': trav,
        'flight': arg,
        'total_money': total_money,
        'conv': int(trav)*200,
    }
    return render(request, 'flyaway/summary.html', param)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)


        if user is not None:
            check = Customer.objects.get(user__username=username)
            print(check.verifiedOr)
            if int(check.verifiedOr) == int(1):
                login(request, user)
                # return JsonResponse({'message': message}, safe=False)
                return redirect('index')
            else:
                send_mail('FlyAway',
                    "Your OTP is : " + str(check.otp),
                    settings.EMAIL_HOST_USER,
                    [check.user.email],
                    fail_silently=False)
                return redirect('verify', username)       
                
        else:
            messages.info(request, "Check Credentials")

    return render(request, 'flyaway/logins.html')


def signUp(request): 
    form = RegisterUser()
    temp = ''.join((random.choice(string.digits) for i in range(0,4)))
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        user = request.POST.get('username')
        email = request.POST.get('email')
        if form.is_valid():
            form.save()
            otps = Customer.objects.get(user__username=user)
            otps.otp = temp
            otps.save()
            send_mail('FlyAway',
                "Your OTP is : " + str(temp),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False)
            return redirect('verify', user)    
        else:
            print('not')
    param ={
        'form': form,
    }
    return render(request, 'flyaway/signup.html', param)
            
    


def addPassenger(request):
    transactionId = datetime.datetime.now().timestamp()
    temp = ''.join((random.choice(string.ascii_letters) for i in range(0,5)))
    abc = json.loads(request.body)
    flight = Schedule.objects.get(slug=abc['form'][0]['flight'])
    passengers = len(abc['form'])
    total_money = (int(flight.farePrice)*int(passengers)) + (int(passengers)*200)
    fare = abc['form'][0]['fare']
    
    if int(total_money) == int(fare):
        print('def')
        for i in abc['form']:
            Bookings.objects.create(
                name=request.user,
                flight=i['flight'],
                passengerFName=i['fname'],
                passengerLName=i['lname'],
                pnr=temp.upper()
            )

        RefBooking.objects.create(name=request.user, pnr=temp.upper(), transaction="Confirmed", transactionId=transactionId)

        send_mail('FlyAway',
            "Ticket Confirmed Your PNR number is : "+ str(temp.upper()),
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False)

        return JsonResponse({'message': temp.upper()}, safe=False)

def success(request):
    return render(request, 'flyaway/confirmed.html')
    


def error(request, exception):
    return render(request, 'flyaway/error.html')

def resend(request, arg):
    abc = Customer.objects.get(user__username=arg)
    temp = ''.join((random.choice(string.digits) for i in range(0,4)))
    abc.otp = temp
    abc.save()

    send_mail('FlyAway',
        "Your OTP is : " + str(temp),
        settings.EMAIL_HOST_USER,
        [abc.user.email],
        fail_silently=False)
    return redirect(verify, arg)

@csrf_exempt
def check(request): 
    if request.method =="POST":
        otp = request.POST.get('otp')
        user = request.POST.get('user')
        print(otp)
        abc = Customer.objects.get(user__username=user)
        if str(abc.otp) == str(otp):
            abc.verifiedOr = "1"
            abc.save()
            message = '1'
        else:
            message = '0'
    return JsonResponse({'message': message},safe=False)

def origin(request):
    if 'term' in request.GET:
        name = request.GET.get('term')
        qs = Airport.objects.filter(Q(name__icontains=name) | Q(code__icontains=name) | Q(address__icontains=name))
        lists = list()
        for detail in qs:
            lists.append(detail.name)
        return JsonResponse(lists, safe=False)\


@login_required(login_url='index')
def bookings(request):
    lists = RefBooking.objects.filter(name=request.user)

    return render(request, 'flyaway/Bookings.html', {'lists': lists})



def verify(request, arg):
    user = Customer.objects.get(user__username=arg)
    otp = user.otp

    
    return render(request, 'flyaway/OTP.html', {'user': arg})


@login_required(login_url='index')
def viewTicket(request, pnr):
    lists = Bookings.objects.filter(pnr=pnr)
    number = lists.count()
    newf = lists.first()
    list2 = RefBooking.objects.get(pnr=pnr)
    flight = Schedule.objects.get(slug=newf.flight)
    total= (int(number)* int(flight.farePrice)) + (int(number)*200)

    return render(request, 'flyaway/viewTicket.html', {'lists': lists, 'qr': list2, 'flight': flight, 'total': total,})
    