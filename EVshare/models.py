from django.db import models
from django.conf import settings
from django.urls import reverse


CONNECTOR_CHOICES = [
    ('type1', 'Type 1 (J1772)'),
    ('type2', 'Type 2 (Mennekes)'),
    ('ccs', 'CCS'),
    ('chademo', 'CHAdeMO'),
    ('tesla', 'Tesla / NACS'),
]

BOOKING_STATUS = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]


class Charger(models.Model):
    """An EV charger listed by its owner."""
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chargers'
    )
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    connector_type = models.CharField(max_length=20, choices=CONNECTOR_CHOICES)
    power_kw = models.DecimalField(max_digits=5, decimal_places=1, help_text="Charging speed in kW")
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.city})"

    def get_absolute_url(self):
        return reverse('charger_detail', args=[self.pk])


class Booking(models.Model):
    """Connects a driver to an owner's charger for a time slot."""
    charger = models.ForeignKey(Charger, on_delete=models.CASCADE, related_name='bookings')
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='pending')
    message = models.CharField(max_length=255, blank=True, help_text="Optional note to the owner")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.driver} -> {self.charger} ({self.status})"
