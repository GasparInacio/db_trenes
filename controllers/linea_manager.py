from modelos.linea import Linea

class LineaManager:
    def __init__(self, session):

        self.session = session

    def obtener_lineas(self):
        lineas = self.session.query(Linea).all()
        lineas_dict = [linea.to_dict() for linea in lineas]
        return lineas_dict


    def obtener_linea(self, id):
        linea = self.session.get(Linea, id)
        return linea.to_dict() if linea else None

    def agregar_linea(self, nombre, descripcion):

        if not self.session.query(Linea).filter_by(nombre=nombre).first():
            nueva_linea = Linea(nombre=nombre, descripcion=descripcion)
            try:
                self.session.add(nueva_linea)
                self.session.commit()
                return nueva_linea.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None

    def actualizar_linea(self, id, nombre, descripcion):

        linea = self.session.get(Linea, id)

        if linea:
            if nombre:
                linea.nombre = nombre
            if descripcion:
                linea.descripcion = descripcion
            try:
                self.session.commit()
                return linea.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None

    def eliminar_linea(self, id):

        linea = self.session.get(Linea, id)
        if linea:
            try:
                self.session.delete(linea)
                self.session.commit()
                return True
            except Exception as e:
                self.session.rollback()
                print(e)
                return False
        return False




