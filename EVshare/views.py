from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import Charger, Booking, CONNECTOR_CHOICES
from .forms import ChargerForm, BookingRequestForm


def home(request):
    featured = Charger.objects.filter(is_available=True)[:6]
    return render(request, 'EVshare/home.html', {'featured': featured})


# ---------- SEARCH (driver finds a charger) ----------
def search_chargers(request):
    chargers = Charger.objects.filter(is_available=True)

    city = request.GET.get('city', '').strip()
    connector = request.GET.get('connector_type', '').strip()

    if city:
        chargers = chargers.filter(city__icontains=city)
    if connector:
        chargers = chargers.filter(connector_type=connector)

    context = {
        'chargers': chargers,
        'connector_choices': CONNECTOR_CHOICES,
        'selected_city': city,
        'selected_connector': connector,
    }
    return render(request, 'EVshare/search.html', context)


# ---------- CHARGER DETAIL + BOOK ----------
def charger_detail(request, pk):
    charger = get_object_or_404(Charger, pk=pk)
    form = None

    if request.user.is_authenticated and request.user != charger.owner:
        if request.method == 'POST':
            form = BookingRequestForm(request.POST)
            if form.is_valid():
                booking = form.save(commit=False)
                booking.charger = charger
                booking.driver = request.user
                booking.save()
                messages.success(request, "Booking request sent to the owner.")
                return redirect('charger_detail', pk=charger.pk)
        else:
            form = BookingRequestForm()

    return render(request, 'EVshare/charger_detail.html', {
        'charger': charger,
        'form': form,
    })


# ---------- ADD A CHARGER (owner lists their charger) ----------
@login_required
def add_charger(request):
    if request.method == 'POST':
        form = ChargerForm(request.POST)
        if form.is_valid():
            charger = form.save(commit=False)
            charger.owner = request.user
            charger.save()
            messages.success(request, "Your charger is now listed.")
            return redirect('charger_detail', pk=charger.pk)
    else:
        form = ChargerForm()

    return render(request, 'EVshare/add_charger.html', {'form': form})


# ---------- DELETE A CHARGER (owner only) ----------
@login_required
def delete_charger(request, pk):
    charger = get_object_or_404(Charger, pk=pk, owner=request.user)
    if request.method == 'POST':
        charger.delete()
        messages.success(request, "Your charger listing has been deleted.")
        return redirect('profile')
    return render(request, 'EVshare/delete_charger_confirm.html', {'charger': charger})


# ---------- DRIVER: my booking requests ----------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(driver=request.user).select_related('charger')
    return render(request, 'EVshare/my_bookings.html', {'bookings': bookings})


# ---------- OWNER: requests made on my chargers ----------
@login_required
def owner_bookings(request):
    bookings = Booking.objects.filter(charger__owner=request.user).select_related('charger', 'driver')
    return render(request, 'EVshare/owner_bookings.html', {'bookings': bookings})


@login_required
def update_booking_status(request, pk, new_status):
    booking = get_object_or_404(Booking, pk=pk, charger__owner=request.user)
    if new_status in dict(Booking._meta.get_field('status').choices):
        booking.status = new_status
        booking.save()
        messages.success(request, f"Booking marked as {new_status}.")
    return redirect('owner_bookings')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            from django.contrib.auth import login
            login(request, user)
            messages.success(request, "Welcome to EVshare!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'EVshare/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'EVshare/profile.html', {
        'chargers': request.user.chargers.all(),
    })


def about(request):
    return render(request, 'EVshare/about.html')


def contact(request):
    return render(request, 'EVshare/contact.html')
