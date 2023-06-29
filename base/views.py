from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.models import Group, User
from .models import Flight
from .forms import FlightForm, AddFlight, BookTicket, AddPassenger
from django.db.models import Q
from .models import Ticket
from .decorators import allowed_user
from datetime import datetime, timedelta, date
import uuid


def home(request):
    return render(request, 'base/index.html')

def login_user(request):
    form = AuthenticationForm()
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
    
    return render(request, 'base/login.html', {'form' : form})

def register(request):
    form =  UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.username = form.username.lower()
            form.save()
            
            user = User.objects.get(username=form.username)
            user_group = Group.objects.get(name='user')
            
            user.groups.add(user_group)
            
            user.save()
            
            messages.success(request, 'Registered Successfully! Login here.')
            return redirect('login')
        else:
            messages.error(
                request, 'Please fill the deatils correctly.')
    
    return render(request, 'base/register.html', {'form' : form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def dashboard(request):
    form = FlightForm()
    return render(request, 'base/home.html', {'form': form})

@login_required(login_url='login')
@allowed_user(roles=['user'])
def add_passenger(request):
    form = AddPassenger()
    
    if request.method == 'POST':
        form = AddPassenger(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Passenger added successfully!')
            return redirect('home')
    
    return render(request, 'base/add_passenger.html', {'form': form})

@login_required(login_url='login')
@allowed_user(roles=['user'])
def book_flight(request, pk):
    form = BookTicket()
    
    if request.method == 'POST':
        passengers = request.POST.get('passengers')
        
        flight = Flight.objects.get(id=pk)
        req_seats = len(passengers)
        if flight.seats >= req_seats:
            ticket = Ticket()
            ticket.flight = flight
            ticket.user = request.user
            ticket.ref_no = str(uuid.uuid4())[:6]
            ticket.flight_fare = flight.fare * req_seats
            ticket.booking_date = datetime.now()
            ticket.status = 'CONFIRMED'
            ticket.save()
            
            ticket.passengers.set(passengers)
            ticket.save()
            
            flight.seats -= req_seats
            flight.save()
            
            messages.success(request, f'{req_seats} Tickets booked successfully!')
            return redirect('home')
        else:
            messages.error(request, f'Sorry! {req_seats} seats are avilable')    
    return render(request, 'base/book_ticket.html', {'form': form, 'id': pk})

@login_required(login_url='login')
def user_bookings(request):
    tickets = Ticket.objects.filter(user=request.user)
    print(tickets)
    return render(request, 'base/bookings.html', {'tickets': tickets})

@login_required(login_url='login')
def flights(request):
    
    flights = None
    
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        departure_time = request.POST.get('departure_time')
        
        if departure_time is not '':
            departure_time = datetime.strptime(departure_time, '%H:%M:%S').time()
        
        flights = Flight.objects.filter(
            origin=origin,
            destination=destination
        )

        if departure_time:
            flights = flights = flights.filter(
            Q(departure_day__number__gt=date.today().weekday()) |
            (Q(departure_day__number=date.today().weekday()) & Q(departure_time__gt=departure_time)))
        else:
            flights = flights = flights.filter(
            Q(departure_day__number__gt=date.today().weekday()) 
    )
    else:
        flights = Flight.objects.all()
    
    return render(request, 'base/flights.html', { 'flights' : flights })

# ////////////////////////////// Admin Views /////////////////////////////////////////

@login_required(login_url='login')
@allowed_user(roles=['admin'])
def add_flight(request):
    form = AddFlight()
    
    if request.method == 'POST':
        form = AddFlight(data=request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Flight added successfully!')
            return redirect('flights')
    
    return render(request, 'base/add_flight.html', {'form': form})


@login_required(login_url='login')
@allowed_user(roles=['admin'])
def view_bookings(request, pk):
    tickets = Ticket.objects.filter(flight__id=pk)
    return render(request, 'base/view_bookings.html', { 'tickets': tickets })


@login_required(login_url='login')
@allowed_user(roles=['admin'])
def delete_flight(request, pk):
    flight = Flight.objects.get(id=pk)
    flight.delete()
    return redirect('flights')