import subprocess
import importlib

def verifier_modules():
    # Nom du fichier texte contenant les modules requis
    fichier_modules = "modules_requis.txt"

    try:
        # Lecture du fichier texte contenant les modules requis
        with open(fichier_modules, 'r') as file:
            modules_requis = file.readlines()
            modules_requis = [module.strip() for module in modules_requis]
            
            # Vérification de chaque module requis
            modules_manquants = []
            for module in modules_requis:
                try:
                    importlib.import_module(module)
                    print(f"{module} est installé.")
                except ImportError:
                    print(f"{module} n'est pas installé.")
                    modules_manquants.append(module)
            
            # Installation des modules manquants
            if modules_manquants:
                print("\nInstallation des modules manquants...")
                for module in modules_manquants:
                    subprocess.run(["pip", "install", module])
                    print(f"{module} a été installé.")
                print("\nTous les modules ont été installés.")
            else:
                print("\nTous les modules requis sont déjà installés.")

    except FileNotFoundError:
        print(f"Le fichier {fichier_modules} n'a pas été trouvé.")

try:
    import sqlite3
    import webbrowser
    from colorama import *
except:
    verifier_modules()


print("\n")
print(Fore.LIGHTBLUE_EX + "Bornes avec coordonnées")
print(Fore.RED + "Bornes sans coordonnées")
print(Style.RESET_ALL)

def main():
    connexion = sqlite3.connect("bornedb")
    curseur = connexion.cursor()
    latitude = None
    longitude = None
    adresse = None
    nombre = 1
    alllocation = []

#longitude == None and latitude == None or 
    while adresse == None:
        ville =  input("Entrez la ville dans laquelle se situe votre borne : ")
        curseur.execute(f"SELECT bornes_irve.operateur, bornes_irve.ad_station, bornes_irve.accessibilité, bornes_irve.puiss_max, bornes_irve.Xlongitude, bornes_irve.Ylatitude, code_insee_postal.code_postal FROM bornes_irve JOIN code_insee_postal ON bornes_irve.code_insee = code_insee_postal.code_insee_insee WHERE code_insee_postal.Commune LIKE '{ville}'")
        for resultat in curseur:
            if resultat not in alllocation:
                if resultat[4] == None and resultat[5] == None:
                    print(Fore.RED + f"{nombre} | Adresse : {resultat[1]} | Opérateur : {resultat[0]} | Accessibilité : {resultat[2]} | Puissance : {resultat[3]}")
                    print(Style.RESET_ALL)
                else:
                    print(Fore.LIGHTBLUE_EX + f"{nombre} | Adresse : {resultat[1]} | Opérateur : {resultat[0]} | Accessibilité : {resultat[2]} | Puissance : {resultat[3]}")
                    print(Style.RESET_ALL)
                nombre += 1
                alllocation.append(resultat)
        try :
            resultat[0]
            print(f"Voici toutes les bornes situés à {ville}, choisissez en une valable : ")
            rep = int(input("Chiffre : "))-1
            longitude = alllocation[rep][4]
            latitude = alllocation[rep][5]
            adresse = alllocation[rep][1]

        except:
            print("Il n'y a pas de bornes dans cette ville choissisez une autre ville.")
            main()

    if longitude == None or latitude == None:
        webbrowser.open(f"https://www.google.com/maps/place/{adresse}")
        #print("Les coordonnées de cette borne ne sont pas répertoriées.")
    else:
        webbrowser.open(f"https://www.google.com/maps/place/{latitude},{longitude}")

while True:
    try:
        if __name__ == "__main__":
            main()
    except :
        main()