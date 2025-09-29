from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base
from controllers.db import Base

class ViaSegmento(Base):
    __tablename__ = "via_segmento"
    id = Column(Integer, primary_key=True)
    id_via = Column(Integer, ForeignKey("via.id"), nullable=False)
    km_inicio = Column(Float, nullable=False)
    km_fin = Column(Float, nullable=False)
    id_tipo_riel = Column(Integer, ForeignKey("tipo_riel.id"), nullable=False)

    via = relationship("Via", back_populates="segmentos")
    tipo_riel = relationship("TipoRiel", back_populates="segmentos")

    def to_dict(self):
        return {
            'id': self.id,
            'id_via': self.id_via,
            'km_inicio': self.km_inicio,
            'km_fin': self.km_fin,
            'id_tipo_riel': self.id_tipo_riel,
        }