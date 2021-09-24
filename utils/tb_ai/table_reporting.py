from sqlalchemy import Column, Integer, String, ForeignKey

from utils.bdd import Base
class ReportingCodir(Base):
    __tablename__ = 'tb_ai_reporting_codir'

    id_reporting_codir = Column(Integer, primary_key=True, autoincrement=True)
    semaine = Column(String)
    fonctionne = Column(String)
    point_coordination = Column(String)
    difficultes = Column(String)
    id_entite = Column(Integer, ForeignKey('tb_ai_entites.id_entite'))

    def __init__(self, semaine, fonctionne, point_coordination, difficultes, id_entite):
        self.semaine = semaine
        self.fonctionne = fonctionne
        self.point_coordination = point_coordination
        self.difficultes = difficultes
        self.id_entite = id_entite