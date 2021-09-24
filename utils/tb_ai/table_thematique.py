from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from utils.bdd import Base
class Thematiques(Base):
    __tablename__ = 'tb_ai_thematiques'

    id_thematique = Column(Integer, primary_key=True, autoincrement=True)
    libelle_thematique = Column(String)
    is_active = Column(Boolean)

    def __init__(self, libelle_thematique, is_active):
        self.libelle_thematique = libelle_thematique
        self.is_active = is_active
