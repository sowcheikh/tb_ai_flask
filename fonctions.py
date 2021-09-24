from functools import wraps
from flask import redirect, url_for, jsonify
from flask_login import current_user
from datetime import date, timedelta
import os
import numpy as np
from sqlalchemy import func, and_, desc, cast, Date
from werkzeug.utils import secure_filename

from utils.bdd import Sessionalchemy
from utils.table_departement import Departements
from utils.tb_ai.table_competence import Competences
from utils.tb_ai.table_fonction import Fonctions
from utils.tb_ai.table_notation import Notation

from utils.tb_ai.table_suivi_activites import SuiviActivites
from utils.table_entite import Entites
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_statut import Statut
from utils.tb_ai.table_missions import Missions
from utils.tb_ai.table_reporting import ReportingCodir
from utils.tb_ai.table_rapport import Rapports
from datetime import datetime

from utils.tb_ai.table_thematique import Thematiques

Sessionalchemy = Sessionalchemy()
dossier_image = "static/assets/data/rapports/"
dossier_doc = "dossiers/"


def check(a):
    if not a:
        a = None
    return a


def access_entite_admin(access_level: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_fonction_by_ID() in access_level:
                return func(*args, **kwargs)
            elif get_fonction_by_ID() == "Admin":
                return redirect(url_for('admin_dep.liste_departement'))
            else:
                return redirect(url_for('cr.suivi_by_cr'))

        return wrapper

    return decorator


def access_entite_ai(access_level: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_fonction_by_ID() in access_level:
                return func(*args, **kwargs)
            elif get_fonction_by_ID() == "Chef de département":
                return redirect(url_for('mission.liste_mission'))
            else:
                return redirect(url_for('cr.suivi_by_cr'))

        return wrapper

    return decorator


def access_entite_cr(access_level: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if get_fonction_by_ID() in access_level:
                return func(*args, **kwargs)
            elif get_fonction_by_ID() == "Chef de service":
                return redirect(url_for('cr.suivi_by_cr'))
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def liste_suivi_activite_all():
    jour = datetime.now().strftime('%a')
    if jour == "Fri" or jour == "Sat" or jour == "Sun":
        semaine = date_semaine_suivante(datetime.now())
    else:
        semaine = date_semaine(datetime.now())

    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(Entites.id_departement == current_user.id_departement) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(SuiviActivites.semaine == semaine) \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "responsable": chef,
                             "impact": mis.impact, "gravite": mis.gravite, "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission, "fait": format_line(sui.fait),
                             "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_suivi_activite_search_all(sem):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(SuiviActivites.semaine == sem) \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "responsable": chef,
                             "impact": mis.impact, "gravite": mis.gravite, "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission, "fait": format_line(sui.fait),
                             "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


#################################################LISTE MISSSION ET RECHERCHE AI#######################################
def liste_mission_max_occur():
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')

    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(Entites.id_departement == current_user.id_departement) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.type_mission == "mission") \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})
        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee, "entite": ent.entite,
                             "date_debut": mis.date_debut, "date_fin": mis.date_fin, "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "responsable": chef,
                             "impact": mis.impact, "gravite": mis.gravite, "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission, "fait": format_line(sui.fait),
                             "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search(sem):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.type_mission == "mission") \
        .filter(SuiviActivites.semaine == sem).all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee, "entite": ent.entite,
                             "date_debut": mis.date_debut, "date_fin": mis.date_fin, "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_year_search(annee):
    if annee == '':
        annee = 0
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.type_mission == "mission") \
        .filter(Missions.annee == annee) \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = []

        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        nbre_suivi = Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == mis.id_mission).count()

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee, "entite": ent.entite,
                             "date_debut": mis.date_debut,
                             "date_fin": mis.date_fin, "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "nbre_suivi": nbre_suivi,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


######################################################################################################################

#################################################LISTE ACTIVITE ET RECHERCHE AI#######################################
def liste_activite_max_occur():
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')

    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(Entites.id_departement == current_user.id_departement) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.type_mission == "activite") \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})
        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee, "entite": ent.entite,
                             "date_debut": mis.date_debut, "date_fin": mis.date_fin, "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "responsable": chef,
                             "impact": mis.impact, "gravite": mis.gravite, "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission, "fait": format_line(sui.fait),
                             "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_activite_max_occur_search(sem):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.type_mission == "activite") \
        .filter(SuiviActivites.semaine == sem).all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee, "entite": ent.entite,
                             "date_debut": mis.date_debut,
                             "date_fin": mis.date_fin, "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_activite_max_occur_year_search(annee):
    if annee == '':
        annee = 0
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.type_mission == "activite") \
        .filter(Missions.annee == annee) \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = []

        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        nbre_suivi = Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == mis.id_mission).count()

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee, "entite": ent.entite,
                             "date_debut": mis.date_debut,
                             "date_fin": mis.date_fin, "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "nbre_suivi": nbre_suivi,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


