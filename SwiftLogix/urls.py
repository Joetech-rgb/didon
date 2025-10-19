from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),  # Changed: service → services
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),     # Changed: price → pricing
    path('feature/', views.feature, name='feature'),
    path('quote/', views.quote, name='quote'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path("404/", views.page_not_found_view, name="page_not_found"),
    path('track/', views.track_shipment, name='track'),
    path('terms/', views.terms, name='terms'),            # Added: terms page
    path('help/', views.help, name='help'),  
    path("air/", views.air, name="air"),
    path("sea/", views.sea, name="sea"),
    path("road/", views.road, name="road"),
    path("warehouse/", views.warehouse, name="warehouse"),
    path("customs/", views.customs, name="customs"),
    path("express/", views.express, name="express"),  # Added: express page
     path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register')

              # Added: help page
]