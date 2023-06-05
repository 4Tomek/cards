from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name="packages"),
    path('package/<str:pk>/<str:card>/<int:answer>',
         views.package, name="package"),
    path('create-cards/', views.createCards, name="create-cards"),
    path('create-textbook/', views.createTextbook, name="create-textbook"),
    path('cards-finished/<str:pk>/', views.cardsFinished, name="cards-finished"),
    path('reset-textbook/<str:pk>/', views.resetTextbook, name="reset-textbook"),
]