#########################################################################################################

def liste_mission_max_occur_cr(ent):
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Entites.entite == ent) \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = []

        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        nbre_suivi = Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == mis.id_mission).count()

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "nbre_suivi": nbre_suivi,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search_cr(sem, ent):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(SuiviActivites.semaine == sem) \
        .filter(Entites.entite == ent).all()
    missions_all = []

    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search_cr_year(annee, ent):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.annee == annee) \
        .filter(Entites.entite == ent).all()
    missions_all = []

    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


#####################################################################################################################
#######################################################Missions CR#############################################
def liste_mission_max_occur_cr_mission(ent):
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Entites.entite == ent) \
        .filter(Missions.type_mission == "mission") \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = []

        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        nbre_suivi = Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == mis.id_mission).count()

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "nbre_suivi": nbre_suivi,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search_cr_mission(sem, ent):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(SuiviActivites.semaine == sem) \
        .filter(Missions.type_mission == "mission") \
        .filter(Entites.entite == ent).all()
    missions_all = []

    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search_cr_year_mission(annee, ent):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.annee == annee) \
        .filter(Missions.type_mission == "mission") \
        .filter(Entites.entite == ent).all()
    missions_all = []

    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


#######################################################Activités CR#############################################
def liste_mission_max_occur_cr_activite(ent):
    subquery = Sessionalchemy.query(SuiviActivites.id_mission,
                                    func.max(SuiviActivites.id_suivi_activite).label('maxID')).group_by(
        SuiviActivites.id_mission).subquery('t2')
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .join(subquery,
              and_(SuiviActivites.id_mission == subquery.c.id_mission,
                   SuiviActivites.id_suivi_activite == subquery.c.maxID
                   )
              ) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Entites.entite == ent) \
        .filter(Missions.type_mission == "activite") \
        .all()
    missions_all = []
    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = []

        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        nbre_suivi = Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == mis.id_mission).count()

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all, "nbre_suivi": nbre_suivi,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search_cr_activite(sem, ent):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(SuiviActivites.semaine == sem) \
        .filter(Missions.type_mission == "activite") \
        .filter(Entites.entite == ent).all()
    missions_all = []

    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


def liste_mission_max_occur_search_cr_year_activite(annee, ent):
    missions = Sessionalchemy.query(SuiviActivites, Missions, Statut, Entites) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(SuiviActivites.id_statut_mission == Statut.id_statut_mission) \
        .filter(SuiviActivites.id_mission == Missions.id_mission) \
        .filter(Missions.annee == annee) \
        .filter(Missions.type_mission == "activite") \
        .filter(Entites.entite == ent).all()
    missions_all = []

    for sui, mis, stat, ent in missions:
        auditeur_all = []
        chef = []
        audit = [int(val) for val in mis.auditeurs]
        for val in audit:
            auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == val).first()
            auditeur_all.append({"id_auditeur": auditeur.id_auditeur, "nom_auditeur": auditeur.nom_auditeur})

        responsable = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == mis.responsable).first()
        chef.append({"id_responsable": responsable.id_auditeur, "nom_responsable": responsable.nom_auditeur})

        missions_all.append({"id_suivi": sui.id_suivi_activite, "sem": sui.semaine, "id_mission": mis.id_mission,
                             "intitule_mission": mis.intitule_mission,
                             "type_mission": mis.type_mission, "annee": mis.annee,
                             "entite": ent.entite, "date_debut": mis.date_debut, "date_fin": mis.date_fin,
                             "nbre_jhreel": mis.nbre_jhreel,
                             "nbre_jhprevu": mis.nbre_jhprevu, "auditeurs": auditeur_all,
                             "responsable": chef, "impact": mis.impact, "gravite": mis.gravite,
                             "taux_cim_teste": mis.taux_cim_teste,
                             "commentaires": format_line(mis.commentaires), "id_statut": stat.id_statut_mission,
                             "statut_mission": stat.statut_mission,
                             "fait": format_line(sui.fait), "reste_faire": format_line(sui.reste_faire),
                             "difficultes": format_line(sui.difficultes)})
    return missions_all


###################################################REPORTING CODIR###################################################
def liste_codir_cr(ent):
    reporting_all = []
    reporting = Sessionalchemy.query(ReportingCodir).filter(ReportingCodir.id_entite == ent).order_by(
        ReportingCodir.semaine.desc()).all()
    for val in reporting:
        reporting_all.append({"id_reporting_codir": val.id_reporting_codir, "semaine": val.semaine,
                              "fonctionne": format_line(val.fonctionne),
                              "point_coordination": format_line(val.point_coordination),
                              "difficultes": format_line(val.difficultes), "id_entite": val.id_entite})
    return reporting_all


