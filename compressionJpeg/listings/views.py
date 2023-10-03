from django.shortcuts import render
from django.http import HttpResponse

def compression(request):
    return HttpResponse('<h1>Hello world!</h1>')


def decompression(request):
    return HttpResponse('<h1>Hello world 2!</h1>')

