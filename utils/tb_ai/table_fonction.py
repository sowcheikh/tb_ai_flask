from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from utils.bdd import Base


class Fonctions(Base):
    __tablename__ = 'tb_ai_fonctions'

    id_fonction = Column(Integer, primary_key=True, autoincrement=True)
    libelle = Column(String)
    is_active = Column(Boolean, default=True)

    def __init__(self, libelle):
        self.libelle = libelle