def liste_codir_cr_search(sem, ent):
    reporting_all = []
    reporting = Sessionalchemy.query(ReportingCodir) \
        .filter(ReportingCodir.semaine == sem) \
        .filter(ReportingCodir.id_entite == ent).all()
    for val in reporting:
        reporting_all.append({"id_reporting_codir": val.id_reporting_codir, "semaine": val.semaine,
                              "fonctionne": format_line(val.fonctionne),
                              "point_coordination": format_line(val.point_coordination),
                              "difficultes": format_line(val.difficultes), "id_entite": val.id_entite})
    return reporting_all


def liste_codir_ai():
    reporting_all = []
    max_sem = Sessionalchemy.query(func.max(ReportingCodir.semaine)).scalar()
    reporting = Sessionalchemy.query(ReportingCodir, Entites) \
        .filter(ReportingCodir.id_entite == Entites.id_entite) \
        .filter(ReportingCodir.semaine == max_sem) \
        .order_by(Entites.entite).all()
    for rep, ent in reporting:
        reporting_all.append({"id_reporting_codir": rep.id_reporting_codir, "semaine": rep.semaine,
                              "fonctionne": format_line(rep.fonctionne),
                              "point_coordination": format_line(rep.point_coordination),
                              "difficultes": format_line(rep.difficultes), "id_entite": rep.id_entite,
                              "entite": ent.entite})
    return reporting_all


def liste_codir_ai_search(sem):
    reporting_all = []
    reporting = Sessionalchemy.query(ReportingCodir, Entites) \
        .filter(ReportingCodir.id_entite == Entites.id_entite) \
        .filter(ReportingCodir.semaine == sem) \
        .order_by(Entites.entite).all()
    for rep, ent in reporting:
        reporting_all.append({"id_reporting_codir": rep.id_reporting_codir, "semaine": rep.semaine,
                              "fonctionne": format_line(rep.fonctionne),
                              "point_coordination": format_line(rep.point_coordination),
                              "difficultes": format_line(rep.difficultes), "id_entite": rep.id_entite,
                              "entite": ent.entite})
    return reporting_all


#########################################################################################################################################
########################################################RAPPORT##########################################################################
def liste_rapport_max_occur_ai(ent):
    rapport_all = []
    subquery = Sessionalchemy.query(Rapports.id_mission, func.max(Rapports.id_rapport).label('maxID')).group_by(
        Rapports.id_mission).subquery('t2')
    rapports = Sessionalchemy.query(Rapports, Missions, Entites) \
        .join(subquery,
              and_(Rapports.id_mission == subquery.c.id_mission,
                   Rapports.id_rapport == subquery.c.maxID
                   )
              ) \
        .filter(Rapports.id_mission == Missions.id_mission) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(Entites.entite == ent) \
        .order_by(Rapports.id_rapport.desc()) \
        .all()
    for rapp, mis, en in rapports:
        rapport_all.append(
            {"id_rapport": rapp.id_rapport, "constats": format_line(rapp.constats), "causes": format_line(rapp.causes),
             "recommandations": format_line(rapp.recommandations), "rapport": format_line(rapp.rapport),
             "date": rapp.date,
             "id_mission": mis.id_mission, "intitule_mission": format_line(mis.intitule_mission)
             })
    return rapport_all


def liste_rapport_ai_search(day, ent):
    rapport_all = []
    if day:
        rapports = Sessionalchemy.query(Rapports, Missions, Entites) \
            .filter(Rapports.id_mission == Missions.id_mission) \
            .filter(Missions.id_entite == Entites.id_entite) \
            .filter(Entites.entite == ent) \
            .filter(Rapports.date.cast(Date) == day) \
            .order_by(Rapports.id_rapport.desc()) \
            .all()
        for rapp, mis, en in rapports:
            rapport_all.append({"id_rapport": rapp.id_rapport, "constats": format_line(rapp.constats),
                                "causes": format_line(rapp.causes),
                                "recommandations": format_line(rapp.recommandations),
                                "rapport": format_line(rapp.rapport), "date": rapp.date,
                                "id_mission": mis.id_mission, "intitule_mission": format_line(mis.intitule_mission)
                                })
    return rapport_all


