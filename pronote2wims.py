import csv
import json
import re
from io import StringIO
from flask import Flask, redirect, request, render_template, make_response
from utils import randomStringDigits

app = Flask(__name__)


ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Teste si le fichier a la bonne extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def desaccent(mot):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'],
                    'A': ['À', 'Ã', 'Á', 'Â'],
                    'E': ['É', 'È', 'Ê', 'Ë'],
                    'I': ['Î', 'Ï'],
                    'U': ['Ù', 'Ü', 'Û'],
                    'O': ['Ô', 'Ö']}

        for (char, accented_chars) in accents.items():
            for accented_char in accented_chars:
                mot = mot.replace(accented_char, char)
        return mot
    
def id_factory(nom, prenom, form):
    """ Construit un identifiant pour une ligne élève.
    """
    style_id = form['id_select']
    #il faut enlever les tirets, les apostrophes, etc...
    prenom2 = desaccent(prenom)
    prenom2 = re.sub('[\W_ ]+', '', prenom2)
    nom2 = desaccent(nom)
    nom2 = re.sub('[\W_ ]+', '', nom2)
    if style_id == 'nomp':
        id = nom2.replace(' ', '').lower() + prenom2[0].lower()
    elif style_id == 'prenomnom':
        id = prenom2.replace(' ', '').lower() + nom2.replace(' ', '').lower()
    elif style_id == 'pnom':
        id = prenom2[0].lower() + nom2.replace(' ', '').lower()
    else: 
        # Sinon, le format est "custom"
        id = form['format_id_custom']\
            .replace('$nom', nom2.replace(' ', '').lower())\
            .replace('$prenom', prenom2.replace(' ', '').lower())\
            .replace('$p', prenom2[0].lower())
    #tests sur la longueur de l'id
    if len(id) < 4:
        id = id+'IDENTIFIANT_TROP_COURT_(4_caract_min)'
    elif len(id) > 16:
        id = id+'IDENTIFIANT_TROP_LONG_(16_caract_max)'
    return id

def mdp_factory(ligne, form):
    """ Construit un mot de passe pour une ligne élève.
    """
    style_mdp = form['mdp_select']
    if style_mdp == "aleatoire":
        mdp = randomStringDigits(int(form.get("mdp_longueur")))
    elif style_mdp == "prenom":
        nom = ' '.join(re.findall(r"\b[A-Z][A-Z]+\b", ligne["Élève"]))
        # On enlève le nom de la ligne et l'espace du début
        prenom = ligne["Élève"].replace(nom, '')[1:]
        #on enlève le non alphanumérique
        prenom = re.sub('[\W_ ]+', '',prenom)
        #on met en minuscules et sans accent
        prenom = prenom.lower()
        prenom = desaccent(prenom)
        mdp = prenom
    elif style_mdp == "fixe":
        mdpget = form.get("mdp_fixe")
        if mdpget == '':
            mdpget = 'bonjour'
        mdp = mdpget
    else :
        # Sinon, le style est "date de naissance"
        mdp = ligne['birthday'].replace('/', '')
    #tests sur la longueur de mdp
    if len(mdp) < 4:
        mdp = mdp+'PASSWORD_TROP_COURT_(4_caract_min)'
    elif len(mdp) > 16:
        mdp = mdp+'PASSWORD_TROP_LONG_(16_caract_max)'
    return mdp

def csv2list(csv_list, form):
    """Transforme les données csv de pronote en liste de dictionnaire au format wims."""
    wims_list = []
    for ligne in csv_list:
        # Les noms de familles sont en MAJUSCULES
        nom = ' '.join(re.findall(r"\b[A-Z][A-Z]+\b", ligne["Élève"]))
        # On enlève le nom de la ligne et l'espace du début
        prenom = ligne["Élève"].replace(nom, '')[1:]
        mdp = mdp_factory(ligne, form)
        login = id_factory(nom, prenom, form)
        #les entetes ou pieds de listes dont des lignes où le nom est vide : il faut les enlever
        if nom != '' :
            wims_list.append({
                "lastname": nom,
                "firstname": prenom,
                "password": mdp,
                "birthday": ligne['birthday'],
                "login": login
            })
    return wims_list

@app.route('/telecharger/', methods=['POST'])
def telecharger():
    """Télécharge un fichier csv construit à partir des données json"""
    # On récupère les données JSON que l'on convertit en object python
    wims_list = json.loads(request.form.get("wims_json", None))
    # Pour wims, on n'utilisera que les champs suivants. On omet le champ "birthday"
    fieldnames = ['login', 'firstname', 'lastname', 'password']
    si = StringIO()
    writer = csv.DictWriter(si, fieldnames=fieldnames)
    writer.writeheader()
    # On écrit les lignes dans le csv
    for ligne in wims_list:
        writer.writerow({key: ligne[key] for key in fieldnames})
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=wims.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    La vue principale de notre application.
    Au départ, par GET, on a le formulaire vide qui permet d'envoyer un fichier csv.
    Quand un fichier est envoyé, on le convertit en une liste de dictionnaires:
        [{"firstname": prenom,
          "lastname": nom,
          "login": identifiant,
          "birthday": date_de_naissance,
          "password": mot_de_passe},
          ...
         ]
    On conserve le champ "birthday" car il peut être utile pour la création du mot de passe.
    On stocke cette liste dans un (oups deux) champs de formulaires cachés en JSON.
    L'utilisateur peut renvoyer le formulaire en POST sans renvoyer de fichier csv si il souhaite,
    par exemple, changer les formats des identifiants et mots de passe.
    On utilise alors les données JSON mentionnées ci-dessus qui sont transmises par POST.
    """
    # Au départ on arrive avec GET
    if request.method == "GET":
        # On initialise le formulaire
        form = {
            "mdp_select": "fixe",
            "mdp_fixe": "",
            "mdp_longueur": 6,
            "file": None
        }
        return render_template('pronote2wims.html', form=form)

    if request.method == 'POST':
        # L'utilisateur a envoyé le formulaire
        # On test si un fichier est présent
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if not(file and allowed_file(file.filename)):
                return redirect(request.url)
            # on remplace 'Né(e) le' par 'birthday' pour pouvoir utiliser directement mdp_factory
            csv_texte = file.read().decode('utf-8-sig').replace('Né(e) le', 'birthday').splitlines()
            reader = csv.DictReader(csv_texte, fieldnames=['Élève','birthday'], delimiter=";")
            wims_list = csv2list(reader, request.form)

        else:
            # pas de fichier, on travaille à partir des données json stoquées dans un champ caché. Pas beau mais ça marche.
            wims_list = json.loads(request.form.get("wims_json", None))
            # Il faut actualiser les champs 'password' et 'login'
            for ligne in wims_list:
                ligne['password'] = mdp_factory(ligne, request.form)
                ligne['login'] = id_factory(ligne['lastname'], ligne['firstname'], request.form)
        return render_template(
            'pronote2wims.html',
            form=request.form,
            wims_list=wims_list,
            wims_json=json.dumps(wims_list)
        )
