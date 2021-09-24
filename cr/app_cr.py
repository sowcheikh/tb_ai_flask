from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, session, jsonify
from sqlalchemy import func, and_
from flask_login import login_required, current_user
from datetime import datetime
from utils.bdd import Sessionalchemy
from fonctions import access_entite_cr, liste_mission_max_occur_cr, liste_statut, date_semaine, \
    liste_mission_max_occur_search_cr, date_semaine_suivante, profil_connect, check, liste_entite_sans_ai, \
    liste_mission_max_occur_search_cr_year, liste_mission_max_occur_cr_mission, \
    liste_mission_max_occur_search_cr_mission, liste_mission_max_occur_search_cr_year_mission, \
    liste_mission_max_occur_cr_activite, liste_mission_max_occur_search_cr_activite, \
    liste_mission_max_occur_search_cr_year_activite, get_entity_auditeur, liste_responsable, liste_auditeur, \
    liste_responsable_cr, liste_auditeur_cr, get_role_cr, get_dep
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_rapport import Rapports

from utils.tb_ai.table_suivi_activites import SuiviActivites
from utils.tb_ai.table_missions import Missions
from utils.table_entite import Entites

cr = Blueprint('cr', __name__)
Sessionalchemy = Sessionalchemy()
template = 'cr.suivi_by_cr'
temphtml1 = "/tableau-cr/suivi_by_cr.html"
temphtml2 = "/tableau-cr/missions_cr.html"
temphtml3 = "/tableau-cr/activites_cr.html"


