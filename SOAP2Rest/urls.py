from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.convert_soap_to_rest, name='convert_soap_to_rest'),
]
