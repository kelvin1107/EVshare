from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('search/', views.search_chargers, name='search_chargers'),
    path('charger/<int:pk>/', views.charger_detail, name='charger_detail'),
    path('add/', views.add_charger, name='add_charger'),
    path('charger/<int:pk>/delete/', views.delete_charger, name='delete_charger'),

    path('bookings/mine/', views.my_bookings, name='my_bookings'),
    path('bookings/owner/', views.owner_bookings, name='owner_bookings'),
    path('bookings/<int:pk>/<str:new_status>/', views.update_booking_status, name='update_booking_status'),

    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
