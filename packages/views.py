from django.shortcuts import render
from django.http import HttpResponse


def packages(request):
    return render(request, 'packages/packages.html')

# def packages(request):
#     msg = 'Hello, you are on the packages page'
#     return render(request, 'packages/packages.html', {'message': msg})


def package(request, pk):
    return render(request, 'packages/single-package.html')
