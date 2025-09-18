from modelos import Ramal, Tramo, Estacion, ViaSegmento, TipoRiel, Via
from sqlalchemy import select, or_, func
import pandas as pd
from collections import defaultdict
from sqlalchemy.orm import joinedload

def ramales_de_linea(session, id_linea):
    """
    Retorna todos los ramales que pertenecen a una línea específica.
    """
    return session.query(Ramal).filter(Ramal.id_linea == id_linea).all()

def estaciones_por_linea_ramal(session, id_linea, id_ramal):
    # Verificar que el ramal pertenece a la línea
    ramal = session.get(Ramal, id_ramal)
    if not ramal or ramal.id_linea != id_linea:
        return []

    # Estaciones asociadas a tramos del ramal
    stmt = (
        select(Estacion)
        .join(
            Tramo,
            or_(
                Tramo.estacion_origen_id == Estacion.id,
                Tramo.estacion_destino_id == Estacion.id
            )
        )
        .where(Tramo.id_ramal == id_ramal)
    )
    estaciones = session.execute(stmt).scalars().all()

    # Eliminar duplicados
    estaciones_unicas = {e.id: e for e in estaciones}.values()
    return list(estaciones_unicas)

def tramos_tipo_riel(session, id_ramal, estacion_origen, estacion_destino):
    """
    Devuelve un DataFrame con todos los tramos de un ramal
    y los segmentos de vía asociados con su tipo de riel,
    incluyendo vías ascendentes y descendentes, entre dos estaciones.
    """
    # Obtener estaciones
    est_origen = session.query(Estacion).filter_by(nombre=estacion_origen).first()
    est_destino = session.query(Estacion).filter_by(nombre=estacion_destino).first()

    if not est_origen or not est_destino:
        return pd.DataFrame()  # si alguna no existe

    if est_origen.id == est_destino.id:
        return pd.DataFrame()  # origen y destino iguales

    # Determinar rango de km
    km_inicio = min(est_origen.kilometro_inicio, est_destino.kilometro_inicio)
    km_fin = max(est_origen.kilometro_fin, est_destino.kilometro_fin)

    # Traer todos los tramos del ramal dentro del rango
    tramos = (
        session.query(Tramo)
        .filter(
            Tramo.id_ramal == id_ramal,
            Tramo.km_inicio <= km_fin,
            Tramo.km_fin >= km_inicio
        )
        .order_by(Tramo.km_inicio)
        .all()
    )

    data = []

    for tramo in tramos:
        # Traer todas las vías del tramo (ascendente y descendente)
        vias_tramo = session.query(Via).filter_by(id_ramal=id_ramal).all()

        for via in vias_tramo:
            segmentos = (
                session.query(ViaSegmento)
                .filter(
                    ViaSegmento.id_via == via.id,
                    ViaSegmento.km_inicio <= tramo.km_fin,
                    ViaSegmento.km_fin >= tramo.km_inicio
                )
                .order_by(ViaSegmento.km_inicio)
                .all()
            )

            merged = []
            prev_tipo, prev_inicio, prev_fin = None, None, None

            for seg in segmentos:
                tipo = session.get(TipoRiel, seg.id_tipo_riel)
                tipo_nombre = tipo.nombre if tipo else "N/A"

                if prev_tipo == tipo_nombre and abs(prev_fin - seg.km_inicio) < 0.001:
                    prev_fin = seg.km_fin
                else:
                    if prev_tipo is not None:
                        merged.append((prev_inicio, prev_fin, prev_tipo))
                    prev_tipo, prev_inicio, prev_fin = tipo_nombre, seg.km_inicio, seg.km_fin

            if prev_tipo is not None:
                merged.append((prev_inicio, prev_fin, prev_tipo))

            for inicio, fin, tipo in merged:
                data.append({
                    "Tramo": f"{tramo.estacion_origen.nombre} → {tramo.estacion_destino.nombre}",
                    "Km tramo": f"{tramo.km_inicio:.2f} - {tramo.km_fin:.2f}",
                    "Vía": f"{via.numero} ({via.sentido_obj.nombre})" if via.sentido_obj else f"{via.numero}",
                    "Km segmento": f"{inicio:.2f} - {fin:.2f}",
                    "Tipo de riel": tipo
                })

    return pd.DataFrame(data)

def cantidad_km_tipo_riel(session, id_ramal, estacion_origen, estacion_destino):
    """
    Devuelve un DataFrame con la suma de kilómetros por tipo de riel
    y por sentido de vía (ascendente/descendente) entre dos estaciones de un ramal.
    """
    # Obtener estaciones
    est_origen = session.query(Estacion).filter_by(nombre=estacion_origen).first()
    est_destino = session.query(Estacion).filter_by(nombre=estacion_destino).first()

    if not est_origen or not est_destino:
        return pd.DataFrame({"Error": ["No se encontraron las estaciones seleccionadas"]})

    if est_origen.id == est_destino.id:
        return pd.DataFrame({"Error": ["La estación de origen y destino no pueden ser la misma"]})

    # Asegurar orden de km
    km_inicio = min(est_origen.kilometro_inicio, est_destino.kilometro_inicio)
    km_fin = max(est_origen.kilometro_fin, est_destino.kilometro_fin)

    # Traer todas las vías del ramal y cargar su objeto sentido_obj
    vias = (
        session.query(Via)
        .options(joinedload(Via.sentido_obj))
        .filter_by(id_ramal=id_ramal)
        .all()
    )
    via_ids = [v.id for v in vias]

    # Traer todos los segmentos de esas vías dentro del rango de km
    segmentos = (
        session.query(ViaSegmento)
        .filter(
            ViaSegmento.id_via.in_(via_ids),
            ViaSegmento.km_inicio <= km_fin,
            ViaSegmento.km_fin >= km_inicio
        )
        .all()
    )

    # Acumular km por tipo de riel y sentido
    km_dict = defaultdict(lambda: defaultdict(float))  # km_dict[tipo][sentido]

    for seg in segmentos:
        tipo = session.get(TipoRiel, seg.id_tipo_riel)
        via = next((v for v in vias if v.id == seg.id_via), None)
        sentido = via.sentido_obj.nombre if via and via.sentido_obj else "N/A"

        if tipo and via:
            # recortar segmento al rango seleccionado
            seg_inicio = max(seg.km_inicio, km_inicio)
            seg_fin = min(seg.km_fin, km_fin)
            km_dict[tipo.nombre][sentido] += seg_fin - seg_inicio

    # Convertir a DataFrame
    rows = []
    for tipo, sentidos in km_dict.items():
        for sentido, km in sentidos.items():
            rows.append({
                "TipoRiel": tipo,
                "Sentido": sentido,
                "KmTotal": round(km, 2)
            })

    return pd.DataFrame(rows)




    return resumen