import pandas as pd
from controllers.via_manager import ViaManager
from controllers.estacion_manager import EstacionManager
from controllers.sentido_manager import SentidoManager
from controllers.tramo_manager import TramoManager
from modelos.via import Via
from controllers.db import session
from modelos.estacion import Estacion
from modelos.tramo import Tramo
from modelos.sentido import Sentido


class ArchivoManager:
    def __init__(self, archivo):
        self.archivo = archivo
        self.df = None

    def leer_archivo(self):
        self.df = pd.read_excel(self.archivo)

    def cargar_estaciones(self, id_ramal):

        em = EstacionManager(session=session, id_ramal=id_ramal)

        stations_dict = {}

        for _, row in self.df.iterrows():
            nombre_estacion = str(row["StationName"]).strip()
            km_inicio = float(row["sKm"])
            km_fin = float(row["eKm"])

            # Verificar si ya existe en la DB
            existente = session.query(Estacion).filter_by(nombre=nombre_estacion, id_ramal=id_ramal).first()

            if existente:
                stations_dict[nombre_estacion] = existente.id
                continue

            nueva = em.agregar_estacion(nombre_estacion, km_inicio, km_fin)

            if nueva:
                stations_dict[nombre_estacion] = nueva.to_dict()["id"]

        return stations_dict

    def cargar_tramos(self, id_ramal):

        estaciones = self.cargar_estaciones(id_ramal)

        sm = SentidoManager(session=session)
        tm = TramoManager(session=session)
        vm = ViaManager(session=session, id_ramal=id_ramal)

        # Creación de tramos consecutivos
        for i in range(len(self.df) - 1):
            origen_name = self.df.loc[i, "StationName"]
            destino_name = self.df.loc[i + 1, "StationName"]
            sentido = self.df.loc[i, "direction"]

            origen_id = estaciones.get(origen_name)
            destino_id = estaciones.get(destino_name)
            if origen_id is None or destino_id is None:
                print(f"⚠️ Estación faltante: {origen_name} o {destino_name}")
                continue

            sentido_obj = session.query(Sentido).filter_by(nombre=sentido).first()
            if not sentido_obj:
                sm.agregar_sentido(nombre=sentido)
                sentido_obj = session.query(Sentido).filter_by(nombre=sentido).first()

            vias_existentes = session.query(Via).filter_by(id_ramal=id_ramal, id_sentido=sentido_obj.id).all()
            if sentido == "ascendente":
                via_numero = 1
                if vias_existentes:
                    numeros_usados = [v.numero for v in vias_existentes if v.numero % 2 == 1]
                    while via_numero in numeros_usados:
                        via_numero += 2
            else:
                via_numero = 2
                if vias_existentes:
                    numeros_usados = [v.numero for v in vias_existentes if v.numero % 2 == 0]
                    while via_numero in numeros_usados:
                        via_numero += 2

            via_dict = vm.agregar_via(id_sentido=sentido_obj.id, numero=via_numero)
            via_id = via_dict["id"]

            # Crear el tramo
            tramo = Tramo(
                id_ramal=id_ramal,
                estacion_origen_id=origen_id,
                estacion_destino_id=destino_id,
                km_inicio=float(self.df.loc[i, "sKm"]),
                km_fin=float(self.df.loc[i + 1, "sKm"]),
                id_via=via_id
            )

            tm.agregar_tramo(tramo)