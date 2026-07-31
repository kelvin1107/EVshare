from django.contrib import admin
from .models import Charger, Booking


@admin.register(Charger)
class ChargerAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'city', 'connector_type', 'price_per_hour', 'is_available')
    list_filter = ('connector_type', 'is_available', 'city')
    search_fields = ('title', 'city', 'owner__username')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('charger', 'driver', 'status', 'start_time', 'end_time')
    list_filter = ('status',)
