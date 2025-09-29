from controllers.db import session
from modelos import Linea, Ramal

# Línea de referencia
linea_roca = session.query(Linea).filter_by(nombre="Linea Roca").first()

# Ramales a cargar
ramales = ['Constitucion - La Plata', 'Constitucion - Temperley', 'Temperley - Ezeiza', 'Ezeiza - Cañuelas', 'Temperley - Korn', 'Bosques via Quilmes', 'Bosques via Temperley']

# Carga de los ramales
for nombre in ramales:
    ramal = Ramal(
        id_linea=linea_roca.id,
        nombre=nombre,
        descripcion=None
    )
    session.add(ramal)

session.commit()
print("Ramales de Línea Roca agregados.")



