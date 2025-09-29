from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class TipoRiel(Base):
    __tablename__ = "tipo_riel"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)

    segmentos = relationship("ViaSegmento", back_populates="tipo_riel")

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }