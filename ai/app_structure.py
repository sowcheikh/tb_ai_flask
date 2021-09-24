from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, jsonify, session
from sqlalchemy import exc

from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.table_entite import Entites
from utils.tb_ai.table_missions import Missions

from fonctions import access_entite_ai, profil_connect, liste_entite_sans_ai, get_dep

struct = Blueprint('struct', __name__)
Sessionalchemy = Sessionalchemy()

template = "struct.structure_all"


@struct.route('/structure_all', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def structure_all():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-ai/structure.html", profil=profil, liste_cr=liste_entite_sans_ai(), departement=get_dep())


@struct.route('/ajout_entite', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def ajout_entite():
    if request.method == 'POST':
        entite = request.form['entite']
        table_entite = Entites(entite.upper())
        Sessionalchemy.add(table_entite)
        Sessionalchemy.commit()
    return redirect(url_for(template))


@struct.route('/modification_entite', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def modification_entite():
    if request.method == 'POST':
        id_entite_modif = request.form['id_entite_modif']
        entite_modif = request.form['entite_modif'].strip()

        structure = Sessionalchemy.query(Entites) \
            .filter(Entites.id_entite == id_entite_modif).first()

        test_exist = Sessionalchemy.query(Entites) \
            .filter(Entites.entite == entite_modif.upper()).all()
        if test_exist:
            flash("L'entité existe déjà.", "danger")
        else:
            structure.entite = entite_modif.upper()
            Sessionalchemy.commit()
        return redirect(url_for(template))


@struct.route('/modification_code_structure', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def modification_code_structure():
    if request.method == 'POST':
        id_entite_modif = request.form['id_entite_modif_code']
        entite = Sessionalchemy.query(Entites).filter(Entites.id_entite == id_entite_modif).first()
        ancien_code = request.form['ancien_code']
        nouveau_code = request.form['nouveau_code']
        confirm_code = request.form['confirm_code']
        print(entite.code_permanant)
        if entite.code_permanant != ancien_code:
            flash("L'ancien code saisi n'est pas exact", "danger")
        elif nouveau_code != confirm_code:
            flash("Les informations que vous avez saisi ne correspondent pas", "danger")
        elif entite.code_temporaire == nouveau_code:
            flash("Le code existe déjà. Veuillez choisir un autre", "danger")
        elif nouveau_code == entite.code_permanant:
            flash("Le nouveau code est identique à celui de l'ancien. Veuillez le changer", "danger")
        elif len(nouveau_code) <= 5:
            flash("Le code d'accès doit comporter au minimum 5 caractères.", "danger")
        else:
            structure = Sessionalchemy.query(Entites).filter(Entites.id_entite == id_entite_modif).first()
            structure.code_permanant = confirm_code
            Sessionalchemy.commit()
            flash("Le code d'accès a été modifié avec succès.", "success")
        return redirect(url_for(template))


@struct.route('/suppression_entite/<id_entite>', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suppression_entite(id_entite):
    test_exist = Sessionalchemy.query(Missions).filter(Missions.id_entite == id_entite).all()
    if test_exist:
        flash("Impossible de supprimer l'entité car elle est liée à d'autres données.", "danger")
        return redirect(url_for(template))
    else:
        Sessionalchemy.query(Entites).filter(Entites.id_entite == id_entite).delete()
        Sessionalchemy.commit()
    return redirect(url_for(template))
