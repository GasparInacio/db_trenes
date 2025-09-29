from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class Estacion(Base):
    __tablename__ = 'estacion'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    kilometro_inicio = Column(Float, nullable=False)
    kilometro_fin = Column(Float, nullable=False)
    id_ramal = Column(Integer, ForeignKey('ramal.id'))

    tramos_origen = relationship("Tramo", back_populates="estacion_origen", foreign_keys='Tramo.estacion_origen_id')
    tramos_destino = relationship("Tramo", back_populates="estacion_destino", foreign_keys='Tramo.estacion_destino_id')
    ramal = relationship('Ramal', back_populates='estaciones')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'kilometro_inicio': self.kilometro_inicio,
            'kilometro_fin': self.kilometro_fin,
        }