from db import session
from modelos import Ramal, Estacion, Tramo, Sentido, Via
import pandas as pd

ramal = session.query(Ramal).filter_by(nombre="Constitucion - La Plata").first()

df = pd.read_excel('stations/roca/constitucion_laplata.xlsx')

# Guardamos todas las estaciones primero
stations_dict = {}
for _, row in df.iterrows():
    station = session.query(Estacion).filter_by(nombre=row["StationName"]).first()
    if not station:
        station = Estacion(
            nombre=row["StationName"],
            kilometro_inicio=row["sKm"],
            kilometro_fin=row["eKm"]
        )
        session.add(station)
        session.flush()  # para que station.id esté disponible
    stations_dict[row["StationName"]] = station.id

session.commit()

# Creamos los tramos consecutivos
for i in range(len(df)-1):
    origen_name = df.loc[i, "StationName"]
    destino_name = df.loc[i+1, "StationName"]
    sentido = df.loc[i, "direction"]  # "ascendente" o "descendente"

    # Determinar número de vía según sentido
    via_numero = 1 if sentido.lower() == "ascendente" else 2

    # Buscar o crear la vía
    via = session.query(Via).filter_by(id_ramal=ramal.id, numero=via_numero).first()
    if not via:
        # Crear el sentido si no existe
        sentido_obj = session.query(Sentido).filter_by(nombre=sentido).first()
        if not sentido_obj:
            sentido_obj = Sentido(nombre=sentido)
            session.add(sentido_obj)
            session.flush()

        # Crear la vía
        via = Via(id_ramal=ramal.id, id_sentido=sentido_obj.id, numero=via_numero)
        session.add(via)
        session.flush()

    # Crear el tramo
    tramo = Tramo(
        id_ramal=ramal.id,
        estacion_origen_id=stations_dict[origen_name],
        estacion_destino_id=stations_dict[destino_name],
        km_inicio=df.loc[i, "sKm"],
        km_fin=df.loc[i + 1, "sKm"],
        id_via=via.id
    )
    session.add(tramo)

# Confirmamos todos los cambios
session.commit()

