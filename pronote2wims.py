from flask import Flask, flash, redirect, request, render_template
from werkzeug.utils import secure_filename
from utils import randomStringDigits
import csv
import json
app = Flask(__name__)
import re

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def id_factory(nom, prenom, form):
    """ Construit un identifiant pour une ligne élève.
    """
    style_id = form['id_select']
    if style_id == 'prenomnom':
        return prenom.replace(' ', '').lower() + nom.replace(' ', '').lower()
    if style_id == 'pnom':
        return prenom[0].lower() + nom.replace(' ', '').lower()
    return form['format_id_custom']\
        .replace('$nom', nom.replace(' ', '').lower())\
        .replace('$prenom', prenom.replace(' ', '').lower())\
        .replace('$p', prenom[0].lower())



def mdp_factory(ligne, form):
    """ Construit un mot de passe pour une ligne élève.
    """
    style_mdp = form['mdp_select']
    if style_mdp == "aleatoire":
        return randomStringDigits(int(form.get("mdp_longueur")))
    if style_mdp == "fixe":
        return form.get("mdp_fixe")
    return ligne['birthday'].replace('/','')

def csv2list(csv_list, form):
    wims_list = []
    for ligne in csv_list:
        # Les noms de familles sont en MAJUSCULES
        nom = ' '.join(re.findall(r"\b[A-Z][A-Z]+\b", ligne["Élève"]))
        # On enlève le nom de la ligne et l'espace du début
        prenom = ligne["Élève"].replace(nom, '')[1:]
        mdp = mdp_factory(ligne, form)
        id = id_factory(nom, prenom, form)
        wims_list.append({
            "lastname": nom,
            "firstname": prenom,
            "password": mdp,
            "birthday": ligne['birthday'],
            "id": id
        })
    return wims_list



@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "GET":
        form = {
            "mdp_select": "fixe",
            "mdp_fixe": "",
            "mdp_longueur": 6,
            "file": None
        }
        return render_template('pronote2wims.html', form=form)
    if request.method == 'POST':
        # On test si un fichier est présent
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if not(file and allowed_file(file.filename)):
                return redirect(request.url)
            # on commence par remplacer les noms des champs par le format wims
            csv_texte = file.read().decode('utf-8-sig').replace('Né(e) le', 'birthday').splitlines()
            reader = csv.DictReader(csv_texte, delimiter=";")
            wims_list = csv2list(reader, request.form)

        else:
            # pas de fichier, on travail à partir des données json stoquées dans un champ caché. Pas beau mais ca marche.
            wims_list = json.loads(request.form.get("wims_json", None))
            for ligne in wims_list:
                ligne['password'] = mdp_factory(ligne, request.form)
                ligne['id'] = id_factory(ligne['lastname'], ligne['firstname'], request.form)

            # vue de téléchargement csv

        return render_template('pronote2wims.html', form=request.form, wims_list=wims_list, wims_json=json.dumps(wims_list))
