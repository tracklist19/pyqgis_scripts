##########################################################################
###  creates a shape file containing two point geometries with attributes
###  QGIS-Version: 3.16
##########################################################################


### IMPORTS ### 														# Imports nicht notwendig innerhalb qgis_python_console_editor
from qgis.core import *
from qgis.PyQt.QtCore import QVariant
import os


### VARIABLEN ###
outp = "/home/yyyy/_GIS_home_ubu/Ueb_atene/_data_uebAtene/build_data/ppoi_pyqgis_25833.shp" 


### LÖSCHEN if file exists ###
# if os.path.exists(outp):
	# QgsVectorFileWriter.deleteShapeFile(outp)
	# print("Output file already existed and was now deleted.")


########################################################################
### CREATE FIELDS/SPALTEN ###									        # per QgsFields & QgsVectorFileWriter

layerFields = QgsFields()
layerFields.append(QgsField("ID", QVariant.Int))
layerFields.append(QgsField("address", QVariant.String))


### WRITE FILE ###
crs = QgsCoordinateReferenceSystem('EPSG:25833')    					# außerhalb qgis_python_console_editor: CRS zuweisen
#crs = QgsProject.instance().crs()                  					# innerhalb qgis_python_console_editor: nutzt Projekt-CRS
save_options = QgsVectorFileWriter.SaveVectorOptions()
save_options.driverName = "ESRI Shapefile"
save_options.fileEncoding = "UTF-8" 
transform_context = QgsCoordinateTransformContext()

writer = QgsVectorFileWriter.create(outp, layerFields, QgsWkbTypes.Point, crs, transform_context, save_options)

### Fehler-Ausgabe ###
if writer.hasError() != QgsVectorFileWriter.NoError:
    print("Error when creating shapefile: ",  writer.errorMessage())


### ADD FEATURES/GEOMETRIES/ATTRIBUTES ###

features = {															# dictionary_key = ID-attribute
    1 : [395098.517923233564943, 5815344.281443133018911, 'Ederstr_24'],
    2 : [392901.898330981261097, 5815612.682892174459994, 'Weisestr_2'] 
    }

keys = (*features,)            											# Tupel der Dictionary-Keys
n = 1                          											# Zähler für TupelIndex
for i in features:
    feat = QgsFeature()
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(features[i][0], features[i][1])))
    n = n-1                    											# Index des keys-Tupel
    feat.setAttributes([keys[n], features[i][2]])
    writer.addFeature(feat)

### DELETE WRITER : flush file to disk ###

del(writer) 


########################################################################
### File als LAYER LADEN im QGIS-Projekt ###							# falls script im qgis_python_console_editor ausgeführt

#iface.addVectorLayer(outp, '', 'ogr')
