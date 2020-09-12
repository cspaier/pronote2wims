import csv
import json
import re
import unidecode
from io import StringIO
from flask import Flask, redirect, request, render_template, make_response
from utils import randomStringDigits

app = Flask(__name__)


ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Teste si le fichier a la bonne extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def nettoyer(chaine):
    """Nettoie une chaîne de caractères:
    - Enlève les accents.
    - supprime les caractères non alphanumériques
    """
    sortie = unidecode.unidecode(chaine)
    sortie = ''.join(e for e in sortie if e.isalnum())
    return sortie

def id_factory(nom, prenom, form):
    """ Construit un identifiant pour une ligne élève.
    """
    style_id = form['id_select']
    #il faut enlever les tirets, les apostrophes, etc...
    prenom = nettoyer(prenom)
    nom = nettoyer(nom)
    if style_id == 'nomp':
        id = nom.replace(' ', '').lower() + prenom[0].lower()
    elif style_id == 'prenomnom':
        id = prenom.replace(' ', '').lower() + nom.replace(' ', '').lower()
    elif style_id == 'pnom':
        id = prenom[0].lower() + nom.replace(' ', '').lower()
    else:
        # Sinon, le format est "custom"
        id = form['format_id_custom']\
            .replace('$nom', nom.replace(' ', '').lower())\
            .replace('$prenom', prenom.replace(' ', '').lower())\
            .replace('$p', prenom[0].lower())
    #tests sur la longueur de l'id
    if len(id) < 4:
        erreur = 'trop court: moins de 4'
    elif len(id) > 16:
        erreur = 'trop long: plus de 16'
    else:
        erreur = None
    return id, erreur

def mdp_factory(prenom, form):
    """ Construit un mot de passe pour une ligne élève.
    """
    style_mdp = form['mdp_select']
    if style_mdp == "aleatoire":
        mdp = randomStringDigits(int(form.get("mdp_longueur")))
    elif style_mdp == "prenom":
        mdp = nettoyer(prenom).replace(' ', '')
    elif style_mdp == "fixe":
        mdp = form.get("mdp_fixe")
    #tests sur la longueur de mdp
    if len(mdp) < 4:
        erreur = 'trop court: moins de 4'
    elif len(mdp) > 16:
        erreur = 'trop long: plus de 16'
    else:
        erreur = None
    return mdp, erreur

def ligne_factory(ligne, form):
    """
    Créé les logins et mots de passe pour une ligne
    Prend en entré un dictionnaire contenant les champs 'firstname' et 'lastname'
    retourne un dictionnaire contenant les champs 'firstname', 'lastname', 'password', 'login' et 'erreur'
    """
    # on stocke les erreur dans un dict: {mdp: 'erreur du mdp', login: 'erreur du login'}
    erreur = {}
    mdp, erreur["password"] = mdp_factory(ligne['firstname'], form)
    login, erreur['login'] = id_factory(ligne['lastname'], ligne['firstname'], form)
    return {
        'firstname': ligne['firstname'],
        'lastname': ligne['lastname'],
        'password': mdp,
        'login': login,
        'erreur': erreur
    }

def csv2list(csv_list, form):
    """Transforme les données csv de pronote en liste de dictionnaire au format wims.
        Les exports pronote on une chose en commun: le premier champ est le NOM prénom
        Les headers sont variables et ils nous faut juste le premier champ.
        csv_list est une liste de champs. On chope le premier
    """
    wims_list = []
    # On ne prend pas la première ligne qui est le header variable
    for ligne in csv_list:
        # Les noms de familles sont en MAJUSCULES
        noms = re.findall(r"\b[A-Z][A-Z]+\b", ligne[0])
        nom = ' '.join(noms)
        #les entetes ou pieds de listes dont des lignes où le nom est vide : il faut les enlever
        # Ca fonctionne tant que pronote ne rajoute pas des champs non élèves contenant des mots en majuscules
        if nom == '':
            continue
        # On enlève les noms pour récupérer les prénoms
        # Note: r"\b[A-Z][a-z]+\b" trouve les mots commencant par une majuscule mais a un soucis avec les accents
        prenom = ligne[0]
        for n in noms:
            prenom = prenom.replace(n, '')
        # Le prénom commence par une majuscule
        prenom = ' '.join(re.findall(r"[A-Z].+", prenom))
        wims_list.append(ligne_factory({'lastname': nom, 'firstname': prenom}, form))
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
            csv_texte = file.read().decode('utf-8-sig').splitlines()
            reader = csv.reader(csv_texte, delimiter=";")
            wims_list = csv2list(reader, request.form)

        else:
            # pas de fichier, on travaille à partir des données json stoquées dans un champ caché. Pas beau mais ça marche.
            old_wims_list = json.loads(request.form.get("wims_json", None))
            wims_list = []
            # Il faut actualiser les champs 'password' et 'login'
            for ligne in old_wims_list:
                wims_list.append(ligne_factory(ligne, request.form))
        return render_template(
            'pronote2wims.html',
            form=request.form,
            wims_list=wims_list,
            wims_json=json.dumps(wims_list)
        )
