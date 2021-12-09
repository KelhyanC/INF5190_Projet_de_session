# INF5190 - Projet de session

# Auteur
- Nom : CARMONT
- Prénom : Kelhyan
- Code Permanent : CARK68120101

# Parcours
A1 -> A2 -> A3 -> A4 -> A5 -> A6 -> D1 -> D2 -> D3 -> D4 (avec request http basic auth)

Total de 115XP effectués

remarque : Les termes installations et activités sont équivalents dans ce projet. Dans le fichier `app.py`, j'ai effectué des print à certains moments, pour que vous puissiez avoir un aperçu de ce qu'il se passe.

Vous pouvez utiliser la commande `make` dans le répertoire du code source, pour lancer l'application.

J'ai donné accès à [mon repo Git](https://github.com/KelhyanC/INF5190_Projet_de_session) à Jacques Berger au cas où vous en aurez besoin.

# A1 - 15 XP

Pour la modélisation des données, j'ai gardé les données communes parmis tous les datasets.
J'ai gardé uniquement celle dont j'avais besoin pour réaliser mes fonctionnalités, le schéma de données est le suivant :
- `id` : l'identifiant
- `type_installation` : le type d'installation (piscine, patinoire, glissade...)
- `nom` : le nom de l'installation
- `arrondissement` : l'arrondissement de l'installation
- `ajout_bd` : la date d'ajout/modification de l'installation dans la BD

En lançant l'application Flask, le programme vérifie l'existance de la BD, quand je vous remettrai ce projet, la BD existera déjà
pour vous faire gagner du temps. Si vous voulez que l'application crée la BD, vous n'avez qu'à supprimer tous les fichiers `.xml, .csv` dans le répertoire `data` et le fichier `database.db` dans le répertoire `db`.
Si la BD n'existe pas, on la crée et on y charge les données, elle se situe dans le répertoire db.
Le fichier piscines.csv est téléchargé et stocké dans le répertoire data,
ainsi que les fichiers patinoires et glissades .xml. Il faut que le programme ait tous les droits dans le répertoire pour n'avoir aucun soucis d'exécution car il interragit avec le système de fichiers de la machine sur laquelle il est exécuté.
Il n'y a pas de script SQL utilisé pour initialiser la BD, celle-ci est créée et modélisée à travers l'application Flask avec SQLAlchemy

# A2 - 5 XP

La mise à jour des données est faite tous les jours automatiquement à l'aide d'un BackgroundScheduler. J'ai pu remarquer que l'application Flask doit être en cours d'exécution à minuit `UTC` pour voir la fonction s'exécuter. Vous pouvez consulter dans le fichier `app.py` ligne 204 afin de voir l'implémentation du BackgroundScheduler.

# A3 - 5 XP

Le document `doc.html` dans le répertoire `templates` a été généré à partir du fichier `doc.raml` avec l'utilitaire npm `raml2html`.
Pour des raisons d'incompatibilité et de manque de configuration avec l'environnement d'exécution vagrant fourni, j'ai appelé l'utilitaire en dehors de l'environnement sur ma machine locale.

Rendez-vous à la route `/doc` pour voir le résultat.

# A4 - 10 XP

En effectuant une requête `GET` sur l'url `/api/installations?arrondissement=nomArrondissement`
L'application retournne la liste des installations par nom d'arrondissement, en cas du succès les installations sont retournées sous format de tableau JSON, sinon retourne un message d'erreur.
J'ai facilité la recherche d'installations par arrondissement, en permettant l'insensibilité à la case du paramètre du Query String lors de la recherche dans la BD.
Vous pouvea utiliser le client REST de votre choix (ex: PostMan) ou utiliser un navigateur.

Remarque : Remplacer "nomArrondissement" par le vrai nom de l'arrondissement (ex: verdun, lasalle...etc) -> `GET /api/installations?arrondissement=verdun` .

# A5 - 10 XP

En vous rendant sur la route principale `/`, vous pouvez saisir un arrondissement dans la barre recherche, la recherche est insensible à la casse.
En cas de succès, les installations sont retournées sous forme de tableau, sinon retourne un message d'erreur avec une image. J'ai utilisé le `fetch API` dans le fichier `index.js` pour effectuer la requête asynchrone des installations sur l'API cité en A4. Un loader et un message apparaîssent pendant le chargement, si la requête est efficace vous le verrez à peine.

# A6 - 10 XP

En se rendant sur la route principale `/`, l'application charge toutes les installations à partir de la BD.
Sur la page d'accueil, vous verrez un sélecteur par nom d'installation. En sélectionnant l'installation et en cliquant sur trouver, une requête GET asynchrone est faite sur l'api `/api/installation/<id>`. Le même mécanisme de loading est fait comme pour A5, et les informations sur l'installation sont affichées. 

Bien évidemment vous pouvez tester l'API avec un client REST ou en tapant l'url dans le navigateur pour avoir un retour des données en format JSON.
Une installation avec un ID invalide retourne une erreur.

Remarque : Pour avoir un identifiant d'installation valide, cherchez une installation dans la liste déroulante, son ID y sera présenté dans ses informations affichées.

# D1 - 15 XP

En utilisant un client REST, appelez une méthode PATCH sur l'url `/api/installation/<id>`, fournissez une entrée JSON avec comme contenu dans le body le `type_installation` ainsi que le `nom` de l'installation, vous êtes libre d'y mettre le contenu que vous voulez tant que le format est sous forme de `string`. Les autres champs ne sont pas permis car nous ne pouvons pas créer un nom d'arrondissement imaginaire, ni changer l'ID pour éviter d'avoir des conflits dans la BD. La date `ajout_bd` est mise à jour, avec la date et l'heure à laquelle vous effectuez cette modification avec PATCH. En cas d'erreur dans le body fourni ou d'ID invalide, une erreur vous sera retournée, sinon le nouvel objet mis à jour avec tous ses champs vous sera retourné à titre informatif. Vous pouvez également modifier une installation via l'interface de l'application en effectuant une recherche par arrondissement.

Exemple de body JSON :

```json
{
    "type_installation": "Type Test",
    "nom" : "Un Nom Imaginaire"
}
```

# D2 - 5 XP

En utilisant un client REST, appelez une méthode `DELETE` sur l'url `/api/installation/<id>`, Si tout s'est bien passé, un élément json vous sera retourné avec l'élément supprimé, sinon un message d'erreur vous sera retourné.

Vous pouvez également tester cette fonctionnalité sur l'interface graphique de l'application, en effectuant une recherche par nom d'arrondissement, un tableau s'affichera avec un bouton supprimer pour chaque élément du tableau, faites-vous alors plaisir.

Remarque : Cette fonctionnalité requiert l'authentification, référez-vous à la section `D4` pour plus d'informations.

# D3 - 20 XP

En effectuant une recherche par arrondissement, la liste des installations s'affiche sous forme de tableau et vous pouvez modifier ou supprimer une installation. Les services faits en D1 et D2 sont invoqués et un message de confirmation est affiché pour chaque opération effectué.

Pour la modification, après avoir cliqué sur le bouton modifier, un formulaire vous sera affiché avec tous les champs grisés, sauf ceux modifiables. Une validation sera faite dépendemment de si vous y entrez des champs valide, un champs ne peut pas être vide. Une fois soumis, le bouton de soumission disparaît, un message de confirmation s'affiche et les informations de l'installation modifiée sont présentées dans un formulaire désactivé.

# D4 - 20 XP

J'ai implémenté une procédure d'authentification de type "Basic Auth" avec le module `request` de Flask.

En utilisant un client REST, si vous effectuez un DELETE sur une installation sans être authentifié, une erreur vous sera retournée.
Assurez-vous de vous authentifier sur votre client REST.

Vous pouvez également tester l'authentification dans l'application en effectuant une recherche par nom d'arrondissement. En cliquant sur le bouton supprimer, l'invite de votre navigateur vous demandera votre `username` et `password` , entrez-y les informations de connexion données ci-dessous. Les identifiants de connexion vous seront demandés tant qu'il ne sont pas valide, et si vous faites Cancel, vous n'aurez pas l'autorisation de supprimer une installation.

Vous pouvez aussi vérifier dans le fichier `app.py` l'objet `loginfo`, les informations de connexion y sont spécifiées. Vous pouvez les modifier au besoin pour expérimenter.
Votre navigateur peut stocker les données de connexion, et la saisie des identifiants ne serait plus nécessaire par la suite pour
supprimer une installation. Dans ce cas, vous pouvez soit supprimer les données de navigation, soit modifier les champs `username` et `password` dans l'objet loginfo, ou soit dire merci à votre navigateur et profiter de ne plus vous faire embêter par les procédures d'authentification.

Informations d'authentification :
username : `superuser`
password : `secret`