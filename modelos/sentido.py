from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class Sentido(Base):
    __tablename__ = 'sentido'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)

    vias = relationship("Via", back_populates="sentido_obj")

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }