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

from fonctions import access_entite_ai, liste_rapport_max_occur_ai, liste_rapport_ai_search, liste_rapport_max_by_id, \
    remove_file, profil_connect, liste_entite_sans_ai, get_dep

dossier_image = "../static/assets/data/rapports/"

rapp_ai = Blueprint('rapp_ai', __name__)
Sessionalchemy = Sessionalchemy()


@rapp_ai.route('/liste_rapport_ai/<entite>', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_rapport_ai(entite):
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    if request.method == 'POST':
        day = request.form['date_jour']
        # if liste_rapport_ai_search(day,entite):
        return render_template("/tableau-ai/rapport_ai.html", profil=profil, entite=entite,
                               rapports_all=liste_rapport_ai_search(day, entite), departement=get_dep(),
                               liste_rapport_max_by_id=liste_rapport_max_by_id(entite), liste_cr=liste_entite_sans_ai(),
                               day=day)
    return render_template("/tableau-ai/rapport_ai.html", profil=profil, entite=entite,
                           rapports_all=liste_rapport_max_occur_ai(entite), departement=get_dep(),
                           liste_rapport_max_by_id=liste_rapport_max_by_id(entite), liste_cr=liste_entite_sans_ai())


@rapp_ai.route('/ajout_rapport', methods=['GET', 'POST'])
@login_required
def ajout_rapport_ai():
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
        nom_fichier = nom_fichier + "_" + datetime.now().strftime("%d%m%Y%H%M%S") + extension
        # Téléchargement
        rapport.save("static/assets/data/rapports/" + nom_fichier)
        table_rapport = Rapports(constats, causes, recommandations, nom_fichier, datetime.now(), id_mission)
        Sessionalchemy.add(table_rapport)
        Sessionalchemy.commit()
    return redirect(url_for('rapp_ai.liste_rapport_ai', entite=entite_concerne(id_mission)))


def entite_concerne(id_mission):
    rapport = Sessionalchemy.query(Missions, Entites).filter(Missions.id_entite == Entites.id_entite) \
        .filter(Missions.id_mission == id_mission).first()
    return rapport[1].entite


@rapp_ai.route('/modif_rapport_ai', methods=['GET', 'POST'])
@login_required
def modif_rapport_ai():
    if request.method == "POST":
        id_mission_modif = request.form['id_mission_modif']
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
    return redirect(url_for('rapp_ai.liste_rapport_ai', entite=entite_concerne(id_mission_modif)))


@rapp_ai.route('/suppression_rapport_ai/<id_rapport>/<id_mission>', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suppression_rapport_ai(id_rapport, id_mission):
    fichier = Sessionalchemy.query(Rapports).filter(Rapports.id_rapport == id_rapport).scalar()
    remove_file(fichier.rapport)
    Sessionalchemy.query(Rapports).filter(Rapports.id_rapport == id_rapport).delete()
    Sessionalchemy.commit()
    return redirect(url_for("rapp_ai.liste_rapport_ai", entite=entite_concerne(id_mission)))
