from modelos.estacion import Estacion


class EstacionManager:
    def __init__(self, session, id_ramal, id_linea):

        self.session = session
        self.id_ramal = id_ramal

    def mostrar_estaciones_por_ramal(self):

        estaciones = (self.session.query(Estacion).filter_by(id_ramal=self.id_ramal).all())

        return [e.to_dict() for e in estaciones]

    def agregar_estacion(self, nombre, km_inicio, km_fin):
        if not self.session.query(Estacion).filter_by(nombre=nombre, id_ramal=self.id_ramal).first():
            nueva_estacion = Estacion(nombre=nombre, kilometro_inicio=km_inicio, kilometro_fin=km_fin,
                                      id_ramal=self.id_ramal)
            try:
                self.session.add(nueva_estacion)
                self.session.commit()
                return nueva_estacion.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None
