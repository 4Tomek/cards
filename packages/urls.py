from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name="packages"),
    path('package/<str:pk>/<str:card>/<int:answer>/<str:lastCard>/',
         views.package, name="package"),

    path('activate/<str:pk>/<str:card>/<int:answer>/',
         views.activateLessons, name="activate-lessons"),
    path('cards-finished/<str:pk>/<str:card>/<int:answer>/',
         views.cardsFinished, name="cards-finished"),

    path('create-textbook/',
         views.createTextbook, name="create-textbook"),
    path('create-textbook/<str:textbookId>',
         views.createTextbook, name="create-lessons"),
    path('create-cards/<str:textbook>/',
         views.createCards, name="create-cards"),
]