def liste_rapport_max_occur_cr(ent):
    rapport_all = []
    subquery = Sessionalchemy.query(Rapports.id_mission, func.max(Rapports.id_rapport).label('maxID')).group_by(
        Rapports.id_mission).subquery('t2')
    rapports = Sessionalchemy.query(Rapports, Missions, Entites) \
        .join(subquery,
              and_(Rapports.id_mission == subquery.c.id_mission,
                   Rapports.id_rapport == subquery.c.maxID
                   )
              ) \
        .filter(Rapports.id_mission == Missions.id_mission) \
        .filter(Missions.id_entite == Entites.id_entite) \
        .filter(Entites.entite == ent) \
        .order_by(Rapports.id_rapport.desc()) \
        .all()
    for rapp, mis, en in rapports:
        rapport_all.append(
            {"id_rapport": rapp.id_rapport, "constats": format_line(rapp.constats), "causes": format_line(rapp.causes),
             "recommandations": format_line(rapp.recommandations), "rapport": format_line(rapp.rapport),
             "date": rapp.date,
             "id_mission": mis.id_mission, "intitule_mission": format_line(mis.intitule_mission)
             })
    return rapport_all


def liste_rapport_cr_search(day, ent):
    rapport_all = []
    if day:
        rapports = Sessionalchemy.query(Rapports, Missions, Entites) \
            .filter(Rapports.id_mission == Missions.id_mission) \
            .filter(Missions.id_entite == Entites.id_entite) \
            .filter(Entites.entite == ent) \
            .filter(Rapports.date.cast(Date) == day) \
            .order_by(Rapports.id_rapport.desc()) \
            .all()
        for rapp, mis, en in rapports:
            rapport_all.append({"id_rapport": rapp.id_rapport, "constats": format_line(rapp.constats),
                                "causes": format_line(rapp.causes),
                                "recommandations": format_line(rapp.recommandations),
                                "rapport": format_line(rapp.rapport), "date": rapp.date,
                                "id_mission": mis.id_mission, "intitule_mission": format_line(mis.intitule_mission)
                                })
    return rapport_all


def liste_rapport_max_by_id(ent):
    sub = Sessionalchemy.query(Rapports.id_mission, func.max(Rapports.id_rapport).label("max_id")) \
        .group_by(Rapports.id_mission).subquery("t2")
    max_id_rapport = Sessionalchemy.query(Rapports, Missions, Entites) \
        .join(sub, and_(
        Rapports.id_mission == sub.c.id_mission,
        Rapports.id_rapport == sub.c.max_id)) \
        .filter(
        Rapports.id_mission == Missions.id_mission,
        Missions.id_entite == Entites.id_entite,
        Entites.entite == ent
    ).all()
    liste_max_by_id = {}
    for val, a, v in max_id_rapport:
        liste_max_by_id[val.id_mission] = val.id_rapport
    return liste_max_by_id


###############################################################################################################################
def liste_entite():
    return Sessionalchemy.query(Entites).order_by(Entites.id_entite).all()


def liste_entite_one_dep():
    return Sessionalchemy.query(Entites).order_by(Entites.id_entite) \
        .filter(Entites.id_departement == Departements.id_departement) \
        .filter(Entites.id_departement == current_user.id_departement).all()


def liste_departement():
    return Sessionalchemy.query(Departements).order_by(Departements.id_departement).all()


def liste_entite_sans_ai():
    return Sessionalchemy.query(Entites).filter(Entites.id_departement == current_user.id_departement).order_by(
        Entites.id_entite).all()


def liste_responsable():
    return Sessionalchemy.query(Auditeurs).filter(Auditeurs.statut == "Responsable").filter(
        Auditeurs.id_auditeur != 1).all()


def liste_responsable_cr():
    return Sessionalchemy.query(Auditeurs).filter(Auditeurs.statut == "Responsable").filter(
        Auditeurs.id_auditeur == current_user.id_auditeur).all()


def liste_auditeur_cr():
    return Sessionalchemy.query(Auditeurs).filter(Auditeurs.is_active == True) \
        .filter(Auditeurs.id_entite == current_user.id_entite).all()


def liste_auditeur():
    return Sessionalchemy.query(Auditeurs).filter(Auditeurs.activite == True).all()


def list_auditeur():
    return Sessionalchemy.query(Auditeurs).filter(Auditeurs.is_active == True) \
        .filter(get_fonction_by_ID() != 'Chef de département').all()


