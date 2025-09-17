from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Linea(Base):
    __tablename__ = "linea"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)

    ramales = relationship("Ramal", back_populates="linea")

class Ramal(Base):
    __tablename__ = "ramal"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    id_linea = Column(Integer, ForeignKey('linea.id'), nullable=False)

    linea = relationship("Linea", back_populates="ramales")
    tramos = relationship("Tramo", back_populates="ramal")
    vias = relationship("Via", back_populates="ramal")


class Estacion(Base):
    __tablename__ = 'estacion'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    kilometro_inicio = Column(Float, nullable=False)
    kilometro_fin = Column(Float, nullable=False)

    tramos_origen = relationship("Tramo", back_populates="estacion_origen", foreign_keys='Tramo.estacion_origen_id')
    tramos_destino = relationship("Tramo", back_populates="estacion_destino", foreign_keys='Tramo.estacion_destino_id')

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

class Sentido(Base):
    __tablename__ = 'sentido'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)

    vias = relationship("Via", back_populates="sentido_obj")

class TipoRiel(Base):
    __tablename__ = "tipo_riel"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)

    segmentos = relationship("ViaSegmento", back_populates="tipo_riel")


class ViaSegmento(Base):
    __tablename__ = "via_segmento"
    id = Column(Integer, primary_key=True)
    id_via = Column(Integer, ForeignKey("via.id"), nullable=False)
    km_inicio = Column(Float, nullable=False)
    km_fin = Column(Float, nullable=False)
    id_tipo_riel = Column(Integer, ForeignKey("tipo_riel.id"), nullable=False)

    via = relationship("Via", back_populates="segmentos")
    tipo_riel = relationship("TipoRiel", back_populates="segmentos")

