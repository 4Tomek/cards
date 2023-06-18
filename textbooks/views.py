from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Textbook, Lesson, Card, ProfileCard, LastingCard
import random
from django.contrib import messages
from django.db.models import Q
from datetime import datetime


def listTextbooks(request):
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
    return render(request, 'textbooks/textbooks.html', context)


def showCard(request, pk, card=None, answer=None, lastCard=None):
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
        return render(request, 'textbooks/cards-finished.html', context)
    else:
        context = {'textbook': textbookObj, 'card': card, 'lastCard': lastCard}
        return render(request, 'textbooks/card.html', context)


def pickLessons(request, pk):
    textbook = Textbook.objects.get(id=pk)
    lessons = Lesson.objects.filter(textbook=textbook)
    if request.method == 'POST':
        lessonsIds = request.POST.getlist('selected_lessons')
        ProfileCard.objects.filter(profile=request.user.profile).delete()

        if lessonsIds:
            cards = []
            for lesson in lessonsIds:
                lessonCards = Card.objects.filter(
                    textbook=textbook, lesson=lesson)
                cards += lessonCards

            for card in cards:
                PrivateCard = ProfileCard.objects.create(
                    profile=request.user.profile, card=card, mastered=False)
                PrivateCard.save()

            return redirect('show-cards', pk=pk)
        else:
            messages.error(
                request, 'You must select at least one lesson')

    context = {'pk': pk, 'lessons': lessons}
    return render(request, 'textbooks/pick-lessons.html', context)


def cardsFinished(request):
    return render(request, 'textbooks/cards-finished.html')


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
                    return render(request, 'textbooks/textbook_form.html')
                else:
                    textbook.save()
                    if lessonsNames:
                        for lesson in lessonsNames:
                            lesson = lesson.strip()
                            lesson, created = Lesson.objects.get_or_create(
                                name=lesson, textbook=textbook)
                            lesson.save()

                    return redirect('create-cards', textbook=textbook.id)
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
                messages.error(
                    request, "You sent an empty form, try again")
                return redirect('create-lessons', textbookId=textbook.id)
            return redirect('create-cards', textbook=textbook.id)

    context = {'textbookId': textbookId}
    return render(request, 'textbooks/textbook_form.html', context)


def createCards(request, textbook):
    textbook = Textbook.objects.get(id=textbook)
    lessons = Lesson.objects.filter(textbook=textbook)
    if request.method == 'POST':
        for lesson in lessons:
            content = request.POST.get(lesson.name)
            if content:
                if ',' in content:
                    content = content.split(',')
                else:
                    content = [content]

                for card in content:
                    if '-' in card:
                        question, answer = card.split('-')
                        question = question.strip()
                        answer = answer.strip()
                        card, created = Card.objects.get_or_create(
                            question=question, answer=answer, textbook=textbook, lesson=lesson)
                        card.save()
                    else:
                        messages.error(
                            request, f'You must split each question and answer by "-", {card} failed')

    context = {'textbook': textbook, 'lessons': lessons}
    return render(request, "textbooks/cards_form.html", context)


def activateLessons(request, pk):
    textbook = Textbook.objects.get(id=pk)
    lessons = Lesson.objects.filter(textbook=textbook)
    if request.method == 'POST':
        lessonsIds = request.POST.getlist('selected_lessons')

        if lessonsIds:
            cards = []
            for lesson in lessonsIds:
                lessonCards = Card.objects.filter(
                    textbook=textbook, lesson=lesson)
                cards += lessonCards

            for card in cards:
                NewLastingCard = LastingCard.objects.create(
                    profile=request.user.profile, card=card)
                NewLastingCard.save()

            return redirect('repeat-cards')
        else:
            messages.error(
                request, 'You must select at least one lesson')

    context = {'pk': pk, 'lessons': lessons}
    return render(request, 'textbooks/activate-lessons.html', context)


def repeatCards(request, card=None, answer=None, lastCard=None):
    cardsToRepeat = LastingCard.objects.filter(
        profile=request.user.profile, active=True, scheduled__lt=datetime.now())

    if cardsToRepeat:
        if answer:
            if answer == 1:
                cardCorrectAnswered = cardsToRepeat.get(id=card)
                cardCorrectAnswered.last_correct = datetime.now()
                cardCorrectAnswered.active = True
                cardCorrectAnswered.correct_in_row += 1
                cardCorrectAnswered.wrong_in_row = 0
                cardCorrectAnswered.save()

                cardsToRepeat = LastingCard.objects.filter(
                    profile=request.user.profile, active=True, scheduled__lt=datetime.now())
            if answer == 2:
                cardWrongAnswered = cardsToRepeat.get(id=card)
                cardWrongAnswered.scheduled = datetime.now()
                cardWrongAnswered.active = True
                cardWrongAnswered.correct_in_row = 0
                cardWrongAnswered.wrong_in_row += 1
                cardWrongAnswered.wrong_ever_counter += 1
                cardWrongAnswered.save()

                cardsToRepeat = LastingCard.objects.filter(
                    profile=request.user.profile, active=True, scheduled__lt=datetime.now())

        if cardsToRepeat:
            repetitionNotChecked = True
            if lastCard == None:
                card = random.choice(cardsToRepeat)
                repetitionNotChecked = False

            while repetitionNotChecked:
                card = random.choice(cardsToRepeat)
                if len(cardsToRepeat) < 2:
                    repetitionNotChecked = False
                if card.card.question != lastCard:
                    repetitionNotChecked = False
            lastCard = card.card.question
            context = {'card': card, 'lastCard': lastCard}
            return render(request, 'textbooks/lasting-card.html', context)

    return redirect('repeat-next-card')


def activateLastingCards(request):
    return render(request, 'textbooks/add-lasting-cards.html')
