from django.shortcuts import render
from django.http import HttpResponse


def packages(request):
    page = 'packeges'
    number = 10
    context = {'page': page, 'number': number}
    return render(request, 'packages/packages.html', context)


def package(request, pk):
    return render(request, 'packages/single-package.html')
