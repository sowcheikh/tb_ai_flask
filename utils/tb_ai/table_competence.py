from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from utils.bdd import Base


class Competences(Base):
    __tablename__ = 'tb_ai_competences'

    id_competence = Column(Integer, primary_key=True, autoincrement=True)
    libelle_competence = Column(String)
    comp_cnce_it = Column(String)
    is_active = Column(Boolean)
    id_thematique = Column(Integer, ForeignKey('tb_ai_thematiques.id_thematique'))

    def __init__(self, libelle_competence, comp_cnce_it, is_active, id_thematique):
        self.libelle_competence = libelle_competence
        self.comp_cnce_it = comp_cnce_it
        self.is_active = is_active
        self.id_thematique = id_thematique
