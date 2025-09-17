from modelos import Linea
from db import session

# Crear algunas líneas manualmente
lines = [
    Linea(nombre="Linea Roca"),
    Linea(nombre="Linea Sarmiento"),
    Linea(nombre="Linea San Martin"),
    Linea(nombre="Linea Mitre"),
]

# Insertar solo si la tabla está vacía
if not session.query(Linea).first():
    session.add_all(lines)
    session.commit()
    print("Líneas insertadas.")
else:
    print("Ya existen líneas en la base.")
