from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from utils.bdd import Base


class Notation(Base):
    __tablename__ = 'tb_ai_notation'

    id_notation = Column(Integer, primary_key=True, autoincrement=True)
    note = Column(Integer)
    periode = Column(Date)
    id_auditeur = Column(Integer, ForeignKey('tb_ai_auditeurs.id_auditeur'))
    id_competence = Column(Integer, ForeignKey('tb_ai_competences.id_competence'))

    def __init__(self, note, periode, id_auditeur, id_competence):
        self.note = note
        self.periode = periode
        self.id_auditeur = id_auditeur
        self.id_competence = id_competence
