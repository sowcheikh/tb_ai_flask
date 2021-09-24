from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from utils.bdd import Base

class Rapports(Base):
    __tablename__ = 'tb_ai_rapports'

    id_rapport = Column(Integer, primary_key=True, autoincrement=True)
    constats = Column(String)
    causes = Column(String)
    recommandations = Column(String)
    rapport = Column(String)
    date = Column(DateTime)
    id_mission = Column(Integer, ForeignKey('tb_ai_missions.id_mission'))

    def __init__(self, constats, causes, recommandations, rapport, date, id_mission):
        self.constats = constats
        self.causes = causes
        self.recommandations = recommandations
        self.rapport = rapport
        self.date = date
        self.id_mission = id_mission
   