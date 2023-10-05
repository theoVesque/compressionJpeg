let inputFichier = document.querySelector(".input-fichier-par-defaut");
let iconeUpload = document.querySelector(".icone-upload");
let texteGlisserDeposer = document.querySelector(".message-dynamique");
let boutonCompresser = document.querySelector(".bouton-uploader");

//Code pour glisser le fichier sur la zone
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


//Code pour afficher l'image de base une fois le bouton compresser sélectionné
document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault(); // Empêchez le formulaire de se soumettre normalement

    // Récupérez l'élément img de l'aperçu de l'image
    const imagePreview = document.querySelector("#image-preview");

    // Récupérez le champ de fichier
    const inputFichier = document.querySelector(".input-fichier-par-defaut");

    // Récupérez l'élément où vous voulez afficher le titre
    const titreImageContainer = document.querySelector("#titre-image-container");

    // Vérifiez si un fichier a été sélectionné
    if (inputFichier.files.length > 0) {
        // Obtenez le premier fichier sélectionné
        const fichier = inputFichier.files[0];

        // Vérifiez si le fichier est sélectionné
        if (fichier) {
            // Créez un texte pour le titre de l'image
            const titreImage = document.createElement('h2');
            titreImage.innerText = "L'image que vous avez sélectionnée :";
            titreImage.style.textAlign = "center";

            // Créez une div pour le titre et l'image
            const titreImageContainer = document.createElement('div');
            titreImageContainer.appendChild(titreImage);
            titreImageContainer.appendChild(imagePreview);
            titreImageContainer.style.marginTop = "-100px";
            imagePreview.style.padding = '2%';

            // Ajoutez la div au document
            document.body.appendChild(titreImageContainer);

            // Créez un objet URL pour l'image
            const imageURL = URL.createObjectURL(fichier);

            // Affichez l'image dans l'aperçu
            imagePreview.src = imageURL;
            imagePreview.style.display = "block";

            // Réinitialisez l'aperçu du fichier si nécessaire
            iconeUpload.innerHTML = 'file_upload';
            texteGlisserDeposer.innerHTML = 'Glissez votre fichier ici';
            boutonCompresser.innerHTML = 'Compresser';
        } else {
            alert("Le fichier sélectionné n'est pas une image.");
        }
    }
});



