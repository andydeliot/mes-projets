


import pony
from pony.orm import *
import os

try:
    os.remove("database.sqlite")
except:
    pass

db = Database()


class Langue(db.Entity):
    langue = Required(str, unique=True)  # Langue écrite dans sa langue.

    mots = Set(lambda: Mot)


class Mot(db.Entity):

    langue = Required(lambda: Langue)
    sens = Required(lambda: Sens)
    ecritures = Set(lambda: Ecriture)
    prononciation = Set(lambda: Prononciation)


class Sens(db.Entity):
    sens = Required(str, unique=True) # Description en français. (évolutif)

    mots = Set(lambda: Mot)


class Ecriture(db.Entity):
    ecriture = Required(str)

    mot = Required(lambda: Mot)


class Prononciation(db.Entity):
    prononciation = Required(str)

    mot = Required("Mot")


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


# Créations et affichages de la base de données.

@db_session
def ajouter_mot(le_sens, *ecritures):
    """ Ajoute les mots pour chaques langues possible. """
    sens = Sens(sens=le_sens)
    for i in range(len(ecritures)):
        langue = Langue[i+1]
        mot = Mot(langue=langue, sens=sens)
        Ecriture(ecriture=ecritures[i], mot=mot)

@db_session
def creation():
    # Les langues.
    fr = Langue(langue="Français")
    en = Langue(langue="English")
    es = Langue(langue="Español")
    po = Langue(langue="Português")
    al = Langue(langue="Alemannisch")

    # Les mots
    sens="Le bleu est un champ chromatique, regroupant les teintes rappelant celles du ciel ou de la mer par temps clair."
    ajouter_mot(sens, "Bleu", "Blue", "Azul", "Azul", "Blau")

    

@db_session
def affichage():
    select(l for l in Langue).show()
    print()
    select(s for s in Sens).show()
    print()
    select(m for m in Mot).show()
    print()
    
    print("Exercice")
    select(e.mot.sens for e in Ecriture if "B" in e.ecriture).show()

creation()
affichage()



































































