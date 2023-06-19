from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Textbook, Lesson, Card, ProfileCard, LastingCard
import random
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta


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
                NewLastingCard, create = LastingCard.objects.get_or_create(
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
        profile=request.user.profile, active=True, scheduled__lt=datetime.now(), seen_today=False)

    if cardsToRepeat:
        if answer:
            if answer == 1:
                cardCorrectlyAnswered = cardsToRepeat.get(id=card)

                difficulty = 0

                if cardCorrectlyAnswered.wrong_in_row_0 > 10:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_in_row_1 > 20:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_in_row_2 > 30:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_in_row_0 > 5:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_in_row_1 > 10:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_in_row_2 > 20:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_in_row_0 > 0:
                    difficulty += 1
                elif cardCorrectlyAnswered.wrong_in_row_1 > 1:
                    difficulty += 1
                elif cardCorrectlyAnswered.wrong_in_row_2 > 2:
                    difficulty += 1

                if cardCorrectlyAnswered.wrong_ever_counter > 120:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_ever_counter > 40:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_ever_counter > 5:
                    difficulty += 1

                if cardCorrectlyAnswered.correct_in_row == 0:
                    plan = 3
                elif cardCorrectlyAnswered.correct_in_row == 1:
                    plan = 7
                elif cardCorrectlyAnswered.correct_in_row == 2:
                    plan = 15
                elif cardCorrectlyAnswered.correct_in_row == 3:
                    plan = 35
                elif cardCorrectlyAnswered.correct_in_row == 5:
                    plan = 50
                else:
                    plan = 13 * cardCorrectlyAnswered.correct_in_row

                interval = plan - difficulty
                if interval < 1:
                    interval = 1

                cardCorrectlyAnswered.last_correct = datetime.now()
                cardCorrectlyAnswered.scheduled = datetime.now() + timedelta(days=interval)
                cardCorrectlyAnswered.seen_today = False
                cardCorrectlyAnswered.correct_in_row += 1
                cardCorrectlyAnswered.wrong_in_row_2 = cardCorrectlyAnswered.wrong_in_row_1
                cardCorrectlyAnswered.wrong_in_row_1 = cardCorrectlyAnswered.wrong_in_row_0
                cardCorrectlyAnswered.wrong_in_row_0 = 0
                cardCorrectlyAnswered.save()

                cardsToRepeat = LastingCard.objects.filter(
                    profile=request.user.profile, active=True, scheduled__lte=datetime.now(), seen_today=False)
            if answer == 2:
                cardWrongAnswered = cardsToRepeat.get(id=card)
                cardWrongAnswered.scheduled = datetime.now()
                cardWrongAnswered.seen_today = True
                cardWrongAnswered.correct_in_row = 0
                cardWrongAnswered.wrong_in_row_0 += 1
                cardWrongAnswered.wrong_ever_counter += 1
                cardWrongAnswered.save()

                cardsToRepeat = LastingCard.objects.filter(
                    profile=request.user.profile, active=True, scheduled__lte=datetime.now(), seen_today=False)

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

    return redirect('add-lasting-cards')


def finishCards(request, card=None, answer=None, lastCard=None):

    cardsToRepeat = LastingCard.objects.filter(
        profile=request.user.profile, active=True, scheduled__lte=datetime.now())

    if cardsToRepeat:
        if answer:
            if answer == 1:
                cardCorrectlyAnswered = cardsToRepeat.get(id=card)

                difficulty = 0

                if cardCorrectlyAnswered.wrong_in_row_0 > 10:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_in_row_1 > 20:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_in_row_2 > 30:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_in_row_0 > 5:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_in_row_1 > 10:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_in_row_2 > 20:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_in_row_0 > 0:
                    difficulty += 1
                elif cardCorrectlyAnswered.wrong_in_row_1 > 1:
                    difficulty += 1
                elif cardCorrectlyAnswered.wrong_in_row_2 > 2:
                    difficulty += 1

                if cardCorrectlyAnswered.wrong_ever_counter > 120:
                    difficulty += 3
                elif cardCorrectlyAnswered.wrong_ever_counter > 40:
                    difficulty += 2
                elif cardCorrectlyAnswered.wrong_ever_counter > 5:
                    difficulty += 1

                if cardCorrectlyAnswered.correct_in_row == 0:
                    plan = 3
                elif cardCorrectlyAnswered.correct_in_row == 1:
                    plan = 7
                elif cardCorrectlyAnswered.correct_in_row == 2:
                    plan = 15
                elif cardCorrectlyAnswered.correct_in_row == 3:
                    plan = 35
                elif cardCorrectlyAnswered.correct_in_row == 5:
                    plan = 50
                else:
                    plan = 13 * cardCorrectlyAnswered.correct_in_row

                interval = plan - difficulty
                if interval < 1:
                    interval = 1

                cardCorrectlyAnswered.last_correct = datetime.now()
                cardCorrectlyAnswered.scheduled = datetime.now() + timedelta(days=interval)
                cardCorrectlyAnswered.seen_today = False
                cardCorrectlyAnswered.correct_in_row += 1
                cardCorrectlyAnswered.wrong_in_row_2 = cardCorrectlyAnswered.wrong_in_row_1
                cardCorrectlyAnswered.wrong_in_row_1 = cardCorrectlyAnswered.wrong_in_row_0
                cardCorrectlyAnswered.wrong_in_row_0 = 0
                cardCorrectlyAnswered.save()

                cardsToRepeat = LastingCard.objects.filter(
                    profile=request.user.profile, active=True, scheduled__lte=datetime.now())
            if answer == 2:
                cardWrongAnswered = cardsToRepeat.get(id=card)
                cardWrongAnswered.scheduled = datetime.now()
                cardWrongAnswered.seen_today = True
                cardWrongAnswered.correct_in_row = 0
                cardWrongAnswered.wrong_in_row_0 += 1
                cardWrongAnswered.wrong_ever_counter += 1
                cardWrongAnswered.save()

                cardsToRepeat = LastingCard.objects.filter(
                    profile=request.user.profile, active=True, scheduled__lte=datetime.now())

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
            return render(request, 'textbooks/finish-lasting-card.html', context)

    return render(request, 'textbooks/learning-finished.html')


def activateLastingCards(request, cardsToFinishToday=None, cardsToActivate=None):
    if request.method == 'POST':
        cardsNumber = int(request.POST.get('cards_number'))
        cardsToActivate = LastingCard.objects.filter(
            profile=request.user.profile, active=False)
        for i in range(cardsNumber):
            try:
                card = random.choice(cardsToActivate)
                card.active = True
                card.save()
                cardsToActivate = LastingCard.objects.filter(
                    profile=request.user.profile, active=False)
            except:
                messages.error(
                    request, 'You run out of cards, you can go into your textbooks and activate more lessons')
                break
        return redirect('repeat-cards')

    cardsToFinishToday = len(LastingCard.objects.filter(
        profile=request.user.profile, active=True, scheduled__lte=datetime.now()))
    cardsToActivate = len(LastingCard.objects.filter(
        profile=request.user.profile, active=False))

    context = {'cardsToFinishToday': cardsToFinishToday,
               'cardsToActivate': cardsToActivate}
    return render(request, 'textbooks/add-lasting-cards.html', context)
