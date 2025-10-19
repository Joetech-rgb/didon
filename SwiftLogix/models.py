from django.db import models
from django.utils import timezone
import random
import string

class Shipment(models.Model):
    SHIPMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('on_hold', 'On Hold'),
    ]
    
    SHIPMENT_TYPE_CHOICES = [
        ('air', 'Air Freight'),
        ('sea', 'Sea Freight'),
        ('road', 'Road Transport'),
        ('rail', 'Rail Transport'),
    ]

    # Tracking Information
    tracking_number = models.CharField(max_length=20, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=SHIPMENT_STATUS_CHOICES, default='pending')
    shipment_type = models.CharField(max_length=10, choices=SHIPMENT_TYPE_CHOICES)

    # Sender Information
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=20)
    sender_address = models.TextField()
    sender_city = models.CharField(max_length=50)
    sender_country = models.CharField(max_length=50)

    # Receiver Information
    receiver_name = models.CharField(max_length=100)
    receiver_email = models.EmailField()
    receiver_phone = models.CharField(max_length=20)
    receiver_address = models.TextField()
    receiver_city = models.CharField(max_length=50)
    receiver_country = models.CharField(max_length=50)

    # Shipment Details
    package_description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weight in KG")
    dimensions = models.CharField(max_length=100, help_text="L x W x H in cm")
    declared_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Value in USD")

    # Dates
    pickup_date = models.DateTimeField(null=True, blank=True)
    expected_delivery_date = models.DateTimeField()
    actual_delivery_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional Information
    special_instructions = models.TextField(blank=True)
    insurance_coverage = models.BooleanField(default=False)
    signature_required = models.BooleanField(default=False)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.tracking_number} - {self.sender_name} to {self.receiver_name}"
    
    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        super().save(*args, **kwargs)
    
    def generate_tracking_number(self):
        """Generate a unique tracking number"""
        prefix = "SWL"
        random_part = ''.join(random.choices(string.digits, k=10))
        return f"{prefix}{random_part}"
    
    def get_progress_percentage(self):
        """Calculate progress percentage based on status"""
        status_progress = {
            'pending': 10,
            'picked_up': 25,
            'in_transit': 50,
            'out_for_delivery': 75,
            'delivered': 100,
            'cancelled': 0,
            'on_hold': 30,
        }
        return status_progress.get(self.status, 0)


class TrackingUpdate(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='tracking_updates')
    status = models.CharField(max_length=20, choices=Shipment.SHIPMENT_STATUS_CHOICES)
    location = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.status} at {self.location}"


class QuoteRequest(models.Model):
    FREIGHT_CHOICES = [
        ('air', 'Air Freight'),
        ('sea', 'Sea Freight'),
        ('road', 'Road Transport'),
        ('rail', 'Rail Transport'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('quoted', 'Quoted'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    # Contact Information
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number")

    # Shipment Details
    freight_type = models.CharField(
        max_length=10, choices=FREIGHT_CHOICES, verbose_name="Freight Type"
    )
    origin = models.CharField(max_length=100, verbose_name="Origin")
    destination = models.CharField(max_length=100, verbose_name="Destination")
    weight = models.CharField(max_length=50, blank=True, verbose_name="Weight (kg)")
    dimensions = models.CharField(max_length=100, blank=True, verbose_name="Dimensions (LxWxH cm)")

    # Additional Information
    special_note = models.TextField(blank=True, verbose_name="Special Notes")
    quote_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Quote Amount (USD)"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status"
    )

    # New Fields (✅ fixed with null/blank allowed)
    departure = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Departure Location"
    )
    delivery = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Delivery Location"
    )
    message = models.TextField(
        blank=True, null=True, verbose_name="Additional Message"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Quote Request"
        verbose_name_plural = "Quote Requests"

    def __str__(self):
        return f"{self.name} - {self.get_freight_type_display()} ({self.status.capitalize()})"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"
