## pronote2wims

Conversion de données pronote vers csv pour usage dans wims.

Hébergé sur https://pronote2wims.herokuapp.com/

## Déploiement local

1. créer un environement virtuel python: `virtualenv -P python3 venv`
2. l'activer: `source venv/bin/activate`
3. cloner le dépot git: `git clone https://github.com/cspaier/pronote2wims.git`
4. se placer dans le dossier du dépot: `cd pronote2wims`
5. installer les dépendances:`pip install -r requirements.txt`
5. indiquer le nom de l'app flask: `export FLASK_APP=pronote2wims.py`
6. activer le mode débug de flask: `export FLASK_ENV=development`
7. lancer le serveur local: `python -m flask run`

Normalement on a un retour du type:
```
 * Serving Flask app "pronote2wims.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```
Ouvrir l'url http://127.0.0.1:5000/ pour tester.
