# SwiftLogix/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Shipment, TrackingUpdate, QuoteRequest
from django.utils import timezone
from django.contrib import messages
from .models import ContactMessage
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'service.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")
        
        # Save message to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )
        
        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")
    
    return render(request, "contact.html")

def pricing(request):
    return render(request, 'price.html')

def feature(request):
    return render(request, 'feature.html')

def terms(request):
    return render(request, 'terms.html')
def help(request):
    return render(request, 'help.html')
def air(request):
    return render(request, 'air.html')  
def sea(request):
    return render(request, 'sea.html')
def road(request):
    return render(request, 'road.html')
def warehouse(request):
    return render(request, 'warehouse.html')
def customs(request):
    return render(request, 'customs.html')
def express(request):
    return render(request, 'express.html')


def track(request):
    tracking_number = request.GET.get("tracking_number")
    shipment = None
    if tracking_number:
        shipment = get_object_or_404(Shipment, tracking_id=tracking_number)
    return render(request, "track.html", {"shipment": shipment})



def quote(request):
    if request.method == 'POST':
        try:
            quote_request = QuoteRequest.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                mobile=request.POST.get('mobile'),
                freight_type=request.POST.get('freight'),
                origin=request.POST.get('origin', ''),
                destination=request.POST.get('destination', ''),
                weight=request.POST.get('weight', ''),
                dimensions=request.POST.get('dimensions', ''),
                special_note=request.POST.get('note', '')
            )
            messages.success(request, 'Your quote request has been submitted successfully! We will contact you soon.')
            return redirect('quote')  # <-- Important to redirect after POST
        except Exception as e:
            # Show the real error for debugging
            messages.error(request, f"There was an error: {e}")
    
    return render(request, 'quote.html')

def team(request):
    return render(request, 'team.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def page_not_found_view(request, exception=None):
    return render(request, '404.html', status=404)

def track_shipment(request):
    context = {
        'shipment': None,
        'tracking_updates': None,
        'error_message': None
    }
    
    if request.method == 'GET' and 'tracking_number' in request.GET:
        tracking_number = request.GET.get('tracking_number', '').strip()
        
        if tracking_number:
            try:
                shipment = Shipment.objects.get(tracking_number__iexact=tracking_number)
                tracking_updates = shipment.tracking_updates.all()
                context.update({
                    'shipment': shipment,
                    'tracking_updates': tracking_updates
                })
            except Shipment.DoesNotExist:
                context['error_message'] = f"No shipment found with tracking number: {tracking_number}"
        else:
            context['error_message'] = "Please enter a valid tracking number."
    
    return render(request, 'track.html', context)

# API endpoint for AJAX tracking requests
def track_shipment_api(request):
    if request.method == 'GET':
        tracking_number = request.GET.get('tracking_number', '').strip()
        
        if not tracking_number:
            return JsonResponse({
                'success': False,
                'error': 'Please enter a tracking number'
            })
        
        try:
            shipment = Shipment.objects.get(tracking_number__iexact=tracking_number)
            tracking_updates = shipment.tracking_updates.all()
            
            updates_data = []
            for update in tracking_updates:
                updates_data.append({
                    'status': update.get_status_display(),
                    'location': update.location,
                    'description': update.description,
                    'timestamp': update.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'date': update.timestamp.strftime('%b %d, %Y'),
                    'time': update.timestamp.strftime('%I:%M %p')
                })
            
            return JsonResponse({
                'success': True,
                'shipment': {
                    'tracking_number': shipment.tracking_number,
                    'status': shipment.get_status_display(),
                    'status_code': shipment.status,
                    'progress': shipment.get_progress_percentage(),
                    'sender_name': shipment.sender_name,
                    'sender_city': shipment.sender_city,
                    'sender_country': shipment.sender_country,
                    'receiver_name': shipment.receiver_name,
                    'receiver_city': shipment.receiver_city,
                    'receiver_country': shipment.receiver_country,
                    'shipment_type': shipment.get_shipment_type_display(),
                    'pickup_date': shipment.pickup_date.strftime('%Y-%m-%d'),
                    'expected_delivery': shipment.expected_delivery_date.strftime('%Y-%m-%d'),
                    'actual_delivery': shipment.actual_delivery_date.strftime('%Y-%m-%d') if shipment.actual_delivery_date else None,
                    'weight': str(shipment.weight),
                    'dimensions': shipment.dimensions,
                    'package_description': shipment.package_description
                },
                'tracking_updates': updates_data
            })
            
        except Shipment.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'No shipment found with tracking number: {tracking_number}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })
# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('home')  # or a dashboard page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

# Logout view
def logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

# Register view (for clients)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, "Passwords do not match!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful! You can log in now.")
            return redirect('login')
    return render(request, 'register.html')
