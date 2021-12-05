from genericpath import isfile
from logging import error
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import jsonify
from flask.helpers import url_for
import requests
import xml.etree.ElementTree as ET
import random
import csv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib import request as r
from apscheduler.schedulers.background import BackgroundScheduler
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError

from .schemas.update_activite import activite_update_schema

# Configuration de l'app
app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Permet de retourner du JSON en UTF-8
app.config['JSON_AS_ASCII'] = False

# Connexion à la BD
db = SQLAlchemy(app)

schema = JsonSchema(app)

# Pas possible de mettre le model BD dans un module car
# problème d'injection de dépendances entre BD, modèle et app


class Activite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_installation = db.Column(db.String, nullable=False)
    nom = db.Column(db.String, nullable=False)
    arrondissement = db.Column(db.String, nullable=False)
    ajout_bd = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, id, type_installation, nom, arrondissement, ajout_bd):
        self.id = id
        self.type_installation = type_installation
        self.nom = nom
        self.arrondissement = arrondissement
        self.ajout_bd = ajout_bd

    # Transforme le modele en objet compatible avec le format JSON
    def transformation(self):
        rep = {
            "id": str(self.id),
            "type_installation": self.type_installation,
            "nom": self.nom,
            "arrondissement": self.arrondissement,
            "ajout_bd": str(self.ajout_bd)
        }
        return rep

# Permet de lire les gros fichiers morceau par morceau
# pour prevenir les problemes memoires


def download_large_file(filename, url):
    comp_file = './data/'+filename
    with requests.get(url, stream=True) as req:
        with open(comp_file, 'wb') as f:
            for it in req.iter_content(chunk_size=1024):
                f.write(it)
    return comp_file

# Charge les patinoires a partir d'une requete GET
# et les stocke dans le fichier patinoires.xml
# Puis ajoute les patinoires dans la BD si elles n'y existent pas


def load_patinoires():
    print("Chargement des patinoires : ")
    content = download_large_file(
        'patinoires.xml', "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml")
    root = ET.parse(content)
    patinoires = []
    for arrondissement in root.findall('arrondissement'):
        id = random.randint(1, 30000)
        nom_arr = str.strip(arrondissement.find('nom_arr').text)
        type = "patinoire"
        nom = str.strip(arrondissement.find('patinoire').find('nom_pat').text)
        act = Activite(id=id, type_installation=type,
                       nom=nom, arrondissement=nom_arr, ajout_bd=datetime.now())
        if(Activite.query.filter_by(nom=act.nom).first() is None):
            print("N'existe pas dans BD : ajout")
            patinoires.append(act)
        print(id)
        print(nom_arr)
        print(type)
        print(nom)
        print("============")
    db.session.add_all(patinoires)
    db.session.commit()


# Charge les glissades a partir d'une requete GET
# et les stocke dans le fichier glissades.xml
# Puis ajoute les glissades dans la BD si elles n'y existent pas
def load_glissades():
    print("Chargement des glissades : ")
    content = download_large_file(
        'glissades.xml', "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml")
    root = ET.parse(content)
    glissades = []
    for glissade in root.findall('glissade'):
        id = random.randint(30001, 100000)
        nom_arr = glissade.find('arrondissement').find('nom_arr').text
        type = "glissade"
        nom = glissade.find('nom').text
        act = Activite(id=id, type_installation=type,
                       nom=nom, arrondissement=nom_arr, ajout_bd=datetime.now())
        if(Activite.query.filter_by(nom=act.nom).first() is None):
            print("N'existe pas dans BD : ajout")
            glissades.append(act)
        print(id)
        print(nom_arr)
        print(type)
        print(nom)
        print("----------")
    db.session.add_all(glissades)
    db.session.commit()


