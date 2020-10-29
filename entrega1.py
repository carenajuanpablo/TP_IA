from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    astar
)
import random

from simpleai.search.viewers import WebViewer, BaseViewer

ciudades_conectadas = {
    'santo_tome': [('angelica', 85), ('sauce_viejo', 15), ('santa_fe', 5)],
    'esperanza': [('recreo', 20), ('rafaela', 70)],
    'sunchales': [('lehmann', 32)],
    'lehmann': [('rafaela', 8), ('sunchales', 32)],
    'rafaela': [('susana', 10), ('esperanza', 70), ('lehmann', 8)],
    'recreo': [('santa_fe', 10), ('esperanza', 20)],
    'susana': [('angelica', 25), ('rafaela', 10)],
    'san_vicente': [('angelica', 18)],
    'angelica': [('san_vicente', 18), ('sc_de_saguier', 60), ('susana', 25), ('santo_tome', 85)],
    'santa_fe': [('santo_tome', 5), ('recreo', 10)],
    'sauce_viejo': [('santo_tome', 15)]
}

Itinerario = planear_camiones(
    # método de búsqueda a utilizar. Puede ser: astar, breadth_first, depth_first, uniform_cost o greedy
    metodo="astar",
    camiones=[
        # id, ciudad de origen, y capacidad de combustible máxima (litros)
        ('c1', 'rafaela', 1.5),
        ('c2', 'rafaela', 2),
        ('c3', 'santa_fe', 2),
    ],
    paquetes=[
        # id, ciudad de origen, y ciudad de destino
        ('p1', 'rafaela', 'angelica'),
        ('p2', 'rafaela', 'santa_fe'),
        ('p3', 'esperanza', 'susana'),
        ('p4', 'recreo', 'san_vicente'),
    ],
)

ciudad_de_carga = ['santa_fe', 'rafaela']


def planear_camiones(metodo, camiones, paquetes):
    listacamion = []
    listapaq = []

    for camion in camiones:
        listacamion.append((camion[0], camion[1], camion[2], ()))

    for paquete in paquetes:
        listapaq.append((paquete[0]))

    INITIAL_STATE = (tuple(listacamion), tuple(listapaq))


class mercadoArtificial(SearchProblem):

    def is_goal(self, state):
        # es estado meta si los camiones están en las ciudades de Rafaela o SantaFe y a su vez no tienen más paquetes
        # para entregar
        esmeta = true
        camiones, paquetes = state
        if len(paquetes) > 0:
            esmeta = false
        else:
            for camion in camiones:
                a, ciudad, b, c = camion
                if ciudad in ciudad_de_carga:
                    esmeta = true
        return esmeta

    def cost(self, state, action, state2):
        return action[2]

    def actions(self, state):
        acciones = []
        camiones, paquetes = state
        # Recorro cada camión y por cada uno de ellos, las ciudades a las que puede ir desde donde está parado
        for camion in camiones:
            nrocam, ciudad_actual, litros_nafta, paq = camion

            for ciudad in ciudades_conectadas[ciudad_actual]:
                #Calculo cuantos litros de nafta necesito para llegar a destino
                consumo_necesario = ciudad[1]/100
                if consumo_necesario <= litros_nafta:
                    # Si tengo nafta suficiente, genero nueva acción y la agrego a la lista
                    nueva_accion = nrocam, ciudad[0], consumo_necesario
                    acciones.append(nueva_accion)
        return acciones

    def result(self, state, action):
        camiones, paquetes = state
        nrocamion, ciudad_a_mover, consumo_necesario = action
        # Con el id de camion del action localizamos a que camion pertenece de nuestro estado.
        for camion in camiones:
            if (camion[0] == id_camion):
                camion_encontrado = camion
        camion_estado, ciudad_estado, litros_estado, paquetes_estado = camion_encontrado

        # Recorremos la lista de paquetes para averiguar si algunos de ellos
        # esta para ser recogido por el camión que se encuentra en esa ciudad
        for paquete in paquetes:
            id_paquete, origen_paquete, destino_paquete = paquete
            if (origen_paquete == ciudad_estado):
                paquetes_estado.append(paquete)

        # Recorremos la lista de paquetes del camión que identificamos en el
        # accion para entregarlos en caso que la ciudad del camión sea igual
        # a la ciudad de entrega del paquete
        for paquetes_camion in paquetes_estado:
            id_paquete, origen_paquete, destino_paquete = paquetes_camion
            if (destino_paquete == ciudad_estado):
                paquetes_estado.remove(paquetes_camion)

        # Si nos encintramos en una ciudad de carga entonces llenamos el tanque
        # y actualizamos el valor de litros del camion
        litros_estado = litros_estado - consumo_necesario
        if ciudad_a_mover in ciudad_de_carga:
            for camion in camiones:
                if camion[0] == nrocamion:
                    tanque = camion[2]
            litros_estado = tanque

        camion_encontrado = (camion_estado, ciudad_estado, litros_estado, paquetes_estado)
        return state

    # Calcula la cantidad de paquetes que quedan por entregar
    def heuristic (self, state):
        return len(state[1])



