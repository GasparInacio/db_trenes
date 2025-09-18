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
        df = pd.DataFrame()  # dataframe vacío
    else:
        seleccion_estacion1 = st.selectbox(
            "Seleccione la estación de origen",
            [e.nombre for e in estaciones],
            key="estacion_origen"
        )

        seleccion_estacion2 = st.selectbox(
            "Seleccione la estación de destino",
            [e.nombre for e in estaciones],
            key="estacion_destino"
        )

        if seleccion_estacion1 == seleccion_estacion2:
            st.error("La estación de origen y destino no pueden ser la misma.")
            df = pd.DataFrame()
        else:
            df = tramos_tipo_riel(
                session,
                id_ramal=ramal_obj.id,
                estacion_origen=seleccion_estacion1,
                estacion_destino=seleccion_estacion2
            )

            if not df.empty:
                st.dataframe(df)

    df = cantidad_km_tipo_riel(
        session,
        id_ramal=ramal_obj.id,
        estacion_origen=seleccion_estacion1,
        estacion_destino=seleccion_estacion2
    )

    if not df.empty:
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