# Telecharge les piscines en format csv a partir d'une requete GET
# Puis les ajoute dans la BD si elles n'y existent pas
def load_piscines():
    print("Chargement des piscines : ")
    path = 'https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv'
    dest = './data/piscines.csv'
    r.urlretrieve(path, dest)
    piscines = []
    with open(dest, "r") as csv_piscine:
        next(csv_piscine)
        reader = csv.reader(csv_piscine, delimiter=',')
        for row in reader:
            # Pour éviter de traiter les doublons dans ID du fichier
            id = random.randint(6000000, 9999990) + \
                random.randint(0, 9999999)
            nom_arr = row[3]
            type = row[1]
            nom = row[2]
            act = Activite(id=id, type_installation=type,
                           nom=nom, arrondissement=nom_arr, ajout_bd=datetime.now())
            if(Activite.query.filter_by(nom=act.nom).first() is None):
                print("N'existe pas dans BD : ajout")
                piscines.append(act)
            print(id)
            print(nom_arr)
            print(type)
            print(nom)
            print("***********")
        db.session.add_all(piscines)
        db.session.commit()


# Fonction du Background Scheduler qui ajoute les patinoires, glissades et pisines
# qui n'existent pas dans la BD
def load_datas_scheduler():
    print("Mise à jour période des données tous les jours à 00:00 :")
    load_patinoires()
    load_glissades()
    load_piscines()
    print("Mise à jour périodique terminée")


# Vérifie si la base de donnée existe, sinon la crée et charge toutes les données
# Le chargement des données peut être long
if(isfile('db/database.db') == False):
    print("Base de donnée inexistante : initialisation en cours...")
    db.create_all()
    load_patinoires()
    load_glissades()
    load_piscines()
    print("Base de donnée correctement créée et chargée")

# Charge les données inexistante dans la BD tous les jours à minuit
scheduler = BackgroundScheduler()
job = job = scheduler.add_job(
    load_datas_scheduler, 'cron', day_of_week='mon-sun')
scheduler.start()


# AFFICHER LES 3 DERNIERES DONNEES MAJ DE CHAQUE CATEGORIE PAR BACKGROUND SCHEDULER

@app.errorhandler(JsonValidationError)
def validation_error(err):
    errors = [validation_error.message for validation_error in err.errors]
    return jsonify({'Erreur': err.message, 'Details_erreur': errors}), 400


@app.route("/")
def accueil():
    installations = Activite.query.all()
    return render_template("index.html", installations=installations)


@app.route("/doc")
def read_the_doc():
    return render_template("doc.html")


@app.route("/api/installations")
def get_installations():
    arr = request.args['arrondissement']
    arrondissements = Activite.query.filter(
        Activite.arrondissement.ilike(arr)).all()
    if arr.strip() == "" or not arr or arrondissements is None or len(arrondissements) == 0:
        return jsonify({"Erreur": "Arrondissement invalide"}), 404
    else:
        print(arrondissements)
        return jsonify([it.transformation() for it in arrondissements]), 200


@app.route("/api/installation/<id>", methods=["GET", "PATCH", "DELETE"])
@schema.validate(activite_update_schema)
def get_installation(id):
    installation = Activite.query.filter_by(id=id).first()
    if(installation is None):
        return jsonify({"Erreur": "Aucune installation ne correspond à cet identifiant"}), 404
    elif request.method == "GET":
        return jsonify(installation.transformation()), 200
    elif request.method == "PATCH":
        req_data = request.get_json()
        name = req_data['nom']
        type_inst = req_data['type_installation']
        if name.strip() == "" or type_inst.strip() == "":
            return jsonify({"Erreur": "Les données fournies ne peuvent pas être vides"}), 400
        Activite.query.filter_by(id=id).update(
            dict(nom=name, type_installation=type_inst, ajout_bd=datetime.now()))
        db.session.commit()
        new_data = Activite.query.filter_by(id=id).first().transformation()
        return jsonify(new_data), 200
    elif request.method == "DELETE":
        del_data = installation.transformation()
        Activite.query.filter_by(id=id).delete()
        db.session.commit()
        return jsonify(del_data), 200


if __name__ == "__main__":
    app.run(debug=True)
