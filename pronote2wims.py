from flask import Flask, flash, redirect, request, render_template
from werkzeug.utils import secure_filename
from utils import randomStringDigits
import csv
app = Flask(__name__)
import re

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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

        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #print(file.read().decode('utf-8'))
            reader = csv.DictReader(file.read().decode('utf-8-sig').splitlines(), delimiter=";")
            wims_dict = []
            style_mdp = request.form.get("mdp_select")

            for ligne in reader:
                # Les noms de familles sont en MAJUSCULES
                nom = ' '.join(re.findall(r"\b[A-Z][A-Z]+\b", ligne["Élève"]))
                # On enlève le nom de la ligne et l'espace du début
                prenom = ligne["Élève"].replace(nom, '')[1:]
                if style_mdp == "aleatoire":
                    mdp = randomStringDigits(int(request.form.get("mdp_longueur")))
                elif style_mdp == "fixe":
                    mdp = request.form.get("mdp_fixe")
                else:
                    mdp = ligne['Né(e) le'].replace('/','')
                wims_dict.append({
                    "lastname": nom,
                    "firstname": prenom,
                    "password": mdp
                })
                # vue de téléchargement csv

            return render_template('pronote2wims.html', form=request.form, file=request.files, wims_dict=wims_dict)
