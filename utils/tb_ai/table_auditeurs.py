from sqlalchemy import Column, String, Boolean, Integer, Date, ForeignKey
from utils.bdd import Base
from flask_login import UserMixin


class Auditeurs(UserMixin, Base):
    __tablename__ = 'tb_ai_auditeurs'

    id_auditeur = Column(Integer, primary_key=True, autoincrement=True)
    nom_auditeur = Column(String)
    login = Column(String, unique=True)
    methode = Column(String, default="LDAP")
    password = Column(String)
    is_active = Column(Boolean, default=True)
    statut = Column(String)
    activite = Column(Boolean, default=True)

    nbre_jour_formation = Column(String)
    promotion = Column(Date)
    date_entree = Column(Date)
    date_sortie = Column(Date)
    diplomes = Column(String)
    certifications = Column(String)
    id_entite = Column(Integer, ForeignKey('tb_ai_entites.id_entite'))
    id_departement = Column(Integer, ForeignKey('tb_ai_departements.id_departement'))
    fonction = Column(Integer, ForeignKey('tb_ai_fonctions.id_fonction'))

    colonnes = {
        "id_auditeur": id_auditeur, "nom_auditeur": nom_auditeur, "login": login, "statut": statut,
        "password": password, "is_active": is_active, "fonction": fonction, "methode": methode,
        "activite": activite, "nbre_jour_formation": nbre_jour_formation,
        "promotion": promotion, "date_entree": date_entree, "date_sortie": date_sortie,
        "diplomes": diplomes, "certifications": certifications, "id_entite": id_entite,
    }

    def get_id(self):
        return self.id_auditeur

    def __init__(self, colonnes):
        for attr_name, attr_value in colonnes.items():
            setattr(self, attr_name, attr_value)
