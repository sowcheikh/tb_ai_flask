from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, jsonify, send_from_directory, \
    send_file, session
from sqlalchemy import func, or_, and_
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.tb_ai.table_missions import Missions
from utils.tb_ai.table_rapport import Rapports
from utils.table_entite import Entites

from fonctions import access_entite_cr, liste_rapport_max_occur_cr, liste_rapport_cr_search, liste_rapport_max_by_id, \
    remove_file, profil_connect, liste_entite_sans_ai, get_entity_auditeur, get_role_cr, get_dep

dossier_image = "static/assets/data/rapports/"

rapp_cr = Blueprint('rapp_cr', __name__)
Sessionalchemy = Sessionalchemy()


@rapp_cr.route('/liste_rapport_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def liste_rapport_cr():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        day = request.form['date_jour']
        # if liste_rapport_cr_search(day,current_user.entite):
        return render_template("/tableau-cr/rapport_cr.html", profil=profil,
                               rapports_all=liste_rapport_cr_search(day, get_entity_auditeur()),
                               liste_rapport_max_by_id=liste_rapport_max_by_id(get_entity_auditeur()),
                               entite=get_entity_auditeur(), day=day, role=get_role_cr(), departement=get_dep())

    return render_template("/tableau-cr/rapport_cr.html", profil=profil,
                           rapports_all=liste_rapport_max_occur_cr(get_entity_auditeur()),
                           liste_rapport_max_by_id=liste_rapport_max_by_id(get_entity_auditeur()),
                           entite=get_entity_auditeur(), role=get_role_cr(), departement=get_dep())


@rapp_cr.route('/ajout_rapport_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def ajout_rapport_cr():
    if request.method == "POST":
        constats = request.form['constats']
        causes = request.form['causes']
        recommandations = request.form['recommandations']
        id_mission = request.form['id_mission']
        rapport = request.files["rapport"]
        fichier = secure_filename(rapport.filename)
        # Séparation nom fichier et extension
        nom_fichier, extension = os.path.splitext(fichier)
        # Concaténation nom_fichier et extension
        nom_fichier = nom_fichier + " " + datetime.now().strftime("%d%m%Y%H%M%S") + extension
        # Téléchargement
        rapport.save(dossier_image + nom_fichier)
        table_rapport = Rapports(constats, causes, recommandations, nom_fichier, datetime.now(), id_mission)
        Sessionalchemy.add(table_rapport)
        Sessionalchemy.commit()
    return redirect(url_for('rapp_cr.liste_rapport_cr'))


@rapp_cr.route('/modif_rapport_cr', methods=['GET', 'POST'])
@login_required
@access_entite_cr(access_level=[])
def modif_rapport_cr():
    if request.method == "POST":
        constats_modif = request.form['constats_modif']
        causes_modif = request.form['causes_modif']
        recommandations_modif = request.form['recommandations_modif']
        id_rapport_modif = request.form['id_rapport_modif']
        rapport_modif = request.files["rapport_modif"]
        fichier = secure_filename(rapport_modif.filename)

        rapport = Sessionalchemy.query(Rapports).filter(Rapports.id_rapport == id_rapport_modif).first()
        if fichier != "":
            # Séparation nom fichier et extension
            nom_fichier, extension = os.path.splitext(fichier)
            # Concaténation nom_fichier et extension
            nom_fichier = nom_fichier + " " + datetime.now().strftime("%d%m%Y%H%M%S") + extension
            # Téléchargement
            rapport_modif.save(dossier_image + nom_fichier)
            remove_file(rapport.rapport)
            rapport.rapport = nom_fichier

        rapport.constats = constats_modif
        rapport.causes = causes_modif
        rapport.recommandations = recommandations_modif
        rapport.date = datetime.now()
        Sessionalchemy.commit()
    return redirect(url_for('rapp_cr.liste_rapport_cr'))


@rapp_cr.route('/suppression_rapport_cr/<id_rapport>', methods=['POST', 'GET'])
@login_required
@access_entite_cr(access_level=[])
def suppression_rapport_cr(id_rapport):
    fichier = Sessionalchemy.query(Rapports).filter(Rapports.id_rapport == id_rapport).scalar()
    remove_file(fichier.rapport)
    Sessionalchemy.query(Rapports).filter(Rapports.id_rapport == id_rapport).delete()
    Sessionalchemy.commit()
    return redirect(url_for("rapp_cr.liste_rapport_cr"))
