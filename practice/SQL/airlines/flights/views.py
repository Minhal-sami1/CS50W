from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Flight, Passenger
# Create your views here.

def index(request):
    return render(request, "flights/index.html",{
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(id = flight_id)
    passegers = flight.passengers.all()
    non_passenger = Passenger.objects.exclude(flights = flight).all()
    return render(request, "flights/flight.html",{
        "flight": flight,
        "passengers": passegers,
        "non_passengers": non_passenger
    })

def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(id = flight_id)
        passenger_id = int(request.POST['passenger'])
        passenger = Passenger.objects.get(id = passenger_id)
        passenger.flights.add(flight)
        return redirect(reverse('flight', args = (flight_id,)))

    else:
        return redirect(reverse('flight', args = (flight_id,)))
