from django.contrib import admin
# from .models import Booking, Flight
from .models import Flight, Passenger, Place, Ticket, Week

# # Register your models here.
# admin.site.register(Flight)
# admin.site.register(Booking)

admin.site.register(Flight)
admin.site.register(Passenger)
admin.site.register(Place)
admin.site.register(Ticket)
admin.site.register(Week)