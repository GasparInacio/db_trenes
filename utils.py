from modelos import Ramal, Tramo, Estacion, ViaSegmento, TipoRiel, Via
from sqlalchemy import select, or_, func
import pandas as pd
from collections import defaultdict

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

def tramos_tipo_riel(session, id_ramal):
    """
    Devuelve un DataFrame con todos los tramos de un ramal
    y los segmentos de vía asociados con su tipo de riel.
    """
    tramos = (
        session.query(Tramo)
        .filter_by(id_ramal=id_ramal)
        .order_by(Tramo.km_inicio)
        .all()
    )

    data = []

    for tramo in tramos:
        via = tramo.via_obj
        if via is None:
            continue  # saltar tramos sin vía asignada

        segmentos = (
            session.query(ViaSegmento)
            .filter(
                ViaSegmento.id_via == via.id,
                ViaSegmento.km_inicio <= tramo.km_fin,
                ViaSegmento.km_fin >= tramo.km_inicio
            )
            .order_by(ViaSegmento.km_inicio)  # importante para mergear
            .all()
        )

        merged = []
        prev_tipo = None
        prev_inicio = None
        prev_fin = None

        for seg in segmentos:
            tipo = session.get(TipoRiel, seg.id_tipo_riel)
            tipo_nombre = tipo.nombre if tipo else "N/A"

            if prev_tipo == tipo_nombre and abs(prev_fin - seg.km_inicio) < 0.001:
                # mismo tipo y son consecutivos (o casi)
                prev_fin = seg.km_fin
            else:
                # guardar el anterior
                if prev_tipo is not None:
                    merged.append((prev_inicio, prev_fin, prev_tipo))
                # iniciar nuevo bloque
                prev_tipo = tipo_nombre
                prev_inicio = seg.km_inicio
                prev_fin = seg.km_fin

        # guardar el último bloque
        if prev_tipo is not None:
            merged.append((prev_inicio, prev_fin, prev_tipo))

        # agregar al dataframe
        for inicio, fin, tipo in merged:
            data.append({
                "Tramo": f"{tramo.estacion_origen.nombre} → {tramo.estacion_destino.nombre}",
                "Km tramo": f"{tramo.km_inicio:.2f} - {tramo.km_fin:.2f}",
                "Vía": f"{via.numero} ({via.sentido_obj.nombre})" if via.sentido_obj else f"{via.numero}",
                "Km segmento": f"{inicio:.2f} - {fin:.2f}",
                "Tipo de riel": tipo
            })

    return pd.DataFrame(data)

def cantidad_km_tipo_riel(session, id_ramal):
    # Diccionario para acumular kilómetros por tipo de riel
    km_dict = defaultdict(float)

    # 1️⃣ Traer todas las vías del ramal
    vias = session.query(Via).filter_by(id_ramal=id_ramal).all()
    via_ids = [v.id for v in vias]

    # 2️⃣ Traer todos los segmentos de esas vías
    segmentos = session.query(ViaSegmento).filter(ViaSegmento.id_via.in_(via_ids)).all()

    # 3️⃣ Acumular km por tipo de riel
    for seg in segmentos:
        tipo = session.get(TipoRiel, seg.id_tipo_riel)
        if tipo:
            km_segmento = float(seg.km_fin - seg.km_inicio)
            km_dict[tipo.nombre] += km_segmento

    # 4️⃣ Convertir a lista de diccionarios y redondear
    resumen = [{"TipoRiel": k, "KmTotal": round(v, 2)} for k, v in km_dict.items()]
    return resumen