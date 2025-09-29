from modelos.tramo import Tramo

class TramoManager:
    def __init__(self, session, id_ramal):

        self.session = session
        self.id_ramal = id_ramal

    def mostrar_tramos(self):
        tramos = self.session.query(Tramo).filter_by(id_ramal=self.id_ramal).all()
        return [t.to_dict() for t in tramos]

    def agregar_tramo(self, estacion_origen_id, estacion_destino_id, id_via, km_inicio, km_fin):
        if not self.session.query(Tramo).filter_by(id_ramal=self.id_ramal, estacion_origen_id=estacion_origen_id, estacion_destino_id=estacion_destino_id, id_via=id_via).first():

            nuevo_tramo = Tramo(
                id_ramal=self.id_ramal,
                estacion_origen_id=estacion_origen_id,
                estacion_destino_id=estacion_destino_id,
                id_via=id_via,
                km_inicio=km_inicio,
                km_fin=km_fin
            )

            try:
                self.session.add(nuevo_tramo)
                self.session.commit()
                return nuevo_tramo.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None