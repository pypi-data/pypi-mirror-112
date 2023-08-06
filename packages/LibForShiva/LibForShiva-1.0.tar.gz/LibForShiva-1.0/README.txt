Librairie utile pour simplifier le programme. Librairie déstiné au projet Shiva.

Dépendance :

- Numpy

Fonctions :

line(x,y,z,vectX,vectY,vectZ,norme,name='vect',large=0.3, color=[0.4, 1.0, 0.0], selectedColor=[1.0, 0.5000076295109484, 0.5000076295109484]) :

    - x,y,z : position de depart
    - vectX,vectY,vectZ : position d'arriver
    - norme : taille de la ligne
    - name : nom de la ligne (optionnel)
    - large : largeur de la ligne (optionnel)
    - color : couleur du Markups (optionnel)
    - selectedColor : couleur du Markups (optionnel)


point(x,y,z,name="point",large=5.0, color=[0.4, 1.0, 0.0], selectedColor=[1.0, 0.5000076295109484, 0.5000076295109484]) :

    - x,y,z : position du point
    - name : nom du point (optionnel)
    - large : largeur du point (optionnel)
    - color : couleur du Markups (optionnel)
    - selectedColor : couleur du markup (optionnel)


final(suite) :

    - suite : suite contenant tout les dictionnaire creer precedement (Attention, il est imperatif que la condition soit une suite et non un dictionnaire)


rotatBbox(vectPro, centroid, coords) :

    - vectPro : le vecteur propre de l'objet
    - centroid : le centroid de l'objet
    - coords : les coordonnées de chaque voxel de l'objet


calcul(centroid, long, vectPro) :

    - centroid : le centroid de l'objet
    - long : les longueurs renvoyées par rotatBbox(...)
    - vectPro : le vecteur propre de l'objet