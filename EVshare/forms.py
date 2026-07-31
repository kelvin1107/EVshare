from django import forms
from .models import Charger, Booking


class ChargerForm(forms.ModelForm):
    class Meta:
        model = Charger
        fields = [
            'title', 'address', 'city', 'latitude', 'longitude', 'connector_type',
            'power_kw', 'price_per_hour', 'description', 'is_available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
        }


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'message']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'message': forms.TextInput(attrs={'placeholder': 'Anything the owner should know?'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned
