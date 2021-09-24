from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from utils.bdd import Base


class Entites(Base):
    __tablename__ = 'tb_ai_entites'

    id_entite = Column(Integer, primary_key=True, autoincrement=True)
    entite = Column(String)
    # code_permanant = Column(String)
    # code_temporaire = Column(String)
    # date_debut = Column(DateTime)
    # date_fin = Column(DateTime)
    is_active = Column(Boolean)
    responsable_service = Column(Integer, nullable=True, unique=True)
    id_departement = Column(Integer, ForeignKey('tb_ai_departements.id_departement'))

    colonnes = {
        "id_entite": id_entite, "entite": entite, "is_active": is_active,
        "responsable_service": responsable_service, "id_departement": id_departement
    }

    def __init__(self, colonnes):
        for attr_name, attr_value in colonnes.items():
            setattr(self, attr_name, attr_value)