def liste_agent():
    auditeur_all = []
    auditeur = Sessionalchemy.query(Auditeurs, Departements) \
        .filter(Auditeurs.id_departement == Departements.id_departement) \
        .filter(Auditeurs.id_departement == current_user.id_departement) \
        .filter(Auditeurs.is_active == True).all()
    for aud, dep in auditeur:
        if aud.id_entite is not None:
            ent = Sessionalchemy.query(Entites).filter(Entites.id_entite == aud.id_entite).first()
            auditeur_all.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
                "login": aud.login,
                "is_active": aud.is_active,
                "activite": aud.activite, "statut": aud.statut,
                "nbre_jour_formation": aud.nbre_jour_formation,
                "promotion": aud.promotion, "date_entree": aud.date_entree, "date_sortie": aud.date_sortie,
                "fonction": get_libelle_by_ID(aud.fonction), "diplomes": format_line(aud.diplomes),
                "certifications": format_line(check(aud.certifications)), "entite": ent.entite,
                "id_entite": ent.id_entite, "id_departement": dep.id_departement, "departement": dep.departement
            })
        else:
            auditeur_all.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
                "login": aud.login,
                "is_active": aud.is_active,
                "activite": aud.activite, "statut": aud.statut,
                "nbre_jour_formation": aud.nbre_jour_formation,
                "promotion": aud.promotion, "date_entree": aud.date_entree, "date_sortie": aud.date_sortie,
                "fonction": get_libelle_by_ID(aud.fonction), "diplomes": format_line(aud.diplomes),
                "certifications": format_line(check(aud.certifications)), "entite": 'pas de service',
                "id_entite": 0, "id_departement": dep.id_departement, "departement": dep.departement
            })
    return auditeur_all


def liste_statut():
    return Sessionalchemy.query(Statut).all()


def date_semaine(date_jour):
    week_number = date_jour.isocalendar()[:2]
    if len(str(week_number[1])) == 1:
        week_number = str(week_number[0]) + "-W0" + str(week_number[1])
    else:
        week_number = str(week_number[0]) + "-W" + str(week_number[1])
    return str(week_number)


def date_semaine_precedente(date_jour):
    d = date_jour - timedelta(days=7)
    week_number = d.isocalendar()[:2]
    annee = week_number[0]
    sem = week_number[1]
    if sem == 0:
        sem = 1
        annee = week_number[0] - 1
    if len(str(week_number[1])) == 1:
        week_number = str(annee) + "-W0" + str(sem)
    else:
        week_number = str(annee) + "-W" + str(sem)
    return str(week_number)


def date_semaine_suivante(date_jour):
    d = date_jour + timedelta(days=7)
    week_number = d.isocalendar()[:2]

    annee = week_number[0]
    sem = week_number[1]
    if sem == 0:
        sem = 1
        annee = week_number[0] - 1
    if len(str(week_number[1])) == 1:
        week_number = str(annee) + "-W0" + str(sem)
    else:
        week_number = str(annee) + "-W" + str(sem)
    return str(week_number)


def workdays(start, end):
    days = np.busday_count(start, end)
    return days + 1


def format_line(mot):
    if mot is None:
        mot = ""
    else:
        mot = str(mot).replace('\r\n', '<br>').replace('\n', '<br>')
    return mot


def format_fonction(chaine):
    if chaine == "Chef_de_departement":
        chaine = "Chef de département"

    elif chaine == "Chef_de_service":
        chaine = "Chef de service"

    elif chaine == "Data_Scientist":
        chaine = "Data Scientist"
    return chaine
    # return chaine.replace("_", " ")


def remove_file(fichier):
    for file in os.listdir(dossier_image):
        if fichier == file:
            os.remove(dossier_image + fichier)


def profil_connect(entite, code):
    code_perm = Sessionalchemy.query(Auditeurs).filter(Auditeurs.login == entite) \
        .filter(Auditeurs.password == code).scalar()
    profil_connect = "permanent"
    if code_perm == None:
        profil_connect = "temporaire"
    return profil_connect


# ============= département ======================
def list_departements():
    return Sessionalchemy.query(Departements).all()


def list_department():
    # return Sessionalchemy.query(Departements).all()
    department_all = []
    department = Sessionalchemy.query(Departements).all()
    for dep in department:
        if dep.responsable_departement is not None:
            auditeur = Sessionalchemy.query(Auditeurs) \
                .filter(Auditeurs.id_auditeur == dep.responsable_departement).first()
            department_all.append({"id_departement": dep.id_departement, "departement": dep.departement,
                                   "responsable_departement": auditeur.nom_auditeur,
                                   "id_auditeur": auditeur.id_auditeur,
                                   'is_active': dep.is_active
                                   })
        else:
            department_all.append({"id_departement": dep.id_departement, "departement": dep.departement,
                                   "responsable_departement": "Pas de responsable",
                                   "id_auditeur": None,
                                   'is_active': dep.is_active
                                   })
    return department_all


def list_one_department(idDept):
    department_all = []
    department = Sessionalchemy.query(Departements) \
        .filter(Departements.id_departement == idDept).all()
    for dep in department:
        department_all.append({"id_departement": dep.id_departement, "departement": dep.departement,
                               "responsable_departement": dep.responsable_departement, 'is_active': dep.is_active
                               })
    return department_all


def list_departements_json():
    result = []
    departments = Sessionalchemy.query(Departements).all()
    for dep in departments:
        result.append({
            "id_departement": dep.id_departement,
            "departement": dep.departement,
        })

    return result


