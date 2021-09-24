from utils.table_entite import Entites
from utils.tb_ai.table_statut import Statut
from utils.tb_ai.table_auditeurs import Auditeurs

from utils.tb_ai.table_missions import Missions
from utils.tb_ai.table_suivi_activites import SuiviActivites
from utils.tb_ai.table_rapport import Rapports
import csv

from datetime import datetime

from utils.bdd import Sessionalchemy, engine, Base

Sessionalchemy = Sessionalchemy()
chef = "Chef de service"
comp = "COMP"
cnce = "CNCE"
it = "IT"


def check(a):
    if not a:
        a = None
    else:
        a = a.strip().replace('\r\n', '<br>')
    return a


def checkbool(a):
    if a == "true":
        a = True
    else:
        a = False
    return a


try:
    ######################################## TABLE ROLES ET USER #############################
    if Sessionalchemy.query(Entites).count() == 0:
        entite_all = [Entites("AI", "ai2021", None, None, None), Entites("AIGP", "aigp2021", None, None, None),
                      Entites("AISEO", "aiseo2021", None, None, None), Entites("AISUP", "aisup2021", None, None, None),
                      Entites("AITN", "aitn2021", None, None, None), Entites("COPE", "cope2021", None, None, None),
                      Entites("ANALYTICS", "di2021", None, None, None)
                      ]
        Sessionalchemy.add_all(entite_all)
        Sessionalchemy.commit()

    if Sessionalchemy.query(Statut).count() == 0:
        phases_all = [Statut("Non démarré"), Statut("En cours"), Statut("Terminé")]
        Sessionalchemy.add_all(phases_all)
        Sessionalchemy.commit()

    if Sessionalchemy.query(Auditeurs).count() == 0:
        csvfile = open("ressources/diplomes.csv", 'r', encoding='utf-8', errors='ignore')
        csvReader = csv.reader(csvfile, delimiter=";")
        data = list()
        i = 0
        j = 0
        for col in csvReader:
            j = j + 1
            if j != 1:
                colonnes = {
                    "nom_auditeur": check(col[i]), "fonction": check(col[i + 2]), "statut": check(col[i + 1]),
                    "activite": checkbool(col[i + 3]), "nbre_jour_formation": check(col[i + 4]),
                    "promotion": check(col[i + 5]),
                    "date_entree": check(col[i + 6]), "date_sortie": check(col[i + 7]), "diplomes": check(col[i + 8]),
                    "certifications": check(col[i + 9]), "id_entite": check(col[i + 10])
                }
                auditeur_all = Auditeurs(colonnes)
                Sessionalchemy.add(auditeur_all)
                Sessionalchemy.commit()

    """ if Sessionalchemy.query(Thematiques).count() == 0:
        thematique_all = [  Thematiques("Development and Personal Commitment Skills"), 
                            Thematiques("Business understanding"),
                            Thematiques("Results orientation & customer centric"), 
                            Thematiques("Audit, Risk and Control Knowledge & Skills"), 
                            Thematiques("Stakeholder Partnering Skills"), 
                            Thematiques("English")
                        ]
        Sessionalchemy.add_all(thematique_all)
        Sessionalchemy.commit()

    if Sessionalchemy.query(Competences).count() == 0:
        competence_all = [  Competences("Coaching",comp,1), 
                            Competences("Adapdativité",comp,1),
                            Competences("Développement personnel",comp,1), 
                            Competences("Ethique",comp,1), 
                            Competences("Connaissance de l'organisation",cnce,2), 
                            Competences("Juridique et réglementaire",cnce,2)
                        ]
        Sessionalchemy.add_all(competence_all)
        Sessionalchemy.commit() """

    if Sessionalchemy.query(Missions).count() == 0:
        csvfile = open("ressources/missions_all.csv", 'r', encoding='utf-8', errors='ignore')
        csvReader = csv.reader(csvfile, delimiter=";")
        data = list()
        i = 0
        j = 0
        for col in csvReader:
            j = j + 1
            if j != 1:
                if col[i + 8] != "":
                    audi = set([int(val) for val in col[i + 8].split(",")])
                else:
                    audi = []
                colonnes = {"intitule_mission": col[i], "date_debut": check(col[i + 2]),
                            "date_fin": check(col[i + 3]), "nbre_jhreel": check(col[i + 4]),
                            "nbre_jhprevu": check(col[i + 5]),
                            "responsable": col[i + 7], "auditeurs": audi, "impact": None, "gravite": None,
                            "taux_cim_teste": None, "commentaires": check(col[i + 9]), "id_entite": col[i + 10]
                            }

                missions = Missions(colonnes)
                Sessionalchemy.add(missions)
                Sessionalchemy.commit()

                table_suivi = SuiviActivites(col[i + 1], None, None, None, col[i + 11], j - 1)
                Sessionalchemy.add(table_suivi)
                Sessionalchemy.commit()

                table_rapport = Rapports(None, None, None, None, datetime.now(), j - 1)
                Sessionalchemy.add(table_rapport)
                Sessionalchemy.commit()

except (Exception) as error:
    pass
