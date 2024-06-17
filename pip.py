import mysql.connector
from flask import Flask, request, jsonify,render_template
import PyPDF2
import pyttsx3
import requests
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
parametres_connexion = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'database': 'pfe'
}

@app.route('/chercher_url', methods=['GET'])
def chercher_url():
    # Récupérer l'URL local depuis les paramètres de la requête
    url = request.args.get('url')

    # Établir la connexion à la base de données
    connexion = mysql.connector.connect(**parametres_connexion)
    curseur = connexion.cursor()

    # Exécuter la requête SQL pour récupérer le chemin associé à l'URL local
    requete_sql = "SELECT path FROM pfe_test WHERE path = %s"
    curseur.execute(requete_sql, (url,))
    resultat = curseur.fetchone()

    # Fermer la connexion à la base de données
    connexion.close()

    # Vérifier si un résultat a été trouvé
    if resultat:
        path = resultat[0]
        # Lecture audio du contenu du PDF
        contenu_pdf = extraire_contenu_pdf(path)
        lire_audio(contenu_pdf)
        return render_template('afficherPdf.html', texte=contenu_pdf)
    else:
        return jsonify({"message": "L'URL local n'existe pas dans la base de données"}), 404

def extraire_contenu_pdf(url_pdf):
    texte_pdf = ""
    response = requests.get(url_pdf)
    with open("temp.pdf", "wb") as fichier_temporaire:
        fichier_temporaire.write(response.content)
    with open("temp.pdf", "rb") as fichier_pdf:
        lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
        for page_num in range(len(lecteur_pdf.pages)):
            page = lecteur_pdf.pages[page_num]
            texte_pdf += page.extract_text()
            print(texte_pdf)
    return texte_pdf


def lire_audio(texte):
    moteur_audio = pyttsx3.init()
    moteur_audio.say(texte)
    moteur_audio.runAndWait()
    
if __name__ == '__main__':
    app.run(debug=True, port=5003)
