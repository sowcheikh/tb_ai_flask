from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_required
from sqlalchemy import func
from utils.bdd import Sessionalchemy

from fonctions import access_entite_admin, list_service, \
    list_departements, list_one_service, get_auditeurs_list, list_department
from utils.table_entite import Entites
from utils.tb_ai.table_auditeurs import Auditeurs

admin_serv = Blueprint('admin_serv', __name__)
Sessionalchemy = Sessionalchemy()
template_serv = "admin_serv.liste_service"
template_service = "/tableau-admin/service.html"
temp_html_admin = "/tableau-admin/admin.html"


# ================ service ==================
@admin_serv.route('/liste_service', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def liste_service():
    return render_template(template_service, services=list_service(), departements=list_departements())


@admin_serv.route('/creation_service', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def creation_service():
    if request.method == 'POST':
        departement = request.form['id_departement'].strip()
        entite = request.form['entite']
        colonnes = {
            "entite": entite, "id_departement": departement,
            "is_active": True
        }
        new_service = Entites(colonnes)
        Sessionalchemy.add(new_service)
        Sessionalchemy.commit()

    return redirect(url_for(template_serv))


@admin_serv.route('/modification_service', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def modification_service():
    id_entite = request.form['id_entite']
    entite = request.form['entite'].strip()
    id_departement = request.form['id_departement']
    responsable_service = request.form['responsable_service'].strip()
    auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == responsable_service).first()
    auditeur.fonction = 'Chef de service'

    service_modif = Sessionalchemy.query(Entites).filter(Entites.id_entite == id_entite).first()
    dep_modif = Sessionalchemy.query(Entites).filter(Entites.id_departement == id_departement).first()

    service_modif.entite = entite
    service_modif.responsable_service = responsable_service
    service_modif.id_departement = id_departement
    Sessionalchemy.add(auditeur)
    Sessionalchemy.commit()
    return redirect(url_for(template_serv))


@admin_serv.route('/modif_service<valeur>', methods=['GET'])
def modif_service(valeur):
    result = [{
        'services': list_one_service(valeur),
        'infos': get_auditeurs_list(),
        'departements': list_department()
    }]
    return jsonify(result)


@admin_serv.route('/debloquer_service<valeur>', methods=['GET'])
def debloquer_service(valeur):
    service_modif = Sessionalchemy.query(Entites).filter(Entites.id_entite == valeur).first()
    service_modif.is_active = True
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@admin_serv.route('/bloquer_service<valeur>', methods=['GET'])
def bloquer_service(valeur):
    service_modif = Sessionalchemy.query(Entites).filter(Entites.id_entite == valeur).first()
    service_modif.is_active = False
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@admin_serv.route('/supprimer_dept/<valeur>', methods=['POST', 'GET'])
def supprimer_dept(valeur):
    Sessionalchemy.query(Entites).filter(Entites.id_entite == valeur).delete()
    Sessionalchemy.commit()
    return redirect(url_for(template_serv))
