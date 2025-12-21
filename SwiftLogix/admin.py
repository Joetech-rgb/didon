from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Shipment, TrackingUpdate, QuoteRequest, ContactMessage, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'company_name', 'city', 'country', 'created_at']
    search_fields = ['user__username', 'user__email', 'company_name', 'phone']
    list_filter = ['country', 'city', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Details', {
            'fields': ('phone', 'company_name')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('created_at',)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        'tracking_number',
        'sender_name',
        'receiver_name',
        'user',  # Added user field
        'status_badge',
        'shipment_type',
        'created_at',
        'expected_delivery_date',
        'weight'
    ]
    list_filter = [
        'status',
        'shipment_type',
        'sender_country',
        'receiver_country',
        'created_at'
    ]
    search_fields = [
        'tracking_number',
        'sender_name',
        'receiver_name',
        'sender_email',
        'receiver_email',
        'user__username'  # Added user search
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Tracking Information', {
            'fields': ('tracking_number', 'status', 'shipment_type', 'user')  # Added user
        }),
        ('Sender Information', {
            'fields': (
                'sender_name', 'sender_email', 'sender_phone',
                'sender_address', 'sender_city', 'sender_country'
            )
        }),
        ('Receiver Information', {
            'fields': (
                'receiver_name', 'receiver_email', 'receiver_phone',
                'receiver_address', 'receiver_city', 'receiver_country'
            )
        }),
        ('Shipment Details', {
            'fields': (
                'weight', 'dimensions',
                'declared_value', 'special_instructions'
            )
        }),
        ('Delivery Information', {
            'fields': ('expected_delivery_date', 'actual_delivery_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('created_at', 'updated_at')

    def status_badge(self, obj):
        """Display status with color-coded badge"""
        status_colors = {
            'pending': '#ffeaa7',
            'picked_up': '#74b9ff',
            'in_transit': '#fd79a8',
            'out_for_delivery': '#fdcb6e',
            'delivered': '#00b894',
            'cancelled': '#fd79a8',
            'on_hold': '#a29bfe'
        }
        color = status_colors.get(obj.status, '#dee2e6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    actions = ['mark_as_delivered', 'mark_as_in_transit', 'mark_as_cancelled']

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} shipments marked as delivered.')
    mark_as_delivered.short_description = "Mark selected shipments as delivered"

    def mark_as_in_transit(self, request, queryset):
        updated = queryset.update(status='in_transit')
        self.message_user(request, f'{updated} shipments marked as in transit.')
    mark_as_in_transit.short_description = "Mark selected shipments as in transit"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} shipments marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected shipments as cancelled"


class TrackingUpdateInline(admin.TabularInline):
    model = TrackingUpdate
    extra = 1
    fields = ['status', 'location', 'description', 'timestamp']
    ordering = ['-timestamp']


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "user",  # Added user field
        "freight_type",
        "departure",
        "delivery",
        "status_badge",
        "created_at",
    )
    list_filter = ("freight_type", "status", "created_at")
    search_fields = ("name", "email", "departure", "delivery", "user__username")  # Added user search
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    fieldsets = (
        ("User Information", {
            "fields": ("user",),
        }),
        ("Contact Information", {
            "fields": ("name", "email", "mobile"),
        }),
        ("Shipment Details", {
            "fields": ("origin", "destination", "departure", "delivery", "freight_type", "weight", "dimensions"),
        }),
        ("Additional Information", {
            "fields": ("special_note", "message"),
        }),
        ("Quote Status", {
            "fields": ("quote_amount", "status"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    def status_badge(self, obj):
        status_colors = {
            "pending": "#ffeaa7",
            "processing": "#74b9ff",
            "quoted": "#00cec9",
            "accepted": "#00b894",
            "declined": "#d63031",
        }
        color = status_colors.get(obj.status, "#dee2e6")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 8px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )
    status_badge.short_description = "Status"

    actions = ["mark_as_quoted", "mark_as_processing"]

    def mark_as_quoted(self, request, queryset):
        updated = queryset.update(status="quoted")
        self.message_user(request, f"{updated} quote requests marked as quoted.")
    mark_as_quoted.short_description = "Mark selected requests as quoted"

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status="processing")
        self.message_user(request, f"{updated} quote requests marked as processing.")
    mark_as_processing.short_description = "Mark selected requests as processing"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)