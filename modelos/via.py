from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class Via(Base):
    __tablename__ = 'via'
    id = Column(Integer, primary_key=True)
    id_ramal = Column(Integer, ForeignKey('ramal.id'), nullable=False)
    id_sentido = Column(Integer, ForeignKey('sentido.id'), nullable=False)
    numero = Column(Integer, nullable=False)

    ramal = relationship("Ramal", back_populates="vias")
    sentido_obj = relationship("Sentido", back_populates="vias")
    tramos = relationship("Tramo", back_populates="via_obj")
    segmentos = relationship("ViaSegmento", back_populates="via")

    def to_dict(self):
        return {
            'id': self.id,
            'id_ramal': self.id_ramal,
            'id_sentido': self.id_sentido,
            'numero': self.numero,
        }