"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

airportsfile = 'Skylines/airports_full.csv'
routesfile = 'Skylines/routes_full.csv'
citiesfile = 'Skylines/worldcities.csv'

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexion")
    print("3- Encontrar clústeres de trafico aereo")
    print("4- Encontrar la ruta mas corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- Comparar con servicio web externo")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        cont = controller.init()
        #cargar datos
        print("\nCargando información ....\n")
        controller.loadServices(cont, airportsfile, routesfile, citiesfile)
        print("El número total de aeropuertos es: " + str(controller.totalAirports(cont)))
        print("El número total de rutas es: " + str(controller.totalRoutes(cont)))
        print("El número total de ciudades es: " + str(controller.totalCities(cont)))
        print("La información del primer aeropuerto cargado es: " + str(controller.infoPrimerAeropuerto(cont)))
        print("La información de la última ciudad cargada es: " + str(controller.infoUltimaCiudad(cont))+"\n")

    elif int(inputs[0]) == 2:
        pass

    else:
        sys.exit(0)
sys.exit(0)
