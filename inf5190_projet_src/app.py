from logging import error
from flask import Flask
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask.helpers import url_for
from .database.database import Database

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
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
