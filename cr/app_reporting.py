from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, session
from sqlalchemy import func, or_, and_

from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.tb_ai.table_reporting import ReportingCodir
from utils.table_entite import Entites

from fonctions import access_entite_cr, liste_responsable, liste_auditeur, liste_statut, date_semaine, \
    date_semaine_suivante, liste_codir_cr, liste_codir_cr_search, profil_connect, get_entity_auditeur, get_role_cr, \
    get_dep

codir = Blueprint('codir', __name__)
Sessionalchemy = Sessionalchemy()


@codir.route('/reporting_codir_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def reporting_codir_cr():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    max_semaine = Sessionalchemy.query(func.max(ReportingCodir.semaine)) \
        .filter(ReportingCodir.id_entite == current_user.id_entite).scalar()
    if request.method == 'POST':
        sem = request.form['week']
        # if liste_codir_cr_search(sem,current_user.id_entite):
        return render_template("/tableau-cr/reporting_codir_cr.html", profil=profil, entite=get_entity_auditeur(), role=get_role_cr(),
                               com_codir_cr=liste_codir_cr_search(sem, current_user.id_entite), max_semaine=max_semaine, departement=get_dep(),
                               semaine=sem)
    return render_template("/tableau-cr/reporting_codir_cr.html", profil=profil, departement=get_dep(),
                           com_codir_cr=liste_codir_cr(current_user.id_entite), entite=get_entity_auditeur(), role=get_role_cr(),
                           max_semaine=max_semaine, semaine=date_semaine(datetime.now()))


@codir.route('/ajout_commentaire_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def ajout_commentaire_cr():
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
        return redirect(url_for('codir.reporting_codir_cr'))


@codir.route('/modification_commentaire_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def modification_commentaire_cr():
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
        return redirect(url_for('codir.reporting_codir_cr'))


@codir.route('/suppression_commentaire_cr/<id_reporting>', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def suppression_commentaire_cr(id_reporting):
    Sessionalchemy.query(ReportingCodir).filter(ReportingCodir.id_reporting_codir == id_reporting).delete()
    Sessionalchemy.commit()
    return redirect(url_for("codir.reporting_codir_cr"))
