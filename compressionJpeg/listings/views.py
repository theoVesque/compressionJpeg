from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

def compression(request):
    return render(request, 'listings/compression.html')


def decompression(request):
    return HttpResponse('<h1>Hello world 2!</h1>')


