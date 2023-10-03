from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

def compression(request):
    return render(request, 'listings/compression.html')


def decompression(request):
    return render(request, 'listings/decompression.html')


