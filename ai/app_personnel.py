from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, jsonify, session
from sqlalchemy import func, or_, and_

from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.table_entite import Entites
from utils.tb_ai.table_missions import Missions

from fonctions import access_entite_ai, liste_agent, check, profil_connect, liste_entite, liste_entite_sans_ai, \
    list_fonction, liste_entite_one_dep, get_ID_by_fonction, get_dep, get_fonction_by_ID

agent = Blueprint('agent', __name__)
Sessionalchemy = Sessionalchemy()
template = "agent.liste_personnel"


@agent.route('/liste_personnel', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_personnel():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-ai/personnel.html", profil=profil, agents=liste_agent(), departement=get_dep(),
                           liste_entite=liste_entite_one_dep(), liste_cr=liste_entite_sans_ai(), fonctions=list_fonction())


@agent.route('/ajout_personnels', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=["Chef de département"])
def ajout_personnels():
    if request.method == 'POST':
        nom_auditeur = request.form['nom_auditeur'].strip()
        fonction = request.form['fonction']
        login = request.form['login']
        id_entite = request.form['id_entite']
        nbre_jour_formation = request.form['nbre_jour_formation']
        promotion = request.form['promotion']
        date_entree = request.form['date_entree']
        date_sortie = request.form['date_sortie']
        diplomes = request.form['diplomes'].strip()
        certifications = request.form['certifications'].strip()
        if fonction == "Auditeur" or fonction == "Data_Scientist":
            statut = "Auditeur"
        else:
            statut = "Responsable"

        colonnes = {
            "nom_auditeur": nom_auditeur, "fonction": fonction, "id_entite": id_entite, "statut": statut,
            "activite": True, "login": login, "is_active": True, "methode": "LDAP", "password": "test",
            "nbre_jour_formation": check(nbre_jour_formation), "promotion": check(promotion),
            "date_entree": check(date_entree), "id_departement": current_user.id_departement,
            "date_sortie": check(date_sortie), "diplomes": diplomes, "certifications": check(certifications)
        }
        new_personnel = Auditeurs(colonnes)
        Sessionalchemy.add(new_personnel)
        Sessionalchemy.commit()
    return redirect(url_for(template))


@agent.route('/modification_personnels', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def modification_personnels():
    id_auditeur = request.form['id_auditeur']
    nom_auditeur_modif = request.form['nom_auditeur_modif']
    fonction_modif = request.form['fonction_modif']
    id_entite_modif = request.form['id_entite_modif']
    nbre_jour_formation_modif = request.form['nbre_jour_formation_modif']
    promotion_modif = request.form['promotion_modif']
    date_entree_modif = request.form['date_entree_modif']
    date_sortie_modif = request.form['date_sortie_modif']
    diplomes_modif = request.form['diplomes_modif'].strip()
    certifications_modif = request.form['certifications_modif'].strip()

    personnel_modif = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.id_auditeur == id_auditeur).first()

    if fonction_modif == "Auditeur" or fonction_modif == "Data_Scientist":
        statut = "Auditeur"
    else:
        statut = "Responsable"

    if fonction_modif != "Data_Scientist":
        personnel_modif.statut = statut
    personnel_modif.nom_auditeur = nom_auditeur_modif
    personnel_modif.fonction = fonction_modif
    personnel_modif.nbre_jour_formation = check(nbre_jour_formation_modif)
    personnel_modif.promotion = check(promotion_modif)
    personnel_modif.date_entree = check(date_entree_modif)
    personnel_modif.date_sortie = check(date_sortie_modif)
    personnel_modif.diplomes = diplomes_modif
    personnel_modif.certifications = check(certifications_modif)
    personnel_modif.id_entite = id_entite_modif
    Sessionalchemy.commit()
    return redirect(url_for(template))


@agent.route('/suppressions/<id_auditeur>', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def suppression_personnels(id_auditeur):
    id_aud_exist = Sessionalchemy.query(Auditeurs).filter(Missions.auditeurs.any(id_auditeur)).all()
    id_resp_exist = Sessionalchemy.query(Auditeurs).filter(Missions.responsable == id_auditeur).all()
    if id_aud_exist or id_resp_exist:
        flash("Impossible de supprimer le personnel car elle est liée à des missions.", "danger")
    else:
        Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == id_auditeur).delete()
        Sessionalchemy.commit()
    return redirect(url_for(template))


@agent.route('/deblocage/<id_auditeur>', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def deblocage(id_auditeur):
    personnel_modif = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.id_auditeur == id_auditeur).first()
    personnel_modif.activite = True
    Sessionalchemy.commit()
    return redirect(url_for(template))


@agent.route('/blocage/<id_auditeur>', methods=['POST', 'GET'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def blocage(id_auditeur):
    personnel_modif = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.id_auditeur == id_auditeur).first()
    personnel_modif.activite = False
    Sessionalchemy.commit()
    return redirect(url_for(template))
