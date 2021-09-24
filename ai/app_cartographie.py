from flask import Flask, render_template, request, flash, url_for, redirect, Blueprint, jsonify, session
from sqlalchemy import func, or_, and_

from flask_login import login_required, current_user
from datetime import datetime, date
from utils.bdd import Sessionalchemy
from utils.table_departement import Departements
from utils.table_entite import Entites
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_notation import Notation
from utils.tb_ai.table_thematique import Thematiques
from utils.tb_ai.table_competence import Competences

from fonctions import access_entite_ai, profil_connect, liste_entite_sans_ai, list_thematique, list_one_thematique, \
    list_competence, list_one_competence, list_thematiques, list_competences, carto_service, carto_departement, get_dep

carto = Blueprint('carto', __name__)
Sessionalchemy = Sessionalchemy()

template = "carto.liste_thematique"
template_carto = "carto.liste_cartographie"
template_comp = "carto.liste_competence"


@carto.route('/liste_cartographie', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_cartographie():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])

    auditeur = Sessionalchemy.query(Auditeurs).all()
    entite = Sessionalchemy.query(Entites).all()
    dep = Sessionalchemy.query(Departements).all()
    return render_template("/tableau-ai/cartographie.html", profil=profil, liste_cr=liste_entite_sans_ai(),
                           departement=get_dep(),
                           entites=entite, auditeurs=auditeur, departements=dep, competences=list_competence(),
                           aut_id=0)


@carto.route('/liste_cartographie/<id_auditeur>', methods=['GET'])
def cartographie(id_auditeur):
    res = {}
    infos = Sessionalchemy.query(Auditeurs, Notation, Competences, Thematiques) \
        .filter(Auditeurs.id_auditeur == id_auditeur) \
        .filter(Notation.id_auditeur == Auditeurs.id_auditeur) \
        .filter(Competences.id_competence == Notation.id_competence) \
        .filter(Competences.id_thematique == Thematiques.id_thematique).all()
    i = 0
    thematique = []
    for aud, notation, comp, them in infos:
        thematique.append(them.libelle_thematique)
    for tema in thematique:
        i = i + 1
        result = []
        for aud, notation, comp, them in infos:

            if tema == them.libelle_thematique:
                result.append({"id_user": aud.id_auditeur, "auditeur": aud.nom_auditeur,
                               "competence": comp.id_competence,
                               "libelle_competence": comp.libelle_competence,
                               "comp_cnce_it": comp.comp_cnce_it, "id_notation": notation.id_notation,
                               "note": notation.note, "periode": notation.periode,
                               "formation": "pas de formation en cours"

                               })
        res[tema] = result
    return jsonify(res)


@carto.route('/liste_cartographie_ent/<id_entite>', methods=['GET'])
def cartographie_ent(id_entite):
    return jsonify(carto_service(id_entite))


@carto.route('/liste_cartographie_dep/<id_departement>', methods=['GET'])
def cartographie_dep(id_departement):
    return jsonify(carto_departement(id_departement))


# ============== thematique ===================
@carto.route('/liste_thematique', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_thematique():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-ai/thematique.html", profil=profil, liste_thema=list_thematique(),
                           departement=get_dep(),
                           liste_cr=liste_entite_sans_ai(), aut_id=0)


@carto.route('/ajout_thematique', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def ajout_thematique():
    if request.method == 'POST':
        libelle = request.form['libelle_thematique']
        table_thema = Thematiques(libelle)
        Sessionalchemy.add(table_thema)
        Sessionalchemy.commit()
    return redirect(url_for(template))


@carto.route('/modification_thematique', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def modification_thematique():
    id_them = request.form['id_thematique']
    thema_modif = request.form['libelle_thematique'].strip()

    thematique = Sessionalchemy.query(Thematiques).filter(Thematiques.id_thematique == id_them).first()
    thematique.libelle_thematique = thema_modif
    Sessionalchemy.commit()
    return redirect(url_for(template))


@carto.route('/modif_them<valeur>', methods=['GET'])
def modif_them(valeur):
    result = [{
        'thematique': list_one_thematique(valeur),
    }]
    return jsonify(result)


@carto.route('/debloquer_thema<valeur>', methods=['GET'])
def debloquer_thematique(valeur):
    thematique = Sessionalchemy.query(Thematiques).filter(Thematiques.id_thematique == valeur).first()
    thematique.is_active = True
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@carto.route('/bloquer_thematique<valeur>', methods=['GET'])
def bloquer_thematique(valeur):
    thematique = Sessionalchemy.query(Thematiques).filter(Thematiques.id_thematique == valeur).first()
    thematique.is_active = False
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


# ============== thematique ===================


# ============== competence ===================
@carto.route('/liste_competence', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def liste_competence():
    profil = profil_connect(session['entite_connecter'], session['code_connecter'])
    return render_template("/tableau-ai/competence.html", profil=profil, liste_competence=list_competence(),
                           liste_cr=liste_entite_sans_ai(), departement=get_dep(), aut_id=0)


@carto.route('/ajout_competence', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def ajout_competence():
    if request.method == 'POST':
        libelle = request.form['libelle_competence']
        comp = request.form['comp_cnce_it']
        is_active = True
        id_thematique = request.form['id_thematique']
        table_comp = Competences(libelle, comp, is_active, id_thematique)
        Sessionalchemy.add(table_comp)
        Sessionalchemy.commit()
    return redirect(url_for(template_comp))


@carto.route('/modification_competence', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def modification_competence():
    id_comp = request.form['id_competence']
    competence = request.form['libelle_competence'].strip()
    type_comp = request.form['comp_cnce_it'].strip()
    thematique = request.form['id_thematique'].strip()

    competence_modif = Sessionalchemy.query(Competences).filter(Competences.id_competence == id_comp).first()
    competence_modif.libelle_competence = competence
    competence_modif.comp_cnce_it = type_comp
    competence_modif.id_thematique = thematique
    Sessionalchemy.commit()
    return redirect(url_for(template_comp))


@carto.route('/modif_comp<valeur>', methods=['GET'])
def modif_comp(valeur):
    result = [{
        'competence': list_one_competence(valeur),
        'thematique': list_thematiques()
    }]
    return jsonify(result)


@carto.route('/debloquer_comp<valeur>', methods=['GET'])
def debloquer_comp(valeur):
    competence = Sessionalchemy.query(Competences).filter(Competences.id_competence == valeur).first()
    competence.is_active = True
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


@carto.route('/bloquer_comp<valeur>', methods=['GET'])
def bloquer_comp(valeur):
    competence = Sessionalchemy.query(Competences).filter(Competences.id_competence == valeur).first()
    competence.is_active = False
    Sessionalchemy.commit()
    return jsonify({'status': 'ok'})


# ============== competence ===================


# ============== notation ===================
@carto.route('/ajout_notation', methods=['GET', 'POST'])
@login_required
@access_entite_ai(access_level=['Chef de département'])
def ajout_notation():
    if request.method == 'POST':
        note = request.form['note']
        periode = request.form['periode']
        auditeur = request.form['id_auditeur']
        competence = request.form['id_competence']
        table_notation = Notation(note, periode, auditeur, competence)
        Sessionalchemy.add(table_notation)
        Sessionalchemy.commit()
    return redirect(url_for(template_carto))
# ============== notation ===================
