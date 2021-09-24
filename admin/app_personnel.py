import csv
import os
import shutil

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_login import login_required
from sqlalchemy import func
from utils.bdd import Sessionalchemy

from fonctions import check, profil_connect, access_entite_admin, listes_users_default, \
    list_departements, get_one_users, list_departements_json, liste_entite, list_services_json, get_one_user, \
    list_fonction, list_one_fonction, get_departement_name, rename_file, get_entite_name, get_libelle_by_ID, \
    get_fonction_name
from utils.table_departement import Departements
from utils.table_entite import Entites
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_fonction import Fonctions

admin_perso = Blueprint('admin_perso', __name__)
Sessionalchemy = Sessionalchemy()
template_personel = "/tableau-admin/personnel.html"
template = "admin_perso.list_personnel"
temp_html_admin = "/tableau-admin/admin.html"
template_user = "admin_perso.list_personnel"
template_fonction = "admin_perso.liste_fonction"

dossier_doc = "dossiers/"


# ===================== personel =============
@admin_perso.route('/list_personnel', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def list_personnel():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template(template_personel, auditeurs=listes_users_default(), liste_entite=liste_entite(),
                           departements=list_departements(), fonctions=list_fonction())


@admin_perso.route('/ajout_personnel', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def ajout_personnel():
    if request.method == 'POST':
        nom_auditeur = request.form['nom_auditeur'].strip()
        id_departement = request.form['id_departement']
        fonction = request.form['fonction']
        login = request.form['login']
        if fonction == "Auditeur" or fonction == "Data_Scientist":
            statut = "Auditeur"
        elif fonction == "Admin":
            statut = "Admin"
        else:
            statut = "Responsable"

        colonnes = {
            "nom_auditeur": nom_auditeur, "id_departement": id_departement, "login": login,
            "is_active": True, "fonction": fonction, "statut": statut, "activite": True,
            "methode": "LDAP", "password": "test"
        }
        new_personnel = Auditeurs(colonnes)
        Sessionalchemy.add(new_personnel)
        Sessionalchemy.commit()
    return redirect(url_for(template))


@admin_perso.route('/modification_personnel', methods=['POST', 'GET'])
@login_required
@access_entite_admin(access_level=['Admin'])
def modification_personnel():
    id_auditeur = request.form['id_auditeur']
    nom_auditeur = request.form['nom_auditeur']
    login = request.form['login']
    fonction = request.form['fonction']
    departement = request.form['id_departement']
    entite = request.form['id_entite_modif']
    nbre_jour_formation_modif = request.form['nbre_jour_formation_modif']
    promotion_modif = request.form['promotion_modif']
    date_entree_modif = request.form['date_entree_modif']
    date_sortie_modif = request.form['date_sortie_modif']
    diplomes_modif = request.form['diplomes_modif'].strip()
    certifications_modif = request.form['certifications_modif'].strip()
    res_dep = request.form['id_departement']
    res_serv = request.form['id_entite_modif']

    personnel_modif = Sessionalchemy.query(Auditeurs) \
        .filter(Auditeurs.id_auditeur == id_auditeur).first()
    if fonction == "Auditeur" or fonction == "Data_Scientist":
        statut = "Auditeur"
    else:
        statut = "Responsable"

    if fonction != "Data_Scientist":
        personnel_modif.statut = statut
    dep = Sessionalchemy.query(Departements) \
        .filter(Departements.responsable_departement == id_auditeur).first()
    serv = Sessionalchemy.query(Entites) \
        .filter(Entites.responsable_service == id_auditeur).first()

    if fonction == "Auditeur" or fonction == "Data_Scientist":
        statut = "Auditeur"
        if dep is not None:
            dep.responsable_departement = None
        if serv is not None:
            serv.responsable_service = None
    elif fonction == "Admin":
        statut = "Admin"
    else:
        statut = "Responsable"

    if fonction != "Data_Scientist":
        personnel_modif.statut = statut
    elif fonction == "Chef_de_service":
        service = Sessionalchemy.query(Entites) \
            .filter(Entites.id_entite == res_serv).first()
        service.responsable_service = id_auditeur
    elif fonction == "Chef_de_departement":
        departement = Sessionalchemy.query(Departements) \
            .filter(Departements.id_departement == res_dep).first()
        departement.responsable_departement = id_auditeur

    personnel_modif.nom_auditeur = nom_auditeur
    personnel_modif.login = login
    personnel_modif.fonction = fonction
    personnel_modif.nbre_jour_formation = check(nbre_jour_formation_modif)
    personnel_modif.promotion = check(promotion_modif)
    personnel_modif.date_entree = check(date_entree_modif)
    personnel_modif.date_sortie = check(date_sortie_modif)
    personnel_modif.diplomes = diplomes_modif
    personnel_modif.certifications = check(certifications_modif)
    personnel_modif.id_entite = entite
    personnel_modif.id_departement = departement
    Sessionalchemy.commit()
    return redirect(url_for(template_user))


@admin_perso.route('/details<valeur>', methods=['GET'])
def get_infos(valeur):
    return jsonify(get_one_users(int(valeur)))


@admin_perso.route('/modifiers<valeur>', methods=['GET'])
def modif_infos(valeur):
    result = [{
        'departements': list_departements_json(),
        'infos': get_one_users(int(valeur))
    }]
    return jsonify(result)


@admin_perso.route('/auditeurs_modif<valeur>', methods=['GET'])
def auditeurs_modif(valeur):
    result = [{
        'departements': list_departements_json(),
        'services': list_services_json(),
        'infos': get_one_user(int(valeur))
    }]
    return jsonify(result)


@admin_perso.route('/bloquer_personnel<id_user>', methods=['GET'])
@login_required
@access_entite_admin(access_level=['Admin'])
def bloquer_personnel(id_user):
    user = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == id_user).first()
    user.is_active = False
    Sessionalchemy.commit()
    return redirect(url_for(template_user))


@admin_perso.route('/debloquer_personnel<id_user>', methods=['GET'])
@login_required
@access_entite_admin(access_level=['Admin'])
def debloquer_personnel(id_user):
    user = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == id_user).first()
    user.is_active = True
    Sessionalchemy.commit()
    return redirect(url_for(template_user))


