from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, jsonify, session
from sqlalchemy import func, or_, and_

from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_missions import Missions
from utils.tb_ai.table_suivi_activites import SuiviActivites
from utils.tb_ai.table_reporting import ReportingCodir
from utils.table_entite import Entites
from utils.tb_ai.table_statut import Statut

from fonctions import access_entite_ai, liste_responsable, liste_auditeur, liste_statut, date_semaine, \
    date_semaine_suivante, liste_mission_max_occur_cr, liste_codir_ai, liste_codir_ai_search, \
    liste_mission_max_occur_search_cr, profil_connect, liste_suivi_activite_all, liste_suivi_activite_search_all, \
    liste_entite_sans_ai, get_dep

suivi_ai = Blueprint('suivi_ai', __name__)
Sessionalchemy = Sessionalchemy()

template = "/tableau-ai/suivi_cr.html"


@suivi_ai.route('/suivi/<entite>', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suivi(entite):
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        sem = request.form['week']
        # if liste_mission_max_occur_search_cr(sem,entite):
        return render_template(template, entite=entite, missions_all=liste_mission_max_occur_search_cr(sem, entite),
                               liste_cr=liste_entite_sans_ai(), departement=get_dep(), semaine=sem)
    return render_template(template, entite=entite, missions_all=liste_mission_max_occur_cr(entite), departement=get_dep(),
                           liste_cr=liste_entite_sans_ai(), semaine=date_semaine(datetime.now()))


@suivi_ai.route('/suivi_all', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suivi_all():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    jour = datetime.now().strftime('%a')
    if jour == "Fri" or jour == "Sat" or jour == "Sun":
        semaine = date_semaine_suivante(datetime.now())
    else:
        semaine = date_semaine(datetime.now())

    if request.method == 'POST':
        sem = request.form['week']
        # if liste_suivi_activite_search_all(sem):
        return render_template("/tableau-ai/suivi_cr_all.html", profil=profil, departement=get_dep(),
                               missions_all=liste_suivi_activite_search_all(sem), semaine=sem,
                               liste_cr=liste_entite_sans_ai())
    return render_template("/tableau-ai/suivi_cr_all.html", profil=profil, missions_all=liste_suivi_activite_all(),
                           semaine=semaine, liste_cr=liste_entite_sans_ai(), departement=get_dep())


@suivi_ai.route('/suivi_filiales', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def suivi_filiales():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-ai/suivi_filiales.html", profil=profil, departement=get_dep(), liste_cr=liste_entite_sans_ai())


@suivi_ai.route('/suivi_report', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def suivi_report():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-ai/suivi_report.html", profil=profil, departement=get_dep(), liste_cr=liste_entite_sans_ai())


#####################################Reporting CODIR####################################
@suivi_ai.route('/reporting_codir_ai', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def reporting_codir_ai():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    max_semaine = Sessionalchemy.query(func.max(ReportingCodir.semaine)) \
        .filter(ReportingCodir.id_entite == current_user.id_entite).scalar()
    if request.method == 'POST':
        sem = request.form['week']
        # if liste_codir_ai_search(sem):
        return render_template("/tableau-ai/reporting_codir_ai.html", profil=profil,
                               com_codir_ai=liste_codir_ai_search(sem), max_semaine=max_semaine,
                               departement=get_dep(),
                               liste_cr=liste_entite_sans_ai(), semaine=sem)
    return render_template("/tableau-ai/reporting_codir_ai.html", profil=profil, com_codir_ai=liste_codir_ai(),
                           departement=get_dep(),
                           max_semaine=max_semaine, liste_cr=liste_entite_sans_ai(),
                           semaine=date_semaine(datetime.now()))


@suivi_ai.route('/ajout_commentaire_ai', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def ajout_commentaire_ai():
    if request.method == 'POST':
        fonctionne = request.form['fonctionne'].strip()
        point_coordination = request.form['point_coordination'].strip()
        difficultes = request.form['difficultes'].strip()
        jour = datetime.now().strftime('%a')
        if jour == "Fri" or jour == "Sat" or jour == "Sun":
            semaine = date_semaine_suivante(datetime.now())
        else:
            semaine = date_semaine(datetime.now())
        table_reporting = ReportingCodir(semaine, fonctionne, point_coordination, difficultes, current_user.id_entite)
        Sessionalchemy.add(table_reporting)
        Sessionalchemy.commit()
        return redirect(url_for('suivi_ai.reporting_codir_ai'))


@suivi_ai.route('/modification_commentaire_ai', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def modification_commentaire_ai():
    if request.method == 'POST':
        id_reporting_codir = request.form['id_reporting_codir']
        fonctionne_modif = request.form['fonctionne_modif'].strip()
        point_coordination_modif = request.form['point_coordination_modif'].strip()
        difficultes_modif = request.form['difficultes_modif'].strip()

        codir_ai = Sessionalchemy.query(ReportingCodir) \
            .filter(ReportingCodir.id_reporting_codir == id_reporting_codir).first()

        codir_ai.fonctionne = fonctionne_modif
        codir_ai.point_coordination = point_coordination_modif
        codir_ai.difficultes = difficultes_modif
        Sessionalchemy.commit()
        return redirect(url_for('suivi_ai.reporting_codir_ai'))


@suivi_ai.route('/suppression_commentaire_ai/<id_reporting>', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suppression_commentaire_ai(id_reporting):
    Sessionalchemy.query(ReportingCodir).filter(ReportingCodir.id_reporting_codir == id_reporting).delete()
    Sessionalchemy.commit()
    return redirect(url_for("suivi_ai.reporting_codir_ai"))
