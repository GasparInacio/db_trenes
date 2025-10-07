from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()

engine = create_engine("sqlite:///ferro.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():

    from modelos.linea import Linea
    from modelos.ramal import Ramal
    from modelos.estacion import Estacion
    from modelos.via import Via
    from modelos.sentido import Sentido
    from modelos.tramo import Tramo
    from modelos.via_segmento import ViaSegmento
    from modelos.tipo_riel import TipoRiel


    Base.metadata.create_all(engine)

