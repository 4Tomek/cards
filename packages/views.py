from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Textbook, Lesson, Basic_card
from .forms import PackageForm
import random


def packages(request):
    textbooks = Textbook.objects.all()
    context = {'textbooks': textbooks}
    return render(request, 'packages/packages.html', context)


def package(request, pk, card, answer):
    textbookObj = Textbook.objects.get(id=pk)
    cards = textbookObj.basic_card_set.filter(mastered=False)
    cardsFinished = True

    if cards:
        cardsFinished = False
        if answer:
            cardRight = cards.get(id=card)
            cardRight.mastered = True
            cardRight.save()

            cards = textbookObj.basic_card_set.filter(mastered=False)

        if cards:
            card = random.choice(cards)
        else:
            cardsFinished = True

    # if i have no cards with: 'mastered=False'
    if cardsFinished:
        textbookId = textbookObj.id
        context = {'textbook': textbookId}
        return render(request, 'packages/cards-finished.html', context)
    else:
        context = {'textbook': textbookObj, 'card': card}
        return render(request, 'packages/single-package.html', context)


def createTextbook(request):
    if request.method == 'POST':
        textbookName = request.POST.get('newTextbook')
        lessonsNames = request.POST.get('lessons').split(',')
        message = ''
        if textbookName:
            textbookName = textbookName.strip()
            textbook, created = Textbook.objects.get_or_create(
                name=textbookName)
            if created == False:
                message = "textbook with this name already exists, choose another name"
                context = {'message': message}
                return render(request, 'packages/textbook_form.html', context)
            else:
                textbook.save()
                if lessonsNames:
                    for lesson in lessonsNames:
                        lesson = lesson.strip()
                        lesson, created = Lesson.objects.get_or_create(
                            name=lesson, textbook=textbook)
                        lesson.save()

                form = PackageForm()
                context = {'form': form}
                return render(request, 'packages/cards_form.html', context)
    return render(request, 'packages/textbook_form.html')


def createCards(request):
    form = PackageForm()

    if request.method == 'POST':

        form = PackageForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content').split(',')

            formData = form.save(commit=False)
            textbookObj = formData.textbook
            lessonObj = formData.lesson

            for task in content:
                question, answer = task.split('-')
                question = question.strip()
                answer = answer.strip()
                card, created = Basic_card.objects.get_or_create(
                    question=question, answer=answer, textbook=textbookObj, lesson=lessonObj)
                card.save()

            return redirect('packages')

    context = {'form': form}
    return render(request, "packages/cards_form.html", context)


def cardsFinished(request, pk):
    textbook = pk
    context = {'textbook': textbook}
    return render(request, 'packages/cards-finished')


def resetTextbook(request, pk):
    textbookObj = Textbook.objects.get(id=pk)
    cards = textbookObj.basic_card_set.all()
    for card in cards:
        card.mastered = False
        card.save()
    textbooks = Textbook.objects.all()
    context = {'textbooks': textbooks}
    return render(request, 'packages/packages.html', context)
