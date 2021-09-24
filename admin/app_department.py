from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import login_required
from sqlalchemy import func
from utils.bdd import Sessionalchemy

from fonctions import access_entite_admin, list_department, \
    list_auditeur, list_one_department, get_auditeurs_list, get_ID_by_fonction
from utils.table_departement import Departements
from utils.tb_ai.table_auditeurs import Auditeurs

admin_dep = Blueprint('admin_dep', __name__)
Sessionalchemy = Sessionalchemy()
template_dep = "/tableau-admin/departement.html"
template_creation_dep = "/tableau-admin/creation_departement.html"
template = "admin_dep.liste_departement"
temp_html_admin = "/tableau-admin/admin.html"


# ============ departements =================
@admin_dep.route('/liste_departement', methods=['GET'])
@login_required
@access_entite_admin(access_level=['Admin'])
def liste_departement():
    return render_template(template_dep, departements=list_department(), auditeurs=list_auditeur())


@admin_dep.route('/creation_departement', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def creation_departement():
    if request.method == 'POST':
        departement = request.form['departement'].strip()
        responsable_departement = request.form['responsable_departement'].strip()
        auditeur = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == responsable_departement).first()
        auditeur.fonction = get_ID_by_fonction('Chef de département')
        colonnes = {
            "departement": departement, "responsable_departement": responsable_departement,
            "is_active": True,
        }
        new_departement = Departements(colonnes)
        Sessionalchemy.add(new_departement)
        Sessionalchemy.add(auditeur)
        Sessionalchemy.commit()
    return redirect(url_for(template))


@admin_dep.route('/modification_departement', methods=['GET', 'POST'])
@login_required
@access_entite_admin(access_level=['Admin'])
def modification_departement():
    id_departement = request.form['id_departement']
    departement = request.form['departement'].strip()
    responsable_departement = request.form['responsable_departement'].strip()

    departement_modif = Sessionalchemy.query(Departements).filter(Departements.id_departement == id_departement).first()
    usr_modif = Sessionalchemy.query(Auditeurs).filter(Auditeurs.id_auditeur == responsable_departement).first()
    usr_modif.statut = 'Responsable'
    usr_modif.fonction = get_ID_by_fonction('Chef de département')

    departement_modif.departement = departement
    departement_modif.responsable_departement = responsable_departement
    Sessionalchemy.commit()
    return redirect(url_for(template))


@admin_dep.route('/modifier_dep<valeur>', methods=['GET'])
def modifier_dep(valeur):
    result = [{
        'departements': list_one_department(valeur),
        'infos': get_auditeurs_list()
    }]
    return jsonify(result)


@admin_dep.route('/debloquer_dept<valeur>', methods=['GET'])
def debloquer_dept(valeur):
    departement_modif = Sessionalchemy.query(Departements).filter(Departements.id_departement == valeur).first()
    departement_modif.is_active = True
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@admin_dep.route('/bloquer_dept<valeur>', methods=['GET'])
def bloquer_dept(valeur):
    departement_modif = Sessionalchemy.query(Departements).filter(Departements.id_departement == valeur).first()
    departement_modif.is_active = False
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@admin_dep.route('/supprimer_dept/<valeur>', methods=['POST', 'GET'])
def supprimer_dept(valeur):
    Sessionalchemy.query(Departements).filter(Departements.id_departement == valeur).delete()
    Sessionalchemy.commit()
    return redirect(url_for(template))
