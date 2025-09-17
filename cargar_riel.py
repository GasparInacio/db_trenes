from db import session
from modelos import Ramal, Via, TipoRiel, ViaSegmento, Sentido
import pandas as pd

ramal = session.query(Ramal).filter_by(nombre="Constitucion - La Plata").first()

df = pd.read_excel('rail/constitucion_lp_riel.xlsx')

direction_map = {
    "up": "ascendente",
    "down": "descendente"
}

for _, row in df.iterrows():
    via_raw = str(row["LineName"]).lower().strip()  # "VIA 1" -> "via 1"
    via_num = int(via_raw.replace("via", "").strip())
    s_km = float(row["sKm"])
    e_km = float(row["eKm"])
    tipo_riel_nombre = str(row["RailType"]).strip()
    direction_raw = str(row["LineDirection"]).lower().strip()
    sentido_nombre = direction_map.get(direction_raw, direction_raw)

    # --- Sentido ---
    sentido = session.query(Sentido).filter_by(nombre=sentido_nombre).first()
    if not sentido:
        sentido = Sentido(nombre=sentido_nombre)
        session.add(sentido)
        session.flush()

    # --- TipoRiel ---
    tipo_riel = session.query(TipoRiel).filter_by(nombre=tipo_riel_nombre).first()
    if not tipo_riel:
        tipo_riel = TipoRiel(nombre=tipo_riel_nombre)
        session.add(tipo_riel)
        session.flush()

    # --- Via ---
    via = (
        session.query(Via)
        .filter_by(id_ramal=ramal.id, numero=via_num, id_sentido=sentido.id)
        .first()
    )
    if not via:
        via = Via(id_ramal=ramal.id, numero=via_num, id_sentido=sentido.id)
        session.add(via)
        session.flush()

    # --- ViaSegmento ---
    segmento = ViaSegmento(
        id_via=via.id,
        km_inicio=s_km,
        km_fin=e_km,
        id_tipo_riel=tipo_riel.id
    )
    session.add(segmento)

# 5. Guardamos todo
session.commit()