@admin_perso.route('/service_personnel<id_dep>', methods=['GET'])
@login_required
@access_entite_admin(access_level=['Admin'])
def service_personnel(id_dep):
    infos = Sessionalchemy.query(Departements, Entites) \
        .filter(Departements.id_departement == id_dep) \
        .filter(Departements.id_departement == Entites.id_departement).all()
    entite = []
    for dep, ent in infos:
        entite.append({"id_entite": ent.id_entite, "entite": ent.entite
                       })
    return jsonify(entite)


# ============== ajouter par csv ===================
@admin_perso.route('/ajout_personnel_csv', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def ajout_personnel_csv():
    if os.path.exists(dossier_doc) is False:
        os.mkdir(dossier_doc)
    if request.method == 'POST':
        uploaded_file = request.files['files']
        nomfichier = rename_file(uploaded_file)
        if nomfichier is not None:
            filePath = dossier_doc + nomfichier
            csvfile = open(filePath, 'r', encoding='utf-8', errors='ignore')
            csvReader = csv.reader(csvfile, delimiter=",")

            data = []
            i = 0
            for col in csvReader:
                dir_dep = get_departement_name(col[i + 3])
                dir_serv = get_entite_name(col[i + 2])
                dir_fonc = get_fonction_name(col[i + 4])
                colonnes = {
                    "nom_auditeur": col[i], "login": col[i +1], "id_entite": dir_serv, "id_departement": dir_dep, "fonction": dir_fonc
                }
                data.append(colonnes)
                Sessionalchemy.add(Auditeurs(colonnes))
                Sessionalchemy.commit()
            shutil.rmtree(dossier_doc)
        return redirect(url_for(template))


@admin_perso.route('/download', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def telechager():
    path = "ressources/files/file.csv"
    return send_file(path, as_attachment=True)


# ============== ajouter par csv ===================


# ============== fonction ===================
@admin_perso.route('/liste_fonction', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def liste_fonction():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-admin/fonction.html", profil=profil, liste_fonction=list_fonction())


@admin_perso.route('/ajout_fonction', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def ajout_fonction():
    if request.method == 'POST':
        libelle = request.form['libelle'].strip()
        table_fonction = Fonctions(libelle)
        Sessionalchemy.add(table_fonction)
        Sessionalchemy.commit()
    return redirect(url_for(template_fonction))


@admin_perso.route('/modification_fonction', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def modification_fonction():
    id_fonction = request.form['id_fonction']
    fonction_modif = request.form['libelle'].strip()

    fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.id_fonction == id_fonction).first()
    fonction.libelle = fonction_modif
    Sessionalchemy.commit()
    return redirect(url_for(template_fonction))


@admin_perso.route('/modif_fonction<valeur>', methods=['GET'])
def modif_fonction(valeur):
    result = [{
        'fonction': list_one_fonction(valeur),
    }]
    return jsonify(result)


@admin_perso.route('/debloquer_fonction<valeur>', methods=['GET'])
def debloquer_fonction(valeur):
    fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.id_fonction == valeur).first()
    fonction.is_active = True
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@admin_perso.route('/bloquer_fonction<valeur>', methods=['GET'])
def bloquer_fonction(valeur):
    fonction = Sessionalchemy.query(Fonctions).filter(Fonctions.id_fonction == valeur).first()
    fonction.is_active = False
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})

# ============== fonction ===================