@cr.route('/suivi_by_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def suivi_by_cr():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])

    sub = Sessionalchemy.query(SuiviActivites.id_mission, func.max(SuiviActivites.semaine).label("max_week")) \
        .group_by(SuiviActivites.id_mission).subquery("t2")
    max_semaine = Sessionalchemy.query(SuiviActivites, Missions, Entites) \
        .join(sub, and_(
        SuiviActivites.id_mission == sub.c.id_mission,
        SuiviActivites.semaine == sub.c.max_week)) \
        .filter(
        SuiviActivites.id_mission == Missions.id_mission,
        Missions.id_entite == Entites.id_entite,
        Entites.entite == get_entity_auditeur()
    ).all()
    liste_max_semaine_by_id = {}
    for val, a, v in max_semaine:
        liste_max_semaine_by_id[val.id_mission] = val.semaine
    # print(liste_max_semaine_by_id)
    if request.method == 'POST':
        if list(request.form.to_dict().keys())[0] == "week":
            sem = request.form['week']
            return render_template(temphtml1, entite=get_entity_auditeur(), role=get_role_cr(), departement=get_dep(),
                                   missions_all=liste_mission_max_occur_search_cr(sem, get_entity_auditeur()),
                                   statut=liste_statut(), liste_max_semaine_by_id=liste_max_semaine_by_id, semaine=sem,
                                   annee=datetime.now().year)
        elif list(request.form.to_dict().keys())[0] == "annee":
            annee = request.form['annee']
            return render_template(temphtml1, entite=get_entity_auditeur(), role=get_role_cr(), departement=get_dep(),
                                   missions_all=liste_mission_max_occur_search_cr_year(annee, get_entity_auditeur()),
                                   statut=liste_statut(), liste_max_semaine_by_id=liste_max_semaine_by_id, annee=annee,
                                   semaine=date_semaine(datetime.now()))
    return render_template(temphtml1, entite=get_entity_auditeur(),role=get_role_cr(),
                           missions_all=liste_mission_max_occur_cr(get_entity_auditeur()), statut=liste_statut(),
                           liste_max_semaine_by_id=liste_max_semaine_by_id, semaine=date_semaine(datetime.now()),
                           departement=get_dep(),
                           annee=datetime.now().year)


@cr.route('/create_mission', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=['Chef de service'])
def create_mission():
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
        return redirect(url_for('cr.suivi_by_cr'))
    return render_template("/tableau-cr/creation_mission.html", profil=profil, responsable=liste_responsable_cr(),
                           auditeurs=liste_auditeur_cr(), statut=liste_statut(), role=get_role_cr(), departement=get_dep())


@cr.route('/missions_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def missions_cr():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        if list(request.form.to_dict().keys())[0] == "week":
            sem = request.form['week']
            return render_template(temphtml2, entite=get_entity_auditeur(), role=get_role_cr(),
                                   missions_all=liste_mission_max_occur_search_cr_mission(sem, get_entity_auditeur()),
                                   statut=liste_statut(), semaine=sem, annee=datetime.now().year)
        elif list(request.form.to_dict().keys())[0] == "annee":
            annee = request.form['annee']
            return render_template(temphtml2, entite=get_entity_auditeur(), role=get_role_cr(),
                                   missions_all=liste_mission_max_occur_search_cr_year_mission(annee,
                                                                                               get_entity_auditeur()),
                                   statut=liste_statut(), annee=annee, semaine=date_semaine(datetime.now()))
    return render_template(temphtml2, entite=get_entity_auditeur(), role=get_role_cr(),
                           missions_all=liste_mission_max_occur_cr_mission(get_entity_auditeur()),
                           statut=liste_statut(), semaine=date_semaine(datetime.now()), annee=datetime.now().year,
                           responsable=liste_responsable(), auditeurs=liste_auditeur(), departement=get_dep())


@cr.route('/activites_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def activites_cr():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        if list(request.form.to_dict().keys())[0] == "week":
            sem = request.form['week']
            return render_template(temphtml2, entite=get_entity_auditeur(), role=get_role_cr(),
                                   missions_all=liste_mission_max_occur_search_cr_activite(sem, get_entity_auditeur()),
                                   statut=liste_statut(), semaine=sem, annee=datetime.now().year)
        elif list(request.form.to_dict().keys())[0] == "annee":
            annee = request.form['annee']
            return render_template(temphtml2, entite=get_entity_auditeur(), role=get_role_cr(),
                                   missions_all=liste_mission_max_occur_search_cr_year_activite(annee,
                                                                                                get_entity_auditeur()),
                                   statut=liste_statut(), annee=annee, semaine=date_semaine(datetime.now()))
    return render_template(temphtml2, entite=get_entity_auditeur(), role=get_role_cr(),
                           missions_all=liste_mission_max_occur_cr_activite(get_entity_auditeur()),
                           statut=liste_statut(), semaine=date_semaine(datetime.now()), annee=datetime.now().year,
                           responsable=liste_responsable(), auditeurs=liste_auditeur(), departement=get_dep())


@cr.route('/ajout_activite', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def ajout_activite():
    if request.method == 'POST':
        id_mission = request.form['id_mission']
        statut_mission = request.form['statut_mission']
        fait = request.form['fait'].strip()
        reste_faire = request.form['reste_faire'].strip()
        difficultes = request.form['difficultes'].strip()
        nbre_reel = request.form['nbre_reel']
        jour = datetime.now().strftime('%a')
        if jour == "Fri" or jour == "Sat" or jour == "Sun":
            semaine = date_semaine_suivante(datetime.now())
        else:
            semaine = date_semaine(datetime.now())
        mission = Sessionalchemy.query(Missions).filter(Missions.id_mission == id_mission).first()
        mission.nbre_jhreel = check(nbre_reel)
        table_suivi = SuiviActivites(semaine, fait, reste_faire, difficultes, statut_mission, id_mission)
        Sessionalchemy.add(table_suivi)
        Sessionalchemy.commit()
    return redirect(url_for(template))


@cr.route('/modification_activite', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def modification_activite():
    id_mission = request.form['id_mission']
    intitule_modif = request.form['intitule_modif'].strip()
    type_mission = request.form['type_mission']
    annee = request.form['annee_modif']
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
    commentaires_hebdo = request.form['commentaire_hebdo_modif'].strip()
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
    mission_modif.commentaires_hebdo = commentaires_hebdo
    Sessionalchemy.commit()
    return redirect(url_for(template))


@cr.route('/suppression_suivi/<id_suivi>', methods=['POST', 'GET'])
@login_required
@access_entite_cr(access_level=[])
def suppression_suivi(id_suivi):
    Sessionalchemy.query(SuiviActivites).filter(SuiviActivites.id_suivi_activite == id_suivi).delete()
    Sessionalchemy.commit()
    return redirect(url_for(template))


# @cr.route('/auditeurs_modif_cr<valeur>', methods=['POST', 'GET'])
# @login_required
# @access_entite_cr(access_level=[])
# def auditeurs_modif_cr(valeur):
#     auditeurs = Sessionalchemy.query(Auditeurs) \
#         .filter(Auditeurs.activite == True) \
#         .filter(Auditeurs.id_auditeur != valeur).all()
#     statut_responsable = Sessionalchemy.query(Auditeurs, Entites) \
#         .filter(Auditeurs.id_entite == Entites.id_entite) \
#         .filter(Auditeurs.id_entite == current_user.id_entite) \
#         .filter(Auditeurs.id_auditeur == valeur).all()
#     entite = []
#     for aud, ent in statut_responsable:
#         entite.append({"id_entite": ent.id_entite, "entite": ent.entite})
#     liste_auditeurs = []
#     for val in auditeurs:
#         liste_auditeurs.append({"id_auditeur": val.id_auditeur, "nom_auditeur": val.nom_auditeur})
#     liste_finale = [liste_auditeurs, entite]
#     return jsonify(liste_finale)


@cr.route('/auditeurs_cr<valeur>', methods=['POST', 'GET'])
@login_required
@access_entite_cr(access_level=[])
def auditeurs_cr(valeur):
    liste_auditeurs = []
    entite = []
    userConnect = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == valeur).first()
    entites = Sessionalchemy.query(Entites).filter(Entites.id_entite == userConnect.id_entite).all()
    auditeurs = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.activite == True) \
        .filter(Auditeurs.id_entite == userConnect.id_entite).all()
    for val in auditeurs:
        if val.id_auditeur != valeur:
            liste_auditeurs.append({"id_auditeur": val.id_auditeur, "nom_auditeur": val.nom_auditeur})
    for ent in entites:
        entite.append({"id_entite": ent.id_entite, "entite": ent.entite})
    liste_finale = [liste_auditeurs, entite]
    return jsonify(liste_finale)

# @cr.route('/auditeurs_cr<valeur>', methods=['POST', 'GET'])
# @login_required
# @access_entite_cr(access_level=[])
# def auditeurs_cr(valeur):
#     # print(valeur)
#     auditeurs = Sessionalchemy.query(Auditeurs) \
#         .filter(Auditeurs.activite == True) \
#         .filter(Auditeurs.id_auditeur != valeur).all()
#     statut_responsable = Sessionalchemy.query(Auditeurs, Entites) \
#         .filter(Auditeurs.id_entite == Entites.id_entite) \
#         .filter(Auditeurs.id_auditeur != 1) \
#         .filter(Auditeurs.id_auditeur == valeur).all()
#     entite = []
#     for aud, ent in statut_responsable:
#         entite.append({"id_entite": ent.id_entite, "entite": ent.entite})
#     liste_auditeurs = []
#     for val in auditeurs:
#         liste_auditeurs.append({"id_auditeur": val.id_auditeur, "nom_auditeur": val.nom_auditeur})
#     liste_finale = [liste_auditeurs, entite]
#     return jsonify(liste_finale)