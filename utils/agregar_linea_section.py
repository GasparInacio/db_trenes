import streamlit as st

def agregar_linea_section(manager):
    st.write('Agregar Línea')
    nombre_linea = st.text_input('Nombre de la linea')
    descripcion_linea = st.text_input('Descripción de la linea')
    if st.button('Agregar línea'):
        nueva_linea = manager.agregar_linea(nombre=nombre_linea, descripcion=descripcion_linea)
        if nueva_linea:
            st.success(f"Línea '{nombre_linea}' agregada con éxito")
            st.rerun()
    return None, None