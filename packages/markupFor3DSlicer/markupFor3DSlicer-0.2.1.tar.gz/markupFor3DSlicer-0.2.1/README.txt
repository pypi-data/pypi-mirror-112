Librairie que renvoit un simple dictionnaire comportant la mise en page qui lui permet d'être lu par 3D Slicer en temps que fichier markups.

Fonctions :

line(x,y,z,vectX,vectY,vectZ,norme,name='vect',large=0.3)
    - x,y,z : position de depart
    - vectX,vectY,vectZ : position d'arriver
    - norme : taille de la ligne
    - name : nom de la ligne (optionnel)
    - large : largeur de la ligne (optionnel)

point(x,y,z,name="point",large=5.0)
    - x,y,z : position du point
    - name : nom du point (optionnel)
    - large : largeur du point (optionnel)

final(suite)
    - suite : suite contenant tout les dictionnaire creer precedement (Attention, il est imperatif que la condition soit une suite et non un dictionnaire)