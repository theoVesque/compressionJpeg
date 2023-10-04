let inputFichier = document.querySelector(".input-fichier-par-defaut");
let iconeUpload = document.querySelector(".icone-upload");
let texteGlisserDeposer = document.querySelector(".message-dynamique");
let boutonCompresser = document.querySelector(".bouton-uploader");

inputFichier.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    iconeUpload.innerHTML = 'file_download';
    texteGlisserDeposer.innerHTML = 'Glissez votre fichier ici !';
});

inputFichier.addEventListener("dragleave", (e) => {
    e.preventDefault();
    e.stopPropagation();
    iconeUpload.innerHTML = 'file_upload';
    texteGlisserDeposer.innerHTML = 'Glissez votre fichier ici';
});

inputFichier.addEventListener("drop", (e) => {
    e.preventDefault();
    e.stopPropagation();

    let fichiers = e.dataTransfer.files;
    if (fichiers.length > 0) {
        iconeUpload.innerHTML = 'check_circle';
        texteGlisserDeposer.innerHTML = 'Fichier pris en compte';
        boutonCompresser.innerHTML = 'Compresser';

        // Utilisez la variable "fichiers" pour accéder aux fichiers déposés si nécessaire.
        console.log(fichiers[0].name + " " + fichiers[0].size);
        // Mettez à jour le champ de fichier avec les fichiers déposés.
        inputFichier.files = fichiers;
    }
});

inputFichier.addEventListener("change", (e) => {
    if (inputFichier.files.length > 0) {
        iconeUpload.innerHTML = 'check_circle';
        texteGlisserDeposer.innerHTML = 'Fichier sélectionné';
        boutonCompresser.innerHTML = 'Compresser';
    }
});
