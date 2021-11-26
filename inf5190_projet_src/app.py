from logging import error
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask.helpers import url_for
from .db.database import Database
import requests
import xml.etree.ElementTree as ET
import random
import csv

app = Flask(__name__, static_url_path="", static_folder="static")


# Connexion à la BD

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# Fermeture de la connexion

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


# Route principale, s'il n'y a pas d'article dans la BD
# retourne un message en conséquence pour en créer un
# Sinon retourne au plus 5 article, par date décroissante

@app.route("/")
def accueil():
    load_patinoires()
    load_glissades()
    load_piscines()
    return render_template("index.html")


def load_patinoires():
    print("Chargement des patinoires : ")
    req_patinoire = requests.get(
        "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml")
    root = ET.fromstring(req_patinoire.content)
    for arrondissement in root.findall('arrondissement'):
        id = random.randint(1, 30000)
        nom_arr = arrondissement.find('nom_arr').text
        type = "patinoire"
        nom = arrondissement.find('patinoire').find('nom_pat').text
        # Ajout BD
        print(id)
        print(nom_arr)
        print(type)
        print(nom)
        print("----------")


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
        # Ajout BD
        print(id)
        print(nom_arr)
        print(type)
        print(nom)
        print("----------")


def load_piscines():
    print("Chargement des piscines : ")
    with open("./data/piscines.csv", "r") as csv_piscine:
        next(csv_piscine)
        reader = csv.reader(csv_piscine, delimiter=',')
        for row in reader:
            id = random.randint(
                6000000, 9000000) if row[0] == "0" else int(row[0])
            nom_arr = row[3]
            type = row[1]
            nom = row[2]
            # Ajout BD
            print(id)
            print(nom_arr)
            print(type)
            print(nom)
            print("----------")


if __name__ == "__main__":
    app.run(debug=True)
