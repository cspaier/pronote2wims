from os import listdir
from os.path import splitext

nomfichier = "tousAziza.csv"
numeroGroupementWims="2772584"


#Comment utiliser ce fichier :
#- Python doit être installé sur votre ordinateur
#- copier la liste d'élèves depuis pronote et collez-là dans un fichier .csv :
#la première colonne doit contenir les "nom'espace'prénom" des élèves
#la première ligne doit contenir le numéro de la classe de destination dans wims
#- indiquer ci-dessus le nom de votre fichier csv
#- il est possible de mettre plusieurs classes les unes en dessous des autres en les séparant à chaque fois par une ligne contenant le numéro de la classe de destination dans wims
#- exécuter ce fichier python : un fichier csv sera créé avec le même nom de fichier que le nom initial suivi de "-MisEnFormePourWims"

def suppr(ligne):
        """ supprime les accents du texte source """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'],
                    '': ["'", '-']}

        for (char, accented_chars) in accents.items():
            for accented_char in accented_chars:
                ligne = ligne.replace(accented_char, char)
        return ligne


nomfich = nomfichier.split(".")[0]+"-MisEnFormePourWims.csv"

f=open(nomfich, "w")
f.write("login,firstname,lastname,password,participate")

with open(nomfichier, "r") as mon_fichier:
    contenu = mon_fichier.read()
contenu=contenu.replace('  ',' ')
contenu=contenu.split('\n')
contenu.pop()#enl&egrave;ve le dernier &eacute;l&eacute;ment (une ligne vide)
for line in range(len(contenu)):
    initialeok=False
    ligne=contenu[line].split()
    n=len(ligne)
    if n==1 :
        numClasse=str(ligne[0])
    else :
        lastname=""
        login=""
        firstname=""
        password=""
        for j in range(n) :
            if suppr(ligne[j]).isupper():   #tant que le mot est entièrement en majuscules, c'est qu'il fait partie du nom de famille
                lastname+=ligne[j]
                login+=suppr(ligne[j].lower())       #on met le nom en minuscules dans le login
            elif suppr(ligne[j]).isalpha():   #tant que le mot ne contient que des caractères alphabétiques, mais pas tous en majuscules c'est le prénom
                if not initialeok :
                    login=login+suppr(ligne[j].lower())[0]  #on rajoute l'initiale du prénom à la fin du login
                    initialeok=True
                firstname+=ligne[j]
                password+=suppr(ligne[j].lower())
        l=len(login)
        if l<4:
            login=login+"1"*(4-l)
            print("Attention : le login de "+firstname+" "+lastname+" est : "+login)
        l=len(password)
        if l<4:
            password=password+"1"*(4-l)
            print("Attention : le password de "+firstname+" "+lastname+" est : "+password)
        lineOut=login+","+firstname+","+lastname+","+password+","+numeroGroupementWims+"/"+numClasse
        f.write("\n"+lineOut)
f.close()

        #     contenu.pop()#enl&egrave;ve le dernier &eacute;l&eacute;ment (une ligne vide)
#
#
#     listelog=[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]#va contenir les textes exo par exo
#     listesession=[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]#va contenir les num session exo par exo
#
#
#     for line in range(len(contenu)):
#         ligne=LigneLog(contenu[line])
#         if line+1<len(contenu):
#             ligne2=LigneLog(contenu[line+1])
#             duree=ligne2.time-ligne.time
#             if ligne2.date != ligne.date :
#                 duree=1000000
#         if(ligne.sheet==feuille):
#             exo=ligne.exercise
#             if(exo>len(listelog)):
#                 print("Attention : exercices non pris en compte car la taille de listelog se limite à 13 exercices...")
#
#             if str(ligne.session)!=str(listesession[exo-1]):
#                 listesession[exo-1]=ligne.session
#                 listelog[exo-1]+="<br />Le "+ligne.date[6:8]+"/"+ligne.date[4:6]+"/"+ligne.date[0:4]+" &agrave; partir de "+ligne.timetext+" : "
#
#             font1="<font color='red'>"
#             font2="</font>"
#             if(ligne.sc):
#                 font1="<font color='green'><b>"
#                 font2="</b></font>"
#             c=" &ndash;" #tiret court
#             if duree<60:
#                 c=" &middot;" #point si recherche de moins d'une minute
#             if duree>300:
#                 c=" &mdash;" #tiret long si recherche de plus de 5 minutes
#             if(ligne.type=="score"):
#                 c=str(ligne.score)+" "
#                 c=c.replace(".0"," ")
#             listelog[exo-1]+=font1+c+font2
#
#     f.write("<p><b><u><i>Travail sur WIMS : </i></u></b> feuille n&deg;"+str(feuille)+"</p>")
#     f.write("<p style='page-break-after:avoid'><b><u><i>Nom de login : </i></u></b> "+nom+"</p>")
#     f.write("<p style='page-break-after:avoid'><b><u><i>L&eacute;gende : </i></u></b> Chaque tiret indique la visualisation d'un nouvel &eacute;nonc&eacute; (un tiret long indique une recherche de plus de 5 minutes et un point une recherche de moins d'une minute).<br />")
#     f.write("Chaque nombre indique un score obtenu.<br />")
#     f.write("La <font color='green'><b> couleur verte </b></font> indique que l'enregistrement des notes est activ&eacute;.<br />")
#     f.write("La <font color='red'> couleur rouge </font> indique que l'enregistrement des notes est d&eacute;sactiv&eacute;. </p><p style='page-break-after:avoid'>")
#     for i in range(14):
#         if(listelog[i] != " "):
#             f.write(" <b><u><i>Exercice n&deg;"+str(i+1)+" : </i></u></b>"+listelog[i]+"<br />")
#     f.write("</p><p style='page-break-after:avoid'><b><u><i>Commentaires : </i></u></b><br /><br /><hr></p>")
# f.write("</body></html>")



# class LigneLog:
#     #chaque ligne de log devient un objet
#     def __init__(self,lineraw):
#         #ligne raw designe la ligne "brute"
#         lineraw=lineraw+'\t'
#         lineraw=lineraw.split('\t')
#         self.sc=True
#         print(lineraw)
#         if("noscore" in lineraw):
#             self.sc=False
#         self.IP=lineraw[1]
#         lineraw=lineraw[0].split(' ')
#         dateraw=lineraw[0].split('.')
#         self.date=dateraw[0]
#         timeraw=dateraw[1].split(':')
#         self.time=int(timeraw[0])*3600+int(timeraw[1])*60+int(timeraw[2])
#         self.timetext=dateraw[1]
#         self.session=lineraw[1]
#         self.sheet=int(lineraw[2])
#         self.exercise=int(lineraw[3])
#         self.type=lineraw[4]
#         self.score=0
#         if(lineraw[4]=="score"):
#             self.score=float(lineraw[5])
