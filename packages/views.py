from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Textbook, Basic_card
from .forms import PackageForm


def packages(request):
    textbooks = Textbook.objects.all()
    context = {'textbooks': textbooks}
    return render(request, 'packages/packages.html', context)


def package(request, pk):
    textbookObj = Textbook.objects.get(id=pk)
    cards = textbookObj.basic_card_set.all()
    context = {'textbook': textbookObj, 'cards': cards}
    return render(request, 'packages/single-package.html', context)


def createTextbook(request):
    form = PackageForm()

    if request.method == 'POST':

        form = PackageForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content').split(',')

            formData = form.save(commit=False)
            textbookObj = formData.textbook

            for task in content:
                question, answer = task.split('-')
                question = question.strip()
                answer = answer.strip()
                card, created = Basic_card.objects.get_or_create(
                    question=question, answer=answer, textbook=textbookObj)
                card.save()

            return redirect('packages')

    context = {'form': form}
    return render(request, "packages/package_form.html", context)
