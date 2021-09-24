from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, jsonify, session
from sqlalchemy import func, or_, and_

from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.table_departement import Departements
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_missions import Missions
from utils.tb_ai.table_suivi_activites import SuiviActivites
from utils.table_entite import Entites
from utils.tb_ai.table_statut import Statut
from utils.tb_ai.table_reporting import ReportingCodir
from utils.tb_ai.table_rapport import Rapports

from fonctions import access_entite_ai, liste_responsable, liste_auditeur, liste_statut, date_semaine, workdays, \
    liste_mission_max_occur, liste_mission_max_occur_search, \
    check, profil_connect, liste_entite_sans_ai, liste_mission_max_occur_year_search, liste_activite_max_occur, \
    liste_activite_max_occur_search, liste_activite_max_occur_year_search, liste_auditeur_cr, get_dep

mission = Blueprint('mission', __name__)
Sessionalchemy = Sessionalchemy()
template = "mission.liste_mission"
temp_html_mission = "/tableau-ai/missions.html"
temp_html_activite = "/tableau-ai/activites.html"


@mission.route('/liste_mission', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_mission():
    # profil = profil_connect(session['entite_connecter'],session['code_connecter'])
    if request.method == 'POST':
        if list(request.form.to_dict().keys())[0] == "week":
            sem = request.form['week']
            return render_template(temp_html_mission, missions_all=liste_mission_max_occur_search(sem), departement=get_dep(),
                                   responsable=liste_responsable(), auditeurs=liste_auditeur(), statut=liste_statut(),
                                   liste_cr=liste_entite_sans_ai(), semaine=sem, annee=datetime.now().year)

        elif list(request.form.to_dict().keys())[0] == "annee":
            annee = request.form['annee']
            return render_template(temp_html_mission, missions_all=liste_mission_max_occur_year_search(annee),
                                   responsable=liste_responsable(), auditeurs=liste_auditeur(), statut=liste_statut(),
                                   liste_cr=liste_entite_sans_ai(), annee=annee, semaine=date_semaine(datetime.now()), departement=get_dep())

    return render_template(temp_html_mission, missions_all=liste_mission_max_occur(), responsable=liste_responsable(),
                           auditeurs=liste_auditeur(), statut=liste_statut(), liste_cr=liste_entite_sans_ai(),
                           semaine=date_semaine(datetime.now()), annee=datetime.now().year, departement=get_dep())


@mission.route('/liste_activite', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_activite():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        if list(request.form.to_dict().keys())[0] == "week":
            sem = request.form['week']
            return render_template(temp_html_activite, profil=profil, missions_all=liste_activite_max_occur_search(sem),
                                   responsable=liste_responsable(), auditeurs=liste_auditeur(), statut=liste_statut(), departement=get_dep(),
                                   liste_cr=liste_entite_sans_ai(), semaine=sem, annee=datetime.now().year)

        elif list(request.form.to_dict().keys())[0] == "annee":
            annee = request.form['annee']
            return render_template(temp_html_activite, profil=profil,
                                   missions_all=liste_activite_max_occur_year_search(annee), departement=get_dep(),
                                   responsable=liste_responsable(), auditeurs=liste_auditeur(), statut=liste_statut(),
                                   liste_cr=liste_entite_sans_ai(), annee=annee, semaine=date_semaine(datetime.now()))
    return render_template(temp_html_activite, profil=profil, missions_all=liste_activite_max_occur(),
                           responsable=liste_responsable(), auditeurs=liste_auditeur(), statut=liste_statut(),
                           liste_cr=liste_entite_sans_ai(), semaine=date_semaine(datetime.now()), departement=get_dep(),
                           annee=datetime.now().year)


@mission.route('/creation_mission', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def creation_mission():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        intitule_mission = request.form['intitule_mission'].strip()
        type_mission = request.form['type_mission']
        annee = request.form['annee']
        responsable = request.form['responsable']
        auditeurs = request.form.getlist("auditeurs")
        statut = request.form['statut']
        id_entite = request.form['entite']
        date_debut = check(request.form['date_debut'])
        date_fin = check(request.form['date_fin'])
        nbre_jhprevu = request.form['nbre_jhprevu']
        nbre_jhreel = check(request.form['nbre_jhreel'])
        impact = check(request.form['impact'])
        gravite = check(request.form['gravite'])
        taux_cim_teste = check(request.form['taux_cim'])
        commentaires = request.form['commentaires'].strip()
        auditeurs = set([int(val) for val in auditeurs])
        colonnes = {
            "intitule_mission": intitule_mission, "type_mission": type_mission,
            "date_debut": date_debut, "annee": annee,
            "date_fin": date_fin, "nbre_jhreel": nbre_jhreel, "nbre_jhprevu": nbre_jhprevu,
            "responsable": responsable, "auditeurs": auditeurs,
            "impact": impact, "gravite": gravite, "taux_cim_teste": taux_cim_teste,
            "commentaires": commentaires, "id_entite": id_entite
        }

        new_mission = Missions(colonnes)
        Sessionalchemy.add(new_mission)
        Sessionalchemy.commit()

        max_id = Sessionalchemy.query(func.max(Missions.id_mission)).scalar()
        table_suivi = SuiviActivites(date_semaine(datetime.now()), None, None, None, statut, max_id)
        table_rapport = Rapports(None, None, None, None, datetime.now(), max_id)
        Sessionalchemy.add(table_rapport)
        Sessionalchemy.add(table_suivi)
        Sessionalchemy.commit()
        return redirect(url_for('mission.liste_mission'))
    return render_template("/tableau-ai/creation_mission.html", profil=profil, responsable=liste_responsable(),
                           departement=get_dep(),
                           auditeurs=liste_auditeur_cr(), statut=liste_statut(), liste_cr=liste_entite_sans_ai())


@mission.route('/suppression/<id_mission>', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suppression_mission(id_mission):
    test_exist_rapp = Sessionalchemy.query(Rapports).filter(Rapports.id_mission == id_mission).count()
    test_exist_suivi = Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == id_mission).count()

    if test_exist_rapp == 1 and test_exist_suivi == 1:
        Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_mission == id_mission).delete()
        Sessionalchemy.query(Rapports).filter(Rapports.id_mission == id_mission).delete()
        Sessionalchemy.query(Missions).filter(Missions.id_mission == id_mission).delete()
        Sessionalchemy.commit()
    else:
        flash("Impossible de supprimer la mission car elle est liée à d'autres données.", "danger")
    return redirect(url_for(template))


@mission.route('/modification_mission', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def modification_mission():
    id_mission = request.form['id_mission']
    intitule_modif = request.form['intitule_modif'].strip()
    type_mission = request.form['type_mission']
    annee = request.form['annee']
    responsable_modif = request.form['responsable_modif']
    auditeur_modif = request.form.getlist("auditeur_modif")
    entite_modif = request.form['entite_modif']
    dates_debut_modif = check(request.form['dates_debut_modif'])
    dates_fin_modif = check(request.form['dates_fin_modif'])
    jh_prevu_modif = request.form['jh_prevu_modif']
    jhreel_modif = check(request.form['jh_reel_modif'])

    taux_cim_modif = check(request.form['taux_cim_modif'])
    impact_modif = check(request.form['impact_modif'])
    gravite_modif = check(request.form['gravite_modif'])
    commentaire_modif = request.form['commentaire_modif'].strip()
    auditeur_modif = set([int(val) for val in auditeur_modif])

    mission_modif = Sessionalchemy.query(Missions).filter(Missions.id_mission == id_mission).first()

    mission_modif.intitule_mission = intitule_modif
    mission_modif.type_mission = type_mission
    mission_modif.annee = annee
    mission_modif.responsable = responsable_modif
    mission_modif.auditeurs = auditeur_modif
    mission_modif.id_entite = entite_modif
    mission_modif.date_debut = dates_debut_modif
    mission_modif.date_fin = dates_fin_modif
    mission_modif.nbre_jhprevu = jh_prevu_modif
    mission_modif.nbre_jhreel = jhreel_modif
    mission_modif.taux_cim_teste = taux_cim_modif
    mission_modif.impact = impact_modif
    mission_modif.gravite = gravite_modif
    mission_modif.commentaires = commentaire_modif
    Sessionalchemy.commit()
    return redirect(url_for(template))


@mission.route('/auditeurs<valeur>', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def auditeurs(valeur):
    # print(valeur)
    auditeurs = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.activite == True) \
        .filter(Auditeurs.id_auditeur != valeur).all()
    statut_responsable = Sessionalchemy.query(Auditeurs, Entites) \
        .filter(Auditeurs.id_entite == Entites.id_entite) \
        .filter(Auditeurs.id_auditeur != 1) \
        .filter(Auditeurs.id_auditeur == valeur).all()
    entite = []
    for aud, ent in statut_responsable:
        entite.append({"id_entite": ent.id_entite, "entite": ent.entite})
    liste_auditeurs = []
    for val in auditeurs:
        liste_auditeurs.append({"id_auditeur": val.id_auditeur, "nom_auditeur": val.nom_auditeur})
    liste_finale = [liste_auditeurs, entite]
    return jsonify(liste_finale)
