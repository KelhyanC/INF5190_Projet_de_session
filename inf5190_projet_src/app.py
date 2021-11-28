from genericpath import isfile
from logging import error
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask.helpers import url_for
import requests
import xml.etree.ElementTree as ET
import random
import csv
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib import request as r


app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Connexion à la BD
db = SQLAlchemy(app)


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


def load_patinoires():
    print("Chargement des patinoires : ")
    req_patinoire = requests.get(
        "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml")
    root = ET.fromstring(req_patinoire.content)
    for arrondissement in root.findall('arrondissement'):
        id = random.randint(1, 30000)
        nom_arr = str.strip(arrondissement.find('nom_arr').text)
        type = "patinoire"
        nom = str.strip(arrondissement.find('patinoire').find('nom_pat').text)
        act = Activite(id=id, type_installation=type,
                       nom=nom, arrondissement=nom_arr, ajout_bd=datetime.now())
        if(Activite.query.filter_by(nom=act.nom).first() is None):
            print("N'existe pas dans BD : ajout")
            db.session.add(act)
        print(id)
        print(nom_arr)
        print(type)
        print(nom)
        print("============")
    db.session.commit()


def load_glissades():
    print("Chargement des glissades : ")
    req_glissade = requests.get(
        "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml")
    root = ET.fromstring(req_glissade.content)
    for glissade in root.findall('glissade'):
        id = random.randint(30001, 100000)
        nom_arr = glissade.find('arrondissement').find('nom_arr').text
        type = "glissade"
        nom = glissade.find('nom').text
        act = Activite(id=id, type_installation=type,
                       nom=nom, arrondissement=nom_arr, ajout_bd=datetime.now())
        if(Activite.query.filter_by(nom=act.nom).first() is None):
            print("N'existe pas dans BD : ajout")
            db.session.add(act)
        print(id)
        print(nom_arr)
        print(type)
        print(nom)
        print("----------")
    db.session.commit()


def load_piscines():
    print("Chargement des piscines : ")
    path = 'https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv'
    dest = './data/piscines.csv'
    r.urlretrieve(path, dest)
    with open(dest, "r") as csv_piscine:
        next(csv_piscine)
        reader = csv.reader(csv_piscine, delimiter=',')
        for row in reader:
            # Pour éviter de traiter les doublons dans ID du fichier
            id = random.randint(6000000, 9999990)
            nom_arr = row[3]
            type = row[1]
            nom = row[2]
            act = Activite(id=id, type_installation=type,
                           nom=nom, arrondissement=nom_arr, ajout_bd=datetime.now())
            if(Activite.query.filter_by(nom=act.nom).first() is None):
                print("N'existe pas dans BD : ajout")
                db.session.add(act)
            print(id)
            print(nom_arr)
            print(type)
            print(nom)
            print("***********")
        db.session.commit()


if(isfile('db/database.db') == False):
    print("Base de donnée inexistante : initialisation en cours...")
    db.create_all()
    load_patinoires()
    load_glissades()
    load_piscines()
    print("Base de donnée correctement créée et chargée")


@app.route("/")
def accueil():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
