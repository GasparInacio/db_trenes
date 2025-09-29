from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class Linea(Base):
    __tablename__ = "linea"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)

    ramales = relationship("Ramal", back_populates="linea")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion
        }