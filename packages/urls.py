from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name="packages"),
    path('package/<str:pk>', views.package, name="package"),
]
