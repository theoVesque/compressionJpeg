from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UploadFileForm


def compression(request):
    # vérifie si le formulaire est validé
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            # récupère le taux de compression souhaité (valeurs possibles : compression_basse / compression_moyenne / compression_elevee)
            taux_compression = request.POST.get('taux_compression')

            # Vérifie si un fichier est téléchargé
            if 'file' in request.FILES:
                fichier = request.FILES['file']

            # faire la compression ici

        # else:
        #   return HttpResponse('Aucun fichier n\'a été téléchargé.')

    return render(request, 'listings/compression.html')


def decompression(request):
    return render(request, 'listings/decompression.html')
