from django import forms
from .models import Flight, Ticket, Passenger

class FlightForm(forms.ModelForm):
    departure_time = forms.TimeField(
        label='Departure Time',
        required=False
    )
 
    class Meta:
        model = Flight
        fields = ['origin', 'destination', 'departure_time']

class AddFlight(forms.ModelForm):
    class Meta:
        model = Flight
        fields = '__all__'
        
class BookTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['passengers']

class AddPassenger(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = '__all__'