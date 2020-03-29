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

def mdp_factory(ligne, form):
    style_mdp = form['mdp_select']
    if style_mdp == "aleatoire":
        return randomStringDigits(int(form.get("mdp_longueur")))
    if style_mdp == "fixe":
        return form.get("mdp_fixe")
    return ligne['birthday'].replace('/','')

def csv2dict(csv_dict, form):
    wims_list = []
    for ligne in csv_dict:
        # Les noms de familles sont en MAJUSCULES
        nom = ' '.join(re.findall(r"\b[A-Z][A-Z]+\b", ligne["Élève"]))
        # On enlève le nom de la ligne et l'espace du début
        prenom = ligne["Élève"].replace(nom, '')[1:]
        mdp = mdp_factory(ligne, form)
        wims_list.append({
            "lastname": nom,
            "firstname": prenom,
            "password": mdp,
            "birthday": ligne['birthday']
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
        # if user does not select file, browser also
        # submit an empty part without filename

        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if not(file and allowed_file(file.filename)):
                return redirect(request.url)
            reader = csv.DictReader(file.read().decode('utf-8-sig').replace('Né(e) le', 'birthday').splitlines(), delimiter=";")
            wims_list = csv2dict(reader, request.form)
        else:
            # pas de fichier, on travail à partir des données json
            wims_list = json.loads(request.form.get("wims_json", None))
            for line in wims_list:
                line['password'] = mdp_factory(line, request.form)
                print(line)

            # vue de téléchargement csv

        return render_template('pronote2wims.html', form=request.form, wims_list=wims_list, wims_json=json.dumps(wims_list))
