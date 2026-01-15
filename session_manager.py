import json
import os

FISIER_SETARI = "config.json"

def salveaza_date(host, user):
    date_existente = incarca_date()
    date_existente[host] = {"utilizator": user}
    f = open(FISIER_SETARI, "w")
    json.dump(date_existente, f, indent=4)
    f.close()

def incarca_date():
    if not os.path.exists(FISIER_SETARI):
        return {}
    try:
        f = open(FISIER_SETARI, "r")
        date = json.load(f)
        f.close()
        return date
    except:
        return {}
