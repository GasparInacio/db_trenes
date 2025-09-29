import streamlit as st
from controllers.ramal_manager import RamalManager

class PaginaTemplate:
    def __init__(self, id_linea, manager_linea, manager_ramal: RamalManager):
        self.id_linea = id_linea
        self.manager_linea = manager_linea
        self.manager_ramal = manager_ramal
        self.linea = self.manager_linea.obtener_linea(self.id_linea)
        self.ramales = self.manager_ramal.obtener_ramales(id_linea=self.id_linea)

    def header(self):
        linea = self.linea
        if linea:
            st.header(linea['nombre'])
            st.write('Datos')
        else:
            st.warning('No se pudo encontrar la línea')

    def body(self):
        ramales = self.ramales
        if ramales:
            nombres_e_id = {ramal['nombre']: ramal['id'] for ramal in ramales}
            nombres = list(nombres_e_id.keys())
            seleccion_ramal = st.selectbox(
                "Seleccione el ramal",
                nombres
            )

            seleccion_id = nombres_e_id[seleccion_ramal]

            ramal_seleccionado = next(r for r in self.ramales if r['id'] == seleccion_id)

            return ramal_seleccionado
        else:
            st.warning('No se pudo encontrar el ramal')
            return None




