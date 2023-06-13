from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Textbook, Lesson, Basic_card, ProfileCard
import random
from django.contrib import messages
from django.db.models import Q


def packages(request):
    search_query = ''
    if request.user.is_authenticated:
        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')

        textbooks = Textbook.objects.filter(Q(name__icontains=search_query) & Q(
            Q(owner=request.user.profile) | Q(is_public=True)))
    else:
        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')

        textbooks = Textbook.objects.filter(
            Q(name__icontains=search_query) & Q(is_public=True))

    context = {'textbooks': textbooks, 'search_query': search_query}
    return render(request, 'packages/packages.html', context)


def package(request, pk, card, answer, lastCard):
    textbookObj = Textbook.objects.get(id=pk)
    cards = ProfileCard.objects.filter(
        profile=request.user.profile, mastered=False)
    cardsFinished = True

    if cards:
        cardsFinished = False

        if answer:
            cardRight = cards.get(id=card)
            cardRight.mastered = True
            cardRight.save()

            cards = ProfileCard.objects.filter(
                profile=request.user.profile, mastered=False)

        if cards:
            repetitionNotChecked = True
            if lastCard == 'None':
                card = random.choice(cards)
                repetitionNotChecked = False

            while repetitionNotChecked:
                card = random.choice(cards)
                if len(cards) < 2:
                    repetitionNotChecked = False
                if card.card.question != lastCard:
                    repetitionNotChecked = False
            lastCard = card.card.question
        else:
            cardsFinished = True

    if cardsFinished:                 # if i have no cards with: 'mastered=False'
        textbookId = textbookObj.id
        context = {'textbookId': textbookId}
        ProfileCard.objects.filter(profile=request.user.profile).delete()
        return render(request, 'packages/cards-finished.html', context)
    else:
        context = {'textbook': textbookObj, 'card': card, 'lastCard': lastCard}
        return render(request, 'packages/single-package.html', context)


def activateLessons(request, pk, card, answer):
    textbook = Textbook.objects.get(id=pk)
    lessons = Lesson.objects.filter(textbook=textbook)
    if request.method == 'POST':
        lessonsIds = request.POST.getlist('selected_lessons')
        ProfileCard.objects.filter(profile=request.user.profile).delete()

        if lessonsIds:
            cards = []
            for lesson in lessonsIds:
                lessonCards = Basic_card.objects.filter(
                    textbook=textbook, lesson=lesson)
                cards += lessonCards

            for card in cards:
                PrivateCard = ProfileCard.objects.create(
                    profile=request.user.profile, card=card, mastered=False)
                PrivateCard.save()

            return redirect('package', pk=pk, card=card, answer=answer, lastCard=None)

    context = {'pk': pk, 'card': card, 'answer': answer, 'lessons': lessons}
    return render(request, 'packages/activate-lessons.html', context)


def cardsFinished(request):
    return render(request, 'packages/cards-finished.html')


@login_required(login_url="login")
def createTextbook(request, textbookId=None):
    if request.method == 'POST':
        if not textbookId:
            profile = request.user.profile
            textbookName = request.POST.get('newTextbook')
            lessonsNames = request.POST.get('lessons')
            if lessonsNames:
                lessonsNames = lessonsNames.split(',')
            if textbookName:
                textbookName = textbookName.strip()
                textbook, created = Textbook.objects.get_or_create(
                    name=textbookName, owner=profile)
                if created == False:
                    messages.error(
                        request, "Textbook with this name already exists, choose another name")
                    return render(request, 'packages/textbook_form.html')
                else:
                    textbook.save()
                    if lessonsNames:
                        for lesson in lessonsNames:
                            lesson = lesson.strip()
                            lesson, created = Lesson.objects.get_or_create(
                                name=lesson, textbook=textbook)
                            lesson.save()

                    textbookId = textbook.id
                    return redirect('select-lesson', textbookId=textbookId)
        else:
            textbook = Textbook.objects.get(id=textbookId)
            lessonsNames = request.POST.get('lessons')
            if lessonsNames:
                lessonsNames = lessonsNames.split(',')
                for lesson in lessonsNames:
                    lesson = lesson.strip()
                    lesson, created = Lesson.objects.get_or_create(
                        name=lesson, textbook=textbook)
                    lesson.save()
            else:
                print("something went wrong")
            textbookId = textbook.id
            return redirect('create-cards', textbookId=textbookId)

    context = {'textbookId': textbookId}
    return render(request, 'packages/textbook_form.html', context)


def createCards(request, textbook):
    textbook = Textbook.objects.get(id=textbook)
    lessons = Lesson.objects.filter(textbook=textbook)
    if request.method == 'POST':
        for lesson in lessons:
            content = request.POST.get(lesson.name)
            if content:
                if ',' in content:
                    content = content.split(',')

                    for card in content:
                        if '-' in card:
                            question, answer = card.split('-')
                            question = question.strip()
                            answer = answer.strip()
                            card, created = Basic_card.objects.get_or_create(
                                question=question, answer=answer, textbook=textbook, lesson=lesson)
                            card.save()
                        else:
                            messages.error(
                                request, f'You must split each question and answer by "-", {card} failed')
                else:
                    messages.error(request, 'You must to split cards by ","')

    context = {'textbook': textbook, 'lessons': lessons}
    return render(request, "packages/cards_form.html", context)