def get_dep():
    dep = Sessionalchemy.query(Departements) \
        .filter(Departements.id_departement == current_user.id_departement).first()
    return dep.departement


# ============= département ======================


# ============= service ======================
def list_service():
    service_all = []
    entites = Sessionalchemy.query(Entites).all()
    for ent in entites:
        departement = get_departement_by_ID(ent.id_departement)
        service = get_responsable_by_ID(ent.responsable_service)
        service_all.append(
            {"departement": departement, "responsable_service": service,
             "entite": ent.entite,
             "is_active": ent.is_active, "id_entite": ent.id_entite
             })
    return service_all


def get_responsable_by_ID(id_res):
    aud = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == id_res).first()
    if aud is not None:
        return aud.nom_auditeur
    else:
        return "Pas de responsable"


def get_departement_by_ID(id_res):
    departmt = Sessionalchemy.query(Departements) \
        .filter(Departements.id_departement == id_res).first()
    if departmt is not None:
        return departmt.departement
    else:
        return "Pas de departement"


def get_fonction_by_ID():
    fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.id_fonction == current_user.fonction).first()
    if fonction is not None:
        return fonction.libelle
    else:
        return "Pas de fonction"


def get_libelle_by_ID(id_aud):
    if id_aud is not None:
        fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.id_fonction == id_aud).first()
    else:
        return "Pas de fonction"
    return fonction.libelle


def get_ID_by_fonction(foncion):
    if foncion is not None:
        fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.libelle == foncion).first()
        # fonction = Sessionalchemy.query(Fonctions).all()
    else:
        return "Pas de ID"
    return fonction.id_fonction


def list_one_service(idServ):
    entite_all = []
    entite = Sessionalchemy.query(Entites) \
        .filter(Entites.id_entite == idServ).all()
    for ent in entite:
        entite_all.append({"id_service": ent.id_entite, "nom_service": ent.entite,
                           "responsable_service": ent.responsable_service, 'is_active': ent.is_active,
                           "id_departement": ent.id_departement
                           })
    return entite_all


def list_services_json():
    result = []
    services = Sessionalchemy.query(Entites).all()
    for ent in services:
        result.append({
            "id_entite": ent.id_entite,
            "entite": ent.entite,
        })

    return result


# ============= service ======================


# =========== Auditeur ===========================
def listes_users_default():
    # return Sessionalchemy.query(Auditeurs).all()
    auditeur_all = []
    auditeur = Sessionalchemy.query(Auditeurs, Departements) \
        .filter(Auditeurs.id_departement == Departements.id_departement) \
        .filter(Auditeurs.is_active == True).all()
    for aud, dep in auditeur:
        if aud.id_entite is not None:
            ent = Sessionalchemy.query(Entites).filter(Entites.id_entite == aud.id_entite).first()
            auditeur_all.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
                "login": aud.login,
                "is_active": aud.is_active,
                "activite": aud.activite, "statut": aud.statut,
                "nbre_jour_formation": aud.nbre_jour_formation,
                "promotion": aud.promotion, "date_entree": aud.date_entree, "date_sortie": aud.date_sortie,
                "fonction": get_libelle_by_ID(aud.fonction), "diplomes": format_line(aud.diplomes),
                "certifications": format_line(check(aud.certifications)), "entite": ent.entite,
                "id_entite": ent.id_entite, "id_departement": dep.id_departement, "departement": dep.departement
            })
        else:
            auditeur_all.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
                "login": aud.login,
                "is_active": aud.is_active,
                "activite": aud.activite, "statut": aud.statut,
                "nbre_jour_formation": aud.nbre_jour_formation,
                "promotion": aud.promotion, "date_entree": aud.date_entree, "date_sortie": aud.date_sortie,
                "fonction": get_libelle_by_ID(aud.fonction), "diplomes": format_line(aud.diplomes),
                "certifications": format_line(check(aud.certifications)), "entite": 'pas de service',
                "id_entite": 0, "id_departement": dep.id_departement, "departement": dep.departement
            })
    return auditeur_all


def get_auditeurs_list():
    auditeur_infos = []
    auditeur = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.is_active == True).all()
    for aud in auditeur:
        if get_libelle_by_ID(aud.fonction) != 'Chef de département' and get_libelle_by_ID(
                aud.fonction) != 'Chef de service':
            auditeur_infos.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
            })
    return auditeur_infos


