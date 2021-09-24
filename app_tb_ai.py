from flask import Flask, render_template, request, flash, url_for, redirect, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from urllib.parse import urlparse, urljoin
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from datetime import datetime
import os
from ldap3 import Server, Connection, SUBTREE, ALL, SAFE_SYNC

from ldap3.core.exceptions import LDAPException, LDAPBindError

from admin.app_department import admin_dep
from admin.app_personnel import admin_perso
from admin.app_service import admin_serv
from utils.bdd import Sessionalchemy, engine, Base

from utils.table_entite import Entites
from utils.table_departement import Departements
from utils.tb_ai.table_auditeurs import Auditeurs
from utils.tb_ai.table_statut import Statut
from utils.tb_ai.table_missions import Missions
from utils.tb_ai.table_suivi_activites import SuiviActivites
from utils.tb_ai.table_reporting import ReportingCodir
from utils.tb_ai.table_rapport import Rapports

from fonctions import liste_entite, liste_departement, get_fonction_by_ID
# import insertion
from ai.app_mission import mission
from cr.app_reporting import codir
from ai.app_suivi_ai import suivi_ai
from cr.app_cr import cr
from ai.app_rapport_ai import rapp_ai
from cr.app_rapport_cr import rapp_cr
from ai.app_personnel import agent
from ai.app_cartographie import carto
from ai.app_structure import struct
from admin.app_department import admin_dep
from admin.app_service import admin_serv
from admin.app_personnel import admin_perso

app = Flask(__name__)
app.config['SECRET_KEY'] = "Thissecret"
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=60)
login_manager = LoginManager(app)
login_manager.login_view = 'connexion'

app.register_blueprint(admin_dep)
app.register_blueprint(admin_perso)
app.register_blueprint(admin_serv)
app.register_blueprint(mission)
app.register_blueprint(codir)
app.register_blueprint(suivi_ai)
app.register_blueprint(cr)
app.register_blueprint(rapp_ai)
app.register_blueprint(rapp_cr)
app.register_blueprint(agent)
app.register_blueprint(carto)
app.register_blueprint(struct)

Base.metadata.create_all(engine)
Sessionalchemy = Sessionalchemy()
db = SQLAlchemy(app)
secret = URLSafeTimedSerializer('Thisisasecret!')
template_mission = 'mission.liste_mission'
template_dep = "/tableau-admin/departement.html"


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


@login_manager.user_loader
def load_user(id_auditeur):
    return Sessionalchemy.query(Auditeurs).get(int(id_auditeur))


@app.route('/', methods=['GET', 'POST'])
def connexion():
    logout_user()
    if request.method == 'POST':
        entite = request.form['login']
        code = request.form['password']
        session['entite_connecter'] = entite
        session['code_connecter'] = code
        user = Sessionalchemy.query(Auditeurs).filter(Auditeurs.login == entite).scalar()
        if user is None:
            flash("E-mail ou mot de passe incorrect.", "danger")
            return redirect(url_for('connexion'))
        else:
            if user.password == code:
                login_user(user, remember=True)
                # print(get_fonction_by_ID(user.fonction))
                if get_fonction_by_ID() == "Admin":
                    return redirect(url_for('admin_dep.liste_departement'))
                elif get_fonction_by_ID() == "Chef de département":
                    return redirect(url_for(template_mission))
                else:
                    return redirect(url_for('cr.suivi_by_cr'))

            # if user.password == code:
            #     if global_authentication(entite, code) is True:
            #         login_user(user, remember=True)
            #         if user.fonction == "Admin":
            #             return redirect(url_for('admin_dep.liste_departement'))
            #         elif user.fonction == "Chef_de_departement":
            #             return redirect(url_for(template_mission))
            #         else:
            #             return redirect(url_for('cr.suivi_by_cr'))
            #     else:
            #         flash("L'utilisateur n'existe pas.", "danger")
            #         return redirect(url_for('connexion'))

    session['next'] = request.args.get('next')
    return render_template("page-login.html", entites=liste_entite(), departements=liste_departement())


