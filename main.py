import streamlit as st
from paginas.sidebar import sidebar
from paginas.template import PaginaTemplate
from controllers.ramal_manager import RamalManager
from controllers.db import session, init_db

init_db()

session = session
try:
    nombre, id_linea = sidebar()
    ramal_manager = RamalManager(session=session, id_linea=id_linea)
    template = PaginaTemplate(id_linea=id_linea, manager_ramal=ramal_manager)
except Exception as e:
    st.warning('No se encontraron Líneas')

