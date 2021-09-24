from sqlalchemy import Column, Integer, Float, String, Date, ARRAY, ForeignKey

from utils.bdd import Base
class Missions(Base):
    __tablename__ = 'tb_ai_missions'

    id_mission = Column(Integer, primary_key=True, autoincrement=True)
    intitule_mission = Column(String)
    type_mission = Column(String)
    annee = Column(Integer)
    date_debut = Column(Date)
    date_fin = Column(Date)
    nbre_jhreel = Column(Integer)
    nbre_jhprevu = Column(Integer)
    responsable = Column(Integer)
    auditeurs = Column(ARRAY(Integer))
    impact = Column(Integer)
    gravite = Column(Integer)
    taux_cim_teste = Column(Float)
    commentaires = Column(String)
    id_entite = Column(Integer, ForeignKey('tb_ai_entites.id_entite'))

    colonnes = {
                "id_mission":id_mission,"intitule_mission":intitule_mission,"type_mission":type_mission,
                "annee":annee,"date_debut":date_debut,"date_fin":date_fin,"nbre_jhreel":nbre_jhreel,
                "nbre_jhprevu":nbre_jhprevu,"responsable":responsable,"auditeurs":auditeurs,"impact":impact,
                "gravite":gravite,"taux_cim_teste":taux_cim_teste,"commentaires":commentaires,
                "id_entite":id_entite
                }
    def __init__(self, colonnes):
        for attr_name, attr_value in colonnes.items():
            setattr(self, attr_name, attr_value)
   