Librairie utile pour simplifier le programme. Librairie destinee au projet Shiva.

Dependance :

- Numpy

Fonctions :

line(p1,p2,norme,name='vect',large=0.3, color=[0.4, 1.0, 0.0], selectedColor=[1.0, 0.5000076295109484, 0.5000076295109484]) :

    - p1 : position de depart (x,y,z)
    - p2 : position d'arriver (x,y,z)
    - norme : taille de la ligne
    - name : nom de la ligne (optionnel)
    - large : largeur de la ligne (optionnel)
    - color : couleur du Markups (optionnel)
    - selectedColor : couleur du Markups (optionnel)


point(p1,name="point",large=5.0, color=[0.4, 1.0, 0.0], selectedColor=[1.0, 0.5000076295109484, 0.5000076295109484]) :

    - p1 : position du point (x,y,z)
    - name : nom du point (optionnel)
    - large : largeur du point (optionnel)
    - color : couleur du Markups (optionnel)
    - selectedColor : couleur du markup (optionnel)


final(suite) :

    - suite : suite contenant tout les dictionnaire creer precedement (Attention, il est imperatif que la condition soit une suite et non un dictionnaire)


rotatBbox(vectPro, centroid, coords) :

    - vectPro : le vecteur propre de l'objet
    - centroid : le centroid de l'objet
    - coords : les coordonnees de chaque voxel de l'objet


calcul(centroid, long, vectPro) :

    - centroid : le centroid de l'objet
    - long : les longueurs renvoyees par rotatBbox(...)
    - vectPro : le vecteur propre de l'objet