def get_one_users(id_user):
    user_infos = []
    user = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == id_user).scalar()
    if user.id_departement is not None:
        auditeur = Sessionalchemy.query(Auditeurs, Departements, Entites) \
            .filter(Auditeurs.id_departement == Departements.id_departement) \
            .filter(Auditeurs.id_entite == Entites.id_entite).all()
        for aud, dep, ent in auditeur:
            user_infos.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
                "fonction": aud.fonction,
                "login": aud.login,
                "is_active": aud.is_active,
                "nbre_jour_formation": user.nbre_jour_formation,
                "promotion": user.promotion, "date_entree": user.date_entree, "date_sortie": user.date_sortie,
                "diplomes": user.diplomes, "certifications": user.certifications,
                "departement": dep.departement, "id_entite": ent.id_entite, "entite": ent.entite
            })
    else:
        auditeur = Sessionalchemy.query(Auditeurs, Departements, Entites) \
            .filter(Auditeurs.id_departement == Departements.id_departement) \
            .filter(Auditeurs.id_entite == Entites.id_entite).all()
        for aud, dep, ent in auditeur:
            user_infos.append({
                "id_auditeur": aud.id_auditeur,
                "nom_auditeur": aud.nom_auditeur,
                "fonction": aud.fonction,
                "login": aud.login,
                "is_active": aud.is_active,
                "nbre_jour_formation": user.nbre_jour_formation,
                "promotion": user.promotion, "date_entree": user.date_entree, "date_sortie": user.date_sortie,
                "diplomes": user.diplomes, "certifications": user.certifications,
                "departement": "pas de département", "id_entite": ent.id_entite, "entite": ent.entite
            })
    return user_infos


def get_one_user(id_user):
    user_infos = []
    auditeur = Sessionalchemy.query(Auditeurs, Departements, Entites) \
        .filter(Auditeurs.id_auditeur == id_user) \
        .filter(Auditeurs.id_departement == Departements.id_departement) \
        .filter(Auditeurs.id_entite == Entites.id_entite).all()
    for aud, dep, ent in auditeur:
        user_infos.append({
            "id_auditeur": aud.id_auditeur,
            "nom_auditeur": aud.nom_auditeur,
            "fonction": aud.fonction,
            "login": aud.login,
            "is_active": aud.is_active,
            "nbre_jour_formation": aud.nbre_jour_formation,
            "promotion": aud.promotion, "date_entree": aud.date_entree, "date_sortie": aud.date_sortie,
            "diplomes": aud.diplomes, "certifications": aud.certifications,
            "departement": dep.departement, "id_entite": ent.id_entite, "entite": ent.entite
        })
    return user_infos


# =========== Auditeur ===========================
def get_entity_auditeur():
    entite = Sessionalchemy.query(Entites) \
        .filter(Entites.id_entite == current_user.id_entite).first()
    return entite.entite


# ================== thematique =============
def list_thematique():
    return Sessionalchemy.query(Thematiques).all()


def list_thematiques():
    all_thema = []
    thema = Sessionalchemy.query(Thematiques).all()
    for th in thema:
        all_thema.append({
            "id_thematique": th.id_thematique, "thematique": th.libelle_thematique
        })
    return all_thema


def list_one_thematique(idThema):
    thematique_all = []
    thematiques = Sessionalchemy.query(Thematiques) \
        .filter(Thematiques.id_thematique == idThema).all()
    for th in thematiques:
        thematique_all.append({"id_thematique": th.id_thematique, "thematique": th.libelle_thematique
                               })
    return thematique_all


# ================== thematique =============


# ================== competence =============
def list_competences():
    return Sessionalchemy.query(Competences).all()


def list_competence():
    # return Sessionalchemy.query(Competences).all()
    comp_all = []
    competence = Sessionalchemy.query(Competences, Thematiques) \
        .filter(Competences.id_thematique == Thematiques.id_thematique).all()
    for comp, th in competence:
        comp_all.append({"competence": comp.libelle_competence, "thematique": th.libelle_thematique,
                         "id_thematique": th.id_thematique, "id_competence": comp.id_competence,
                         "comp_cnce_it": comp.comp_cnce_it, "is_active": comp.is_active
                         })
    return comp_all


def list_one_competence(idComp):
    competence_all = []
    competences = Sessionalchemy.query(Competences, Thematiques) \
        .filter(Competences.id_competence == idComp) \
        .filter(Competences.id_thematique == Thematiques.id_thematique).all()
    for comp, th in competences:
        competence_all.append({"id_thematique": th.id_thematique, "thematique": th.libelle_thematique,
                               "competence": comp.libelle_competence, "type_comp": comp.comp_cnce_it
                               })
    return competence_all


# ================== competence =============


# ================== fonction =============
def list_fonction():
    return Sessionalchemy.query(Fonctions).filter(Fonctions.libelle != 'Chef de département') \
        .filter(Fonctions.libelle != 'Admin').all()


def list_one_fonction(id_fonction):
    fonction_all = []
    fonctions = Sessionalchemy.query(Fonctions) \
        .filter(Fonctions.id_fonction == id_fonction).all()
    for fc in fonctions:
        fonction_all.append({"id_fonction": fc.id_fonction, "fonction": fc.libelle
                             })
    return fonction_all


