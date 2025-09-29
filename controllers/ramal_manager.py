from modelos.ramal import Ramal

class RamalManager:
    def __init__(self, session, id_linea):

        self.session = session
        self.id_linea = id_linea

    def obtener_ramales(self, id_linea=None):
        linea = id_linea if id_linea else self.id_linea
        ramales = self.session.query(Ramal).filter(Ramal.id_linea == linea).all()
        return [ramal.to_dict() for ramal in ramales]

    def obtener_ramal(self, id):
        ramal = self.session.get(Ramal, id)
        return ramal.to_dict() if ramal else None

    def agregar_ramal(self, nombre, descripcion, id_linea):

        if not self.session.query(Ramal).filter(Ramal.nombre == nombre).first():
            nuevo_ramal = Ramal(nombre=nombre, descripcion=descripcion, id_linea=id_linea)
            try:
                self.session.add(nuevo_ramal)
                self.session.commit()
                return nuevo_ramal.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None

    def actualizar_ramal(self, id, nombre, descripcion, id_linea):

        ramal = self.session.get(Ramal, id)

        if ramal:
            if nombre:
                ramal.nombre = nombre
            if descripcion:
                ramal.descripcion = descripcion
            if id_linea:
                ramal.id_linea = id_linea
            try:
                self.session.commit()
                return ramal.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None

    def eliminar_ramal(self, id):
        ramal = self.session.get(Ramal, id)
        if ramal:
            try:
                self.session.delete(ramal)
                self.session.commit()
                return True
            except Exception as e:
                self.session.rollback()
                print(e)
                return False
        return False