from modelos.via_segmento import ViaSegmento

class ViaSegmentoManager:
    def __init__(self, session):

        self.session = session

    def mostrar_segmentos(self, id_via=None):
        if id_via:
            try:
                segmentos = self.session.query(ViaSegmento).filter_by(id_via=id_via).all()
                return [seg.to_dict() for seg in segmentos]
            except Exception as e:
                print(e)
                return None
        else:
            return None

    def mostrar_segmento(self, id):
        segmento = self.session.get(ViaSegmento, id)
        return segmento.to_dict() if segmento else None

    def agregar_segmento(self, id_via, km_inicio, km_fin, id_tipo_riel):
        nuevo_segmento = ViaSegmento(id_via=id_via, km_inicio=km_inicio, km_fin=km_fin, id_tipo_riel=id_tipo_riel)

        try:
            self.session.add(nuevo_segmento)
            self.session.commit()
            return nuevo_segmento.to_dict()
        except Exception as e:
            self.session.rollback()
            print(e)
            return None

