import streamlit as st
from controllers.linea_manager import LineaManager
from controllers.db import session


def sidebar():
    manager = LineaManager(session)
    lineas = manager.obtener_lineas()
    nombres_e_id = {linea['nombre']: linea['id'] for linea in lineas}
    nombres = list(nombres_e_id.keys())
    opcion = st.sidebar.selectbox(
        "Seleccionar una línea: ",
        nombres
    )

    opcion_id = nombres_e_id[opcion]

    return opcion, opcion_id