def get_departement_name(name):
    departement = Sessionalchemy.query(Departements).filter(Departements.departement == name.upper()).first()
    if departement is not None:
        return departement.id_departement
    else:
        return None


def get_entite_name(name):
    entite = Sessionalchemy.query(Entites).filter(Entites.entite == name.upper()).first()
    if entite is not None:
        return entite.id_entite
    else:
        return None


def get_fonction_name(name):
    fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.libelle == name.upper()).first()
    if fonction is not None:
        return fonction.id_fonction
    else:
        return None


def rename_file(file_load):
    fichier = secure_filename(file_load.filename)
    if fichier == "":
        return None
    else:
        # Séparation nom fichier et extension
        nom_fichier, extension = os.path.splitext(fichier)
        # Concaténation nom_fichier et extension
        nom_fichier = nom_fichier + "_" + datetime.now().strftime("%d%m%Y%H%M%S") + extension
        # Téléchargement
        file_load.save(dossier_doc + nom_fichier)
        return nom_fichier


# ================== Restriction ===================
def get_role_cr():
    role = get_fonction_by_ID()
    if role == 'Chef de service':
        return True
    else:
        return False


# ================== Restriction ===================
def carto_auditeur(id_auditeur):
    res = {}
    infos = Sessionalchemy.query(Auditeurs, Notation, Competences, Thematiques) \
        .filter(Auditeurs.id_auditeur == id_auditeur) \
        .filter(Notation.id_auditeur == Auditeurs.id_auditeur) \
        .filter(Competences.id_competence == Notation.id_competence) \
        .filter(Competences.id_thematique == Thematiques.id_thematique).all()
    i = 0
    thematique = []
    for aud, notation, comp, them in infos:
        thematique.append(them.libelle_thematique)
    for tema in thematique:
        i = i + 1
        result = []
        for aud, notation, comp, them in infos:

            if tema == them.libelle_thematique:
                result.append({"id_user": aud.id_auditeur, "nom_complet": aud.nom_auditeur,
                               "competence": comp.id_competence,
                               "libelle_competence": comp.libelle_competence,
                               "comp_cnce_it": comp.comp_cnce_it, "id_notation": notation.id_notation,
                               "note": notation.note, "periode": notation.periode,
                               "commentaire": "pas de commentaire pour le moment",
                               "formation": "pas de formation en cours"

                               })
        res[tema] = result
    return res


def carto_service(id_service):
    res = {}
    infos = Sessionalchemy.query(Auditeurs, Notation, Competences, Thematiques) \
        .filter(Auditeurs.id_entite == id_service) \
        .filter(Notation.id_auditeur == Auditeurs.id_auditeur) \
        .filter(Competences.id_competence == Notation.id_competence) \
        .filter(Competences.id_thematique == Thematiques.id_thematique).all()
    i = 0
    thematique = []
    for aud, notation, comp, them in infos:
        thematique.append(them.libelle_thematique)
    for tema in thematique:
        i = i + 1
        result = []
        for aud, notation, comp, them in infos:

            if tema == them.libelle_thematique:
                result.append({"id_user": aud.id_auditeur, "auditeur": aud.nom_auditeur,
                               "competence": comp.id_competence,
                               "libelle_competence": comp.libelle_competence,
                               "comp_cnce_it": comp.comp_cnce_it, "id_notation": notation.id_notation,
                               "note": notation.note, "periode": notation.periode,
                               "formation": "pas de formation en cours"

                               })
        res[tema] = result
    return res


def carto_departement(id_departement):
    res = {}
    infos = Sessionalchemy.query(Auditeurs, Notation, Competences, Thematiques) \
        .filter(Auditeurs.id_departement == id_departement) \
        .filter(Notation.id_auditeur == Auditeurs.id_auditeur) \
        .filter(Competences.id_competence == Notation.id_competence) \
        .filter(Competences.id_thematique == Thematiques.id_thematique).all()
    i = 0
    thematique = []
    for aud, notation, comp, them in infos:
        thematique.append(them.libelle_thematique)
    for tema in thematique:
        i = i + 1
        result = []
        for aud, notation, comp, them in infos:

            if tema == them.libelle_thematique:
                result.append({"id_user": aud.id_auditeur, "auditeur": aud.nom_auditeur,
                               "competence": comp.id_competence,
                               "libelle_competence": comp.libelle_competence,
                               "comp_cnce_it": comp.comp_cnce_it, "id_notation": notation.id_notation,
                               "note": notation.note, "periode": notation.periode,
                               "formation": "pas de formation en cours"

                               })
        res[tema] = result
    return res
