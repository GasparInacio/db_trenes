from modelos.tipo_riel import TipoRiel

class TipoRielManager:
    def __init__(self, session):

        self.session = session

    def mostrar_tipos_de_riel(self):

        try:
            tipos_riel = self.session.query(TipoRiel).all()
            return [riel.to_dict() for riel in tipos_riel]
        except Exception as e:
            print(e)
            return None

    def mostrar_riel(self, id):
        try:
            riel = self.session.get(TipoRiel, id)
            return riel.to_dict()
        except Exception as e:
            print(e)
            return None

    def agregar_riel(self, nombre):
        nuevo_riel = TipoRiel(nombre=nombre)
        try:
            self.session.add(nuevo_riel)
            self.session.commit()
            return nuevo_riel.to_dict()
        except Exception as e:
            self.session.rollback()
            print(e)
            return None
