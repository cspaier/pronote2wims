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
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 172-164-488

```
Ouvrir l'url http://127.0.0.1:5000/ pour tester.

## TODO
Voir issues
