from sqlalchemy import Column, String, Integer
from utils.bdd import Base
class Statut(Base):
    __tablename__ = 'tb_ai_statut'

    id_statut_mission = Column(Integer, primary_key=True, autoincrement=True)
    statut_mission = Column(String)
    
    def __init__(self, statut_mission):
        self.statut_mission = statut_mission
