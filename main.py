import streamlit as st
import pandas as pd
from db import session
from utils import estaciones_por_linea_ramal, ramales_de_linea, tramos_tipo_riel, cantidad_km_tipo_riel

opcion = st.sidebar.selectbox(
    "Líneas:",
    ["Línea Roca", "Línea San Martín", "Linea Mitre", "Línea Sarmiento"]
)

if opcion == "Línea Roca":
    st.header("Línea Roca")
    st.write("Datos")

    id_linea = 1

    ramales = ramales_de_linea(session, id_linea)

    seleccion_ramal = st.selectbox(
        "Seleccione la ramal",
        [r.nombre for r in ramales]
    )

    ramal_obj = next(r for r in ramales if r.nombre == seleccion_ramal)

    estaciones = estaciones_por_linea_ramal(session, id_linea=id_linea, id_ramal=ramal_obj.id)

    if not estaciones:
        st.warning("No se encontraron estaciones")
    else:
        seleccion_estacion = st.selectbox(
            "Seleccione la estacion",
            [e.nombre for e in estaciones]
        )

    df = tramos_tipo_riel(session, id_ramal=ramal_obj.id)

    if df.empty:
        st.info("No hay datos de riel para este ramal.")
    else:
        st.dataframe(df, use_container_width=True)

    resumen = cantidad_km_tipo_riel(session, id_ramal=ramal_obj.id)

    if resumen:
        df = pd.DataFrame(resumen)
        st.table(df)
    else:
        st.warning("No hay datos de riel para este ramal.")

elif opcion == "Línea San Martín":
    st.header("Línea San Martín")
    st.write("Datos")

elif opcion == "Linea Mitre":
    st.header("Línea Mitre")
    st.write("Datos")

elif opcion == "Línea Sarmiento":
    st.header("Línea Línea Sarmiento")
    st.write("Datos")