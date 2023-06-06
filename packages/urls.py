from django.urls import path
from . import views

urlpatterns = [
    path('', views.packages, name="packages"),
    path('package/<str:pk>/<str:card>/<int:answer>/',
         views.package, name="package"),
    path('cards-finished/<str:pk>/', views.cardsFinished, name="cards-finished"),
    path('reset-textbook/<str:pk>/', views.resetTextbook, name="reset-textbook"),

    path('create-textbook/',
         views.createTextbook, name="create-textbook"),
    path('create-textbook/<str:textbookId>',
         views.createTextbook, name="create-lessons"),
    path('select-lesson/<str:textbookId>/',
         views.selectLesson, name="select-lesson"),
    path('create-cards/<str:textbook>/<str:lesson>/',
         views.createCards, name="create-cards"),
]
