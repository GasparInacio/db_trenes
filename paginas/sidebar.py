import streamlit as st
from controllers.linea_manager import LineaManager
from controllers.db import session
from utils.agregar_linea_section import agregar_linea_section


def sidebar():
    linea_manager = LineaManager(session)
    lineas = linea_manager.obtener_lineas()
    nombres_e_id = {linea['nombre']: linea['id'] for linea in lineas}
    nombres = list(nombres_e_id.keys()) + ['Agregar datos']
    opcion = st.sidebar.selectbox(
        "",
        nombres
    )
    if opcion == 'Agregar datos':
         agregar_linea_section(manager=linea_manager)
    else:
        opcion_id = nombres_e_id[opcion]

        return opcion, opcion_id