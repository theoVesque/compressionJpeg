from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UploadFileForm


def compression(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        #if form.is_valid():
        # faire la compression ici
        # return HttpResponse('Le fichier a été téléchargé avec succès.')
        #else:
        #   return HttpResponse('Aucun fichier n\'a été téléchargé.')
    return render(request, 'listings/compression.html')


def decompression(request):
    return render(request, 'listings/decompression.html')
