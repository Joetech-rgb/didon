from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('feature/', views.feature, name='feature'),
    path('quote/', views.quote, name='quote'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path("404/", views.page_not_found_view, name="page_not_found"),
    path('track/', views.track_shipment, name='track'),
    path('terms/', views.terms, name='terms'),
    path('help/', views.help, name='help'),
    path("air/", views.air, name="air"),
    path("sea/", views.sea, name="sea"),
    path("road/", views.road, name="road"),
    path("warehouse/", views.warehouse, name="warehouse"),
    path("customs/", views.customs, name="customs"),
    path("express/", views.express, name="express"),
    
    # Authentication URLs (UPDATED)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
]

   