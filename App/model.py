"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.ADT.queue import size
from DISClib.DataStructures.chaininghashtable import keySet
import config
from DISClib.ADT.graph import getEdge, gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from math import sin, cos, acos, radians


"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer = {"ciudades":None,
                "aeropuertos":None,
                "rutas_dobles":None,
                "rutas_unicas":None
                }
    analyzer["ciudades"] = mp.newMap(numelements=41001,
                                    maptype='PROBING',
                                    comparefunction=None)
    analyzer["aeropuertos"] = mp.newMap(numelements=9100,
                                        maptype="PROBING",
                                        comparefunction=None)
    analyzer["latitudes"] = mp.newMap(numelements=9100,
                                        maptype="PROBING",
                                        comparefunction=None)
    analyzer["rutas_unicas"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=9100,
                                            comparefunction=None)
    return analyzer

# Funciones para agregar informacion al catalogo
def addAirport (analyzer, airport):
    cod_aeropuerto = airport["IATA"]
    entry = mp.get(analyzer["aeropuertos"], cod_aeropuerto )
    if entry is None:
        datentry = newDataEntry(airport)
        mp.put(analyzer["aeropuertos"], cod_aeropuerto, datentry)
    else:
        datentry = me.getValue(entry)
    airport["num_routes"] = 0
    add(datentry, airport)
    return analyzer

def addLatitud (analyzer, airport):
    latitud = airport["Latitude"]
    entry = mp.get(analyzer["latitudes"], latitud )
    if entry is None:
        datentry = newDataEntry(airport)
        mp.put(analyzer["latitudes"], latitud, datentry)
    else:
        datentry = me.getValue(entry)
    add(datentry, airport)
    return analyzer

def addCiudad(analyzer, city):
    ciudad = city["city"]
    entry = mp.get(analyzer["ciudades"], ciudad)
    if entry is None:
        datentry = newDataEntry(city)
        mp.put(analyzer["ciudades"], ciudad, datentry)
    else:
        datentry = me.getValue(entry)
    add(datentry, city)
    return analyzer


def addConnections (analyzer, route):
    origen = route["Departure"]
    destino = route["Destination"]
    distancia = route["distance_km"]
    addVertex(analyzer, origen)
    addVertex(analyzer, destino)
    addConnection(analyzer, origen, destino, distancia)
    addRoute(analyzer, origen, destino)


def addVertex(analyzer, aeropuerto):
    if not gr.containsVertex(analyzer['rutas_unicas'], aeropuerto):
            gr.insertVertex(analyzer['rutas_unicas'], aeropuerto)
    return analyzer

def addConnection(analyzer, origin, destination, distance):
    edge = gr.getEdge(analyzer['rutas_unicas'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['rutas_unicas'], origin, destination, distance)
    return analyzer

def addRoute(analyzer, origen, destino):
    mp.get(analyzer["aeropuertos"], origen)["value"]["elements"][0]["num_routes"] += 1
    mp.get(analyzer["aeropuertos"], destino)["value"]["elements"][0]["num_routes"] += 1
    return analyzer

def add(datentry, entry):
    lt.addLast(datentry, entry)
    return datentry

def newDataEntry(entry):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry=lt.newList(datastructure="ARRAY_LIST")
    return entry

# Funciones para creacion de datos

# Funciones de consulta

def totalAirports(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['rutas_unicas'])

def totalRoutes(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['rutas_unicas'])

def totalCities(analyzer):
    """
    Retorna el total de ciudades
    """
    return lt.size(mp.keySet(analyzer["ciudades"]))

def infoPrimerAeropuerto(analyzer):
    aeropuerto = lt.getElement(mp.keySet(analyzer["aeropuertos"]), 1)
    return mp.get(analyzer["aeropuertos"], aeropuerto)["value"]["elements"][0]

def infoUltimaCiudad(analyzer):
    ciudad = lt.getElement(mp.keySet(analyzer["ciudades"]), lt.size(mp.keySet(analyzer["ciudades"])))
    return mp.get(analyzer["ciudades"], ciudad)["value"]["elements"][0]

def semiverseno(lat1, lat2, lng1, lng2):
    punto_1 = (radians(float(lat1)), radians(float(lng1)))
    punto_2 = (radians(float(lat2)), radians(float(lng2)))
    distancia = acos(sin(punto_1[0])*sin(punto_2[0]) + cos(punto_1[0])*cos(punto_2[0])*cos(punto_1[1]-punto_2[1]))
    return distancia * 6371.01

def minimumCostPaths(analyzer, initialStation):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['rutas_unicas'], initialStation)
    return analyzer

def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path
# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

#Requerimientos

def req_1(analyzer):
    rutas = analyzer["rutas_unicas"]
    aeropuertos = analyzer["aeropuertos"]
    lista = lt.newList(datastructure="ARRAY_LIST")
    num = 0
    for a in lt.iterator(gr.vertices(rutas)):
        if gr.degree(rutas, a) > 1:
            num += 1
            lt.addLast(lista, mp.get(aeropuertos, a)["value"]["elements"][0])
    return num, lista

def req_2(analyzer, a1, a2):
    rutas = analyzer["rutas_unicas"]
    clusters = scc.KosarajuSCC(rutas)
    num = scc.connectedComponents(clusters)
    mismo = scc.stronglyConnected(clusters, a1, a2)
    return num, mismo

def req_3(analyzer, ciudad_or, ciudad_des):
    centinela=True
    centinela1=True
    lat_ciu_or = mp.get(analyzer["ciudades"], ciudad_or)["value"]["elements"][0]["lat"]
    lng_ciu_or = mp.get(analyzer["ciudades"], ciudad_or)["value"]["elements"][0]["lng"]
    lat_ciu_des = mp.get(analyzer["ciudades"], ciudad_des)["value"]["elements"][0]["lat"]
    lng_ciu_des = mp.get(analyzer["ciudades"], ciudad_des)["value"]["elements"][0]["lng"]
    i=1
    lista_aeropuertos_or = lt.newList(datastructure="ARRAY_LIST")
    lista_aeropuertos_des = lt.newList(datastructure="ARRAY_LIST")
    latitudes = mp.keySet(analyzer["latitudes"])
    while centinela or centinela1:
        for lat in lt.iterator(latitudes):
            aer_lat = mp.get(analyzer["latitudes"], lat)["value"]
            for aer in lt.iterator(aer_lat):
                if (float(lat_ciu_or)-(0.1*i)) <= float(lat) <= (float(lat_ciu_or)+(0.1*i)) and (float(lng_ciu_or)-(0.1*i)) <= float(aer["Longitude"]) <= (float(lng_ciu_or)+(0.1*i)):
                    lt.addLast(lista_aeropuertos_or, aer)
                    centinela = False
                if (float(lat_ciu_des)-(0.1*i)) <= float(lat) <= (float(lat_ciu_des)+(0.1*i)) and (float(lng_ciu_des)-(0.1*i)) <= float(aer["Longitude"]) <= (float(lng_ciu_des)+(0.1*i)):
                    lt.addLast(lista_aeropuertos_des, aer) 
                    centinela1 = False
        i += 1
    menor=9999999
    for aer in lt.iterator(lista_aeropuertos_or):
        print(aer)
        lat = aer["Latitude"]
        lng = aer["Longitude"]
        distancia = semiverseno(lat_ciu_or, lat, lng_ciu_or, lng)
        if distancia <= menor:
            distancia = menor
            origen = aer
    dist_origen = menor
    print(origen)
    menor = 999999
    for aer in lt.iterator(lista_aeropuertos_des):
        print(aer)
        lat = aer["Latitude"]
        lng = aer["Longitude"]
        distancia = semiverseno(lat_ciu_or, lat, lng_ciu_or, lng)
        if distancia <= menor:
            distancia = menor
            destino = aer
    print(destino)
    dist_destino = menor
    caminos_minimos = minimumCostPaths(analyzer, origen)
    camino_minimo = minimumCostPath(analyzer, destino)
    return (origen, destino, camino_minimo)



