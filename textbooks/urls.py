from django.urls import path
from . import views

urlpatterns = [
    path('', views.listTextbooks, name="list-textbooks"),
    path('card/<str:pk>/<str:card>/<int:answer>/<str:lastCard>/',
         views.showCard, name="card"),
    path('card/<str:pk>/', views.showCard, name="show-cards"),


    path('repeat-cards/', views.repeatCards,
         name="repeat-cards"),
    path('repeat-cards/<str:card>/<int:answer>/<str:lastCard>/',
         views.repeatCards, name="repeat-next-card"),
    path('activate-lessons/<str:pk>/',
         views.activateLessons, name="activate-lessons"),
    path('add-cards/', views.activateLastingCards, name="add-lasting-cards"),


    path('pick-lessons/<str:pk>/', views.pickLessons, name="pick-lessons"),
    path('cards-finished/<str:pk>/<str:card>/<int:answer>/',
         views.cardsFinished, name="cards-finished"),


    path('create-textbook/',
         views.createTextbook, name="create-textbook"),
    path('create-textbook/<str:textbookId>',
         views.createTextbook, name="create-lessons"),
    path('create-cards/<str:textbook>/',
         views.createCards, name="create-cards"),
]