# @app.route('/creation_code_temp', methods=['GET', 'POST'])
# @login_required
# def creation_code_temp():
#     code_temp = request.form['code_temp']
#     expiration = request.form['expiration']
#     if code_temp == current_user.code_permanant:
#         flash("Le code existe déjà. Veuillez choisir un autre", "danger")
#         return redirect(url_for(template_mission))
#     elif len(code_temp) <= 5:
#         flash("Le mot de passe doit comporter au minimum 5 caractères", "danger")
#         return redirect(url_for(template_mission))
#     else:
#         code_modif = Sessionalchemy.query(Entites).filter(Entites.id_entite == current_user.id_entite).first()
#         code_modif.code_temporaire = code_temp
#         code_modif.date_debut = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         code_modif.date_fin = datetime.strptime(expiration, '%d/%m/%Y - %H:%M')
#         Sessionalchemy.commit()
#         flash("Le code temporaire est crée avec succès.", "success")
#     return redirect(url_for(template_mission))
#
#
# @app.route('/modification_code', methods=['GET', 'POST'])
# @login_required
# def modification_code():
#     entite = Sessionalchemy.query(Entites).filter(Entites.entite == current_user.entite).first()
#     if request.method == 'POST':
#         ancien_code = request.form['ancien_code']
#         confirmation_code = request.form['confirmation_code']
#         nouveau_code = request.form['nouveau_code']
#         if entite.code_permanant != ancien_code:
#             flash("L'ancien code saisi n'est pas exact", "danger")
#         elif confirmation_code != nouveau_code:
#             flash("Les informations que vous avez saisi ne correspondent pas", "danger")
#         elif entite.code_temporaire == nouveau_code:
#             flash("Le code existe déjà. Veuillez choisir un autre", "danger")
#         elif nouveau_code == entite.code_permanant:
#             flash("Le nouveau code est identique à celui de l'ancien. Veuillez le changer", "danger")
#         elif len(nouveau_code) <= 5:
#             flash("Le code d'accès doit comporter au minimum 5 caractères.", "danger")
#         else:
#             session['code_connecter'] = confirmation_code
#             entite.code_permanant = confirmation_code
#             Sessionalchemy.commit()
#             flash("Le code d'accès a été modifié avec succès.", "success")
#     return redirect(url_for(template_mission))


@app.route('/deconnexion')
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))


def check_access(entite, code):
    code_perm = Sessionalchemy.query(Entites).filter(Entites.id_entite == entite) \
        .filter(Entites.code_permanant == code).scalar()
    if code_perm == None:
        code_temp = Sessionalchemy.query(Entites).filter(Entites.id_entite == entite) \
            .filter(Entites.code_temporaire == code).scalar()
        if code_temp != None and datetime.now() > code_temp.date_fin:
            flash("Le code d'accès est expiré depuis le " + str(code_temp.date_fin.strftime('%d/%m/%Y')) + " à " + str(
                code_temp.date_fin.strftime('%H:%M')), "danger")
            return False
        elif code_temp != None and code_temp.date_fin > datetime.now():
            return True
        else:
            flash("Le code d'accès est invalide", "danger")
            return False
    else:
        return True


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join("static/assets/data/rapports/")
    return send_from_directory(directory=uploads, filename=filename)


def global_authentication(username, password):
    ldap_user_name = username.strip()
    ldap_user_password = password.strip()

    # ldap server hostname and port
    # ldap_server = f"ldap://localhost:389"
    # ldap_server = f"ldap://orange-sonatel.com:389"
    ldap_server = "ldap://10.100.55.80:389"

    server = Server(ldap_server)

    conn = Connection(server, f'orange-sonatel\\{ldap_user_name}', ldap_user_password, client_strategy=SAFE_SYNC, auto_bind=False)

    return conn.bind()[0]


""" 
cartographie competence
import pandas as pd
removed_list = [0,1,2]

#method to color-code based on condition
def color_negative_red(value):
  if value ==1:
    color = 'red'
  return 'color: %s' % color

@app.route('/table')
def display_table():
    # do something to create a pandas datatable
    df = pd.DataFrame(data=[[1,2],[3,4]])

    #df_html = df.to_html(classes='table table-bordered')  # use pandas method to auto generate html
    df.style.applymap(color_negative_red)
    df_html=df.to_html(classes='table table-bordered')
    return render_template('tableau-ai/test.html', table_html=df_html) """
if __name__ == '__main__':
    app.run(debug=True)
