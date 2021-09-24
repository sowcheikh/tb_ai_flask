from sqlalchemy import Column, Integer, String, ForeignKey

from utils.bdd import Base

class SuiviActivites(Base):
    __tablename__ = 'tb_ai_suivi_activites'

    id_suivi_activite = Column(Integer, primary_key=True, autoincrement=True)
    semaine = Column(String)
    fait = Column(String)
    reste_faire = Column(String)
    difficultes = Column(String)
    id_statut_mission = Column(Integer, ForeignKey('tb_ai_statut.id_statut_mission'))
    id_mission = Column(Integer, ForeignKey('tb_ai_missions.id_mission'))


    def __init__(self, semaine, fait, reste_faire, difficultes, id_statut_mission,id_mission):
        self.semaine = semaine
        self.fait = fait
        self.reste_faire = reste_faire
        self.difficultes = difficultes
        self.id_statut_mission = id_statut_mission
        self.id_mission = id_mission