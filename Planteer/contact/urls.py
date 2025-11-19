from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_page, name='contact'),
    path('success/', views.contact_success, name='contact_success'),
    path('messages/', views.contact_messages, name='contact_messages'),
]
