from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name="packages"),
    path('package/<str:pk>/<str:card>/<int:answer>',
         views.package, name="package"),
    path('create-package/', views.createTextbook, name="create-package"),
    path('cards-finished/<str:pk>/', views.cardsFinished, name="cards-finished"),
    path('reset-textbook/<str:pk>/', views.resetTextbook, name="reset-textbook"),
]
