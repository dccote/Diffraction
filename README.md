# Diffraction

Vous trouverez dans ces deux repertoires du code pour calculer la diffraction: un pour MATLAB, un en Python.

## Python

Le code Python est particulièrement simple: une somme d'onde sphérique, sur une fente de largeur $S$. On regarde sur un écran à une distance $R$. C'est tout.

Le code est d'une lenteur à faire peur. Toute personne le moindrement renseigné comprendra qu'une version en transformée de Fourier discrète sera essentiellement instantanée. 





## MATLAB

Ce code MATLAB extrêmement simple permet de visualiser la diffraction d'une fente carrée, circulaire ou arbitraire.

Trois choix de fentes: carrée, circulaire, abritraire.
Trois "sliders": zoom in/out de l'image, intensité (pour mieux voir le contraste quitte à saturer) et grosseur de l'objet.

### Utilisation
1) Téléchargez le code ici en cliquant sur le bouton vert Clone or Download, ensuite Download zip.
2) Ouvrir MATLAB
3) Aller dans le repertoire où le code a été décompressé
4) tapez guiDiffraction dans la console MATLAB

### Plan général pour le code
1) Ajouter les échelles d'espace au niveau de la fente et du patron de diffraction
2) Corriger l'interface qui a l'air d'avoir été fait par mon fils (Luc, 4 ans).
3) Changer le lookup table pour avoir les images en spectrum
4) Permettre de charger n'importe quel image, pas juste mon image arbitraire.
5) Cotinuer le Unit Testing, qui est en cours de developpement.
6) Completement refactoriser le code: sera fait après l'ajout du Unit Testing.
7) Peut-etre en faire une version Python, puisque tout le monde utilise Python maintenant.

