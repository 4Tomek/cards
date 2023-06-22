from django.urls import path
from . import views

urlpatterns = [
    path('', views.listTextbooks, name="list-textbooks"),
    path('textbooks/card/<str:pk>/<str:card>/<int:answer>/<str:lastCard>/',
         views.showCard, name="card"),
    path('textbooks/card/<str:pk>/', views.showCard, name="show-cards"),


    path('long-learning/repeat-cards/', views.repeatCards,
         name="repeat-cards"),
    path('long-learning/repeat-cards/<str:card>/<int:answer>/<str:lastCard>/',
         views.repeatCards, name="repeat-next-card"),
    path('long-learning/activate-lessons/<str:pk>/',
         views.activateLessons, name="activate-lessons"),
    path('long-learning/deactivate-lessons/<str:pk>/',
         views.deactivateLessons, name="deactivate-lessons"),
    path('long-learning/add-cards/',
         views.activateLastingCards, name="add-lasting-cards"),
    path('long-learning/finish-cards/', views.finishCards,
         name="finish-learning"),
    path('long-learning/finish-cards/<str:card>/<int:answer>/<str:lastCard>/', views.finishCards,
         name="finish-cards"),


    path('pick-lessons/<str:pk>/', views.pickLessons, name="pick-lessons"),
    path('cards-finished/<str:pk>/<str:card>/<int:answer>/',
         views.cardsFinished, name="cards-finished"),


    path('create-textbook/',
         views.createTextbook, name="create-textbook"),
    path('textbooks/create-lessons/<str:textbookId>',
         views.createTextbook, name="create-lessons"),
    path('textbooks/create-cards/<str:textbook>/',
         views.createCards, name="create-cards"),

    path('about/', views.about, name="about"),
]
