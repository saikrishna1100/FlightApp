from django.contrib import admin
from django.urls import path
from .views import home, login_user, register, logout_user, dashboard, book_flight, flights, add_flight, delete_flight, view_bookings, add_passenger, user_bookings

urlpatterns = [
    path('', home, name='index'),
    
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    
    path('dashboard/', dashboard, name='home'),
    
    path('flights/', flights, name='flights'),
    path('add_flight', add_flight, name='add_flight'),
    path('view_bookings/<str:pk>/', view_bookings, name='view_bookings'),
    path('delete_flight/<str:pk>/', delete_flight, name='delete_flight'),
    
    path('add_passenger/', add_passenger, name='add_passenger'),
    path('user_bookings/', user_bookings, name='user_bookings'),
    
    path('book_seat/<str:pk>/', book_flight, name='book_flight')
]
