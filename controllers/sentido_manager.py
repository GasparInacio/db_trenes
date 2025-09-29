from modelos.sentido import Sentido

class SentidoManager:
    def __init__(self, session):

        self.session = session

    def agregar_sentido(self, nombre):

        sentido = self.session.query(Sentido).filter_by(nombre=nombre).first()

        if not sentido:
            try:
                sentido = Sentido(nombre=nombre)
                self.session.add(sentido)
                self.session.commit()
                self.session.flush()
                return sentido.to_dict()
            except Exception as e:
                self.session.rollback()
                print(e)
                return None
        return None