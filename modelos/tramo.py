from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class Tramo(Base):
    __tablename__ = 'tramo'
    id = Column(Integer, primary_key=True)
    id_ramal = Column(Integer, ForeignKey('ramal.id'), nullable=False)
    estacion_origen_id = Column(Integer, ForeignKey('estacion.id'), nullable=False)
    estacion_destino_id = Column(Integer, ForeignKey('estacion.id'), nullable=False)
    km_inicio = Column(Float, nullable=False)
    km_fin = Column(Float, nullable=False)
    id_via = Column(Integer, ForeignKey('via.id'), nullable=False)

    ramal = relationship("Ramal", back_populates="tramos")
    via_obj = relationship("Via", back_populates="tramos")
    estacion_origen = relationship("Estacion", foreign_keys=[estacion_origen_id], back_populates="tramos_origen")
    estacion_destino = relationship("Estacion", foreign_keys=[estacion_destino_id], back_populates="tramos_destino")

    def to_dict(self):
        return {
            'id': self.id,
            'id_ramal': self.id_ramal,
            'id_via': self.id_via,
            'estacion_origen': self.estacion_origen,
            'estacion_destino': self.estacion_destino,
            'km_inicio': self.km_inicio,
            'km_fin': self.km_fin
        }