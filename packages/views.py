from django.shortcuts import render
from django.http import HttpResponse
from .models import Textbook


def packages(request):
    textbooks = Textbook.objects.all()
    context = {'textbooks': textbooks}
    return render(request, 'packages/packages.html', context)


def package(request, pk):
    textbookObj = Textbook.objects.get(id=pk)
    cards = textbookObj.basic_cards_set.all()
    context = {'textbook': textbookObj, 'cards': cards}
    return render(request, 'packages/single-package.html', context)
