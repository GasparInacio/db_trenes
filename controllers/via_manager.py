from modelos.via import Via

class ViaManager:
    def __init__(self, session, id_ramal):

        self.session = session
        self.id_ramal = id_ramal

    def mostrar_vias(self):
        vias = self.session.query(Via).filter_by(id_ramal=self.id_ramal).all()
        return [v.to_dict() for v in vias]

    def agregar_via(self, id_ramal, id_sentido, numero):
        nueva_via = Via(id_ramal=self.id_ramal, id_sentido=id_sentido, numero=numero)
        if nueva_via:
            try:
                self.session.add(nueva_via)
                self.session.commit()
                return nueva_via.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None