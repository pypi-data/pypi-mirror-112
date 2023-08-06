import numpy as np
from numpy import linalg as LA

def rotatBbox(vectPro, centroid, coords):
    vectPro.tolist().append(centroid)
    clustRot=[]
    for i in coords:
        clustRot.append(np.dot(vectPro,i))
    
    clustRot= np.rot90(np.array(clustRot))

    bbox=[[min(clustRot[0]),max(clustRot[0])],
            [min(clustRot[1]),max(clustRot[1])],
            [min(clustRot[2]),max(clustRot[2])]]
    
    long=[bbox[0][1]-bbox[0][0], bbox[1][1]-bbox[1][0], bbox[2][1]-bbox[2][0]]

    return bbox, long

def calcul(centroid, vectPro, long):
    p1,p2,norme=[],[],[]
    for dim in range(3):
        vectProNorme = vectPro[dim]*long[dim]

        p1.append(centroid - (vectProNorme/2))
        p2.append(p1[dim] + vectProNorme)

        norme.append(LA.norm(vectProNorme))

    return p1, p2, norme