import numpy as np
from numpy import linalg as LA, sqrt

def line(x,y,z,vectX,vectY,vectZ,norme,name='vect',large=0.3,color=[0.4, 1.0, 0.0],selectedColor=[1.0, 0.5000076295109484, 0.5000076295109484]):
    dLine={
            "type": "Line",
            "coordinateSystem": "LPS",
            "locked": True,
            "labelFormat": "%N-%d",
            "controlPoints": [
                {
                    "id": "1",
                    "label": f"point_{name}-1",
                    "description": "",
                    "associatedNodeID": "vtkMRMLScalarVolumeNode1",
                    "position": [y, x, z],
                    "orientation": [-1.0, -0.0, -0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 1.0],
                    "selected": True,
                    "locked": True,
                    "visibility": True,
                    "positionStatus": "defined"
                },
                {
                    "id": "2",
                    "label": f"point_{name}-2",
                    "description": "",
                    "associatedNodeID": "vtkMRMLScalarVolumeNode1",
                    "position": [vectY, vectX, vectZ],
                    "orientation": [-1.0, -0.0, -0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 1.0],
                    "selected": True,
                    "locked": True,
                    "visibility": True,
                    "positionStatus": "defined"
                }
            ],
            "measurements": [
                {
                    "name": f"trait_{name}",
                    "enabled": True,
                    "value": norme,
                    "printFormat": "%-#4.4gmm"
                }
            ],
            "display": {
                "visibility": True,
                "opacity": 1.0,
                "color": color,
                "selectedColor": selectedColor,
                "activeColor": [0.4, 1.0, 0.0],
                "propertiesLabelVisibility": True,
                "pointLabelsVisibility": False,
                "textScale": 3.0,
                "glyphType": "Sphere3D",
                "glyphScale": 1.0,
                "glyphSize": 5.0,
                "useGlyphScale": True,
                "sliceProjection": False,
                "sliceProjectionUseFiducialColor": True,
                "sliceProjectionOutlinedBehindSlicePlane": False,
                "sliceProjectionColor": [1.0, 1.0, 1.0],
                "sliceProjectionOpacity": 0.6,
                "lineThickness": large,
                "lineColorFadingStart": 1.0,
                "lineColorFadingEnd": 10.0,
                "lineColorFadingSaturation": 1.0,
                "lineColorFadingHueOffset": 0.0,
                "handlesInteractive": False,
                "snapMode": "toVisibleSurface"
            }
        }
    return dLine

def point(x,y,z,name="point",large=5.0,color=[0.4, 1.0, 0.0],selectedColor=[1.0, 0.5000076295109484, 0.5000076295109484]):
    dPoint={
            "type": "Fiducial",
            "coordinateSystem": "LPS",
            "locked": True,
            "labelFormat": "%N-%d",
            "controlPoints": [
                {
                    "id": "1",
                    "label": name,
                    "description": "",
                    "associatedNodeID": "vtkMRMLScalarVolumeNode1",
                    "position": [y, x, z],
                    "orientation": [-1.0, -0.0, -0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 1.0],
                    "selected": True,
                    "locked": True,
                    "visibility": True,
                    "positionStatus": "defined"
                }
            ],
            "measurements": [],
            "display": {
                "visibility": True,
                "opacity": 1.0,
                "color": color,
                "selectedColor": selectedColor,
                "activeColor": [0.4, 1.0, 0.0],
                "propertiesLabelVisibility": False,
                "pointLabelsVisibility": True,
                "textScale": 3.0,
                "glyphType": "Sphere3D",
                "glyphScale": 1.0,
                "glyphSize": large,
                "useGlyphScale": True,
                "sliceProjection": False,
                "sliceProjectionUseFiducialColor": True,
                "sliceProjectionOutlinedBehindSlicePlane": False,
                "sliceProjectionColor": [1.0, 1.0, 1.0],
                "sliceProjectionOpacity": 0.6,
                "lineThickness": 0.2,
                "lineColorFadingStart": 1.0,
                "lineColorFadingEnd": 10.0,
                "lineColorFadingSaturation": 1.0,
                "lineColorFadingHueOffset": 0.0,
                "handlesInteractive": False,
                "snapMode": "toVisibleSurface"
            }
        }
    return dPoint

def final(liste):
    final={
            "@schema": "https://raw.githubusercontent.com/slicer/slicer/master/Modules/Loadable/Markups/Resources/Schema/markups-schema-v1.0.0.json#",
            "markups": liste
        }
    return final

def rotatBbox(vectPro, centroid, coords):
    vectPro.tolist().append(centroid)
    clustRot=[]
    for i in coords:
        clustRot.append(np.dot(vectPro,i))
    
    clustRot = np.array(clustRot)
    clustRot= np.rot90(clustRot)

    bbox=[[min(clustRot[0]),max(clustRot[0])],
            [min(clustRot[1]),max(clustRot[1])],
            [min(clustRot[2]),max(clustRot[2])]]
    
    long=[bbox[0][1]-bbox[0][0], bbox[1][1]-bbox[1][0], bbox[2][1]-bbox[2][0]]

    return bbox, long

def calcul(centroid, long, vectPro):
    y,x,z=centroid

    norme1=sqrt(long[0]**2 + long[1]**2 + long[2]**2)
    norme1=round(norme1,0)
    vectProNorme=vectPro*norme1

    x1,y1,z1=-x+(vectProNorme[0][1]/2),-y-(vectProNorme[0][0]/2),z

    vectX=x1-vectProNorme[0][1]
    vectY=y1+vectProNorme[0][0]
    vectZ=z1+vectProNorme[0][2]

    norme = sqrt(vectProNorme[0][0]**2 + vectProNorme[0][1]**2 + vectProNorme[0][2]**2)

    return x1,y1,z1, vectX,vectY,vectZ, norme, x,y,z