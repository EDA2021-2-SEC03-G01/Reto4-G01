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


from DISClib.DataStructures.chaininghashtable import keySet
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa


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

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
