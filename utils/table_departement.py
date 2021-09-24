from sqlalchemy import Column, String, Integer, Boolean
from utils.bdd import Base
from flask_login import UserMixin


class Departements(UserMixin, Base):
    __tablename__ = 'tb_ai_departements'

    id_departement = Column(Integer, primary_key=True, autoincrement=True)
    departement = Column(String)
    is_active = Column(Boolean, default=True)
    responsable_departement = Column(Integer, nullable=True, unique=True)

    colonnes = {
        "id_departement": id_departement, "departement": departement, "is_active": is_active,
        "responsable_departement": responsable_departement,
    }

    def __init__(self, colonnes):
        for attr_name, attr_value in colonnes.items():
            setattr(self, attr_name, attr_value)
