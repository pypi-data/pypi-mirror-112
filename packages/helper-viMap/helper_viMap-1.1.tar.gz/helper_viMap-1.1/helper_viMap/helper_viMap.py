from qgis.core import QgsProject, QgsVectorLayer, QgsFeatureRequest

def search_objet(path, name, expression):
    
    try:
        vlayer = QgsVectorLayer(path, name, "ogr")
    except:
        vlayer = QgsProject.instance().mapLayersByName(name)[0]
        
    features = []
    if expression != "All":
        features = [f for f in vlayer.getFeatures(QgsFeatureRequest().setFilterExpression(expression))]

    else:
        features = [f for f in vlayer.getFeatures()]
    
    return features

def createURI(layer_name):
    #attention la génération automatique du uri ne marche pas dans le cas de certaines couches, la couche est bien créée mais l'ajout des attributs de la couche d'origine est impossible 
    uri = ''
    
    if layer_name == 'infrastructure_area_infrastructure':
        uri = 'Polygon?crs=EPSG:4326'
    elif layer_name == 'junction_remarkable_point':
        uri = 'Point?crs=EPSG:4326'
    elif layer_name == 'level_crossing_area_level_crossing':
        uri = 'Polygon?crs=EPSG:4326'
    elif layer_name == 'pylon':
        uri = 'Point?crs=EPSG:4326'
    elif layer_name == 'stopping_area_stopping_point':
        uri = 'Point?crs=EPSG:4326'
    elif layer_name == 'track_asset_geom':
        uri = 'Point?crs=EPSG:4326'
    elif layer_name == 'track_point':
        uri = 'Point?crs=EPSG:4326'
    elif layer_name == 'track_segment':
        uri = 'Linestring?crs=EPSG:4326'
    
    return uri

def create_new_layer_features(features, new_layer_name, layer_path, layer_name):
    
    try:
        layer = QgsVectorLayer(layer_path, layer_name, "ogr")
    except:
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        
        
    fields = [field for field in layer.fields()]
    
    uri = createURI(layer_name)
            
    vlayer = QgsVectorLayer(uri, new_layer_name, 'memory')
    
    for field in fields:
        vlayer.dataProvider().addAttributes([field])
        
    vlayer.updateFields()
        
    
    #add features to the new layer
    for feature in features:
        vlayer.dataProvider().addFeature(feature)
        
    

    vlayer.updateExtents()
    
    return vlayer
    

def get_pylon_born(born_string):

    if born_string == "0-5" :
        born_inf = "0"
        born_sup = "5"
    elif born_string == "5-10":
        born_inf = "5"
        born_sup = "10"
    elif born_string == "10-15":
        born_inf = "10"
        born_sup = "15"
    else:
        born_inf = "NULL"
        born_sup = "NULL"
    
    return born_inf, born_sup
    
def get_track_segment_born(born_string):

    if born_string == "0-100":
        born_sup = "100"
        born_inf = "0"
    elif born_string == "100-200":
        born_sup = "200"
        born_inf = "100"
    elif born_string == "200-300":
        born_sup = "300"
        born_inf = "200"
    elif born_string == "300-400":
        born_sup = "400"
        born_inf = "300"
    elif born_string == "400-500":
        born_sup = "500"
        born_inf = "400"
    elif born_string == "500-600":
        born_sup = "600"
        born_inf = "500"
    elif born_string == "600-700":
        born_sup = "700"
        born_inf = "600"
    elif born_string == "700-800":
        born_sup = "800"
        born_inf = "700"
    elif born_string =="800-900":
        born_sup = "800"
        born_inf = "900"
    elif born_string == ">900":
        born_sup = "2000"
        born_inf = "900"
    else:
        born_sup = "NULL"
        born_inf = "NULL"
    
    return born_inf, born_sup