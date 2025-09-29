from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class Ramal(Base):
    __tablename__ = "ramal"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    id_linea = Column(Integer, ForeignKey('linea.id'), nullable=False)

    linea = relationship("Linea", back_populates="ramales")
    tramos = relationship("Tramo", back_populates="ramal")
    vias = relationship("Via", back_populates="ramal")
    estacions = relationship("Estacion", back_populates="ramal")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "id_linea": self.id_linea,
        }
