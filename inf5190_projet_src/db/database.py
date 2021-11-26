import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    # Transforme un curseur BD en dictionnaire
    def transform_to_dic(self, dic_name, cursor):
        return[dict(dic_name) for dic_name in cursor.fetchall()]

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/db.db')
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Retourne les 5 articles les plus récents
    def get_min_publications(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            """SELECT * FROM article
            WHERE datetime(date_publication) <= datetime('now')
            ORDER BY datetime(date_publication) DESC
            LIMIT 5""")
        return self.transform_to_dic("articles", cursor)

    # Cherche un article à partir d'un pattern
    def search_article(self, pattern):
        cursor = self.get_connection().cursor()
        cursor.execute(f"""SELECT titre,identifiant,date_publication
        FROM article
        WHERE titre LIKE '%{pattern}%' OR paragraphe LIKE '%{pattern}%'""")
        return self.transform_to_dic("articles", cursor)

    # Retourne un article à partir d'un identifiant
    def get_article(self, identifiant):
        cursor = self.get_connection().cursor()
        cursor.execute(
            f"""SELECT * FROM article
            WHERE identifiant='{identifiant}' """)
        return self.transform_to_dic("article", cursor)

    # Retourne tous les articles de la BD
    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM article")
        return self.transform_to_dic("articles", cursor)

    # Met à jour le titre et le paragraphe d'un article
    def update_article(self, identifiant, titre, paragraphe):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute((f"""UPDATE article SET titre=?, paragraphe=?
                        WHERE identifiant='{identifiant}'"""),
                       (titre, paragraphe))
        connection.commit()

    # Insert un article dans la BD à partir d'un objet Article
    def insert_article(self, article):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("""INSERT INTO article(id, titre, identifiant,
         auteur, date_publication, paragraphe) VALUES(?, ?, ?, ?, ?, ?)"""),
                       ([article['id'], article['titre'],
                         article['identifiant'], article['auteur'],
                         article['date_publication'], article['paragraphe']]))
        connection.commit()
