from db import session
from modelos import Linea, Ramal

linea_roca = session.query(Linea).filter_by(nombre="Linea Roca").first()

ramales = ['Constitucion - La Plata', 'Constitucion - Temperley', 'Temperley - Ezeiza', 'Ezeiza - Cañuelas', 'Temperley - Korn', 'Bosques via Quilmes', 'Bosques via Temperley']

for nombre in ramales:
    ramal = Ramal(
        id_linea=linea_roca.id,
        nombre=nombre,
        descripcion=None
    )
    session.add(ramal)

session.commit()
print("Ramales de Línea Roca agregados.")



