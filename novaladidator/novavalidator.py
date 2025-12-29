
import os          # fichiers, chemins, système
import sys         # arguments, runtime
import csv         # fichiers tabulaires

def main():

    if len(sys.argv) >= 2:
        fichier = sys.argv[1]
    else: 
        fichier = input ("Error, reessayer :")

    fichier = fichier.strip()

    if not os.path.isfile(fichier):
        raise FileNotFoundError("Fichier invalide")
    print("Fichier selectionne", fichier)

    file_type = os.path.splitext(fichier)[1].lower().lstrip(".")
    data = open_file(fichier, file_type)
    errors = analyze_structure(data, file_type)
    status = decision(errors)
    rapport(fichier, errors, status)

    #ajouter apres : si fichier pas .csv ou .txt -> recommencer

#NovaValidator ouvre et lit un fichier
def open_file(fichier, file_type):
    #ouvrir le fichier
    #lire son contenu
    #demarrer l'analyse
    if file_type == "txt":
        with open(fichier, "r", encoding="utf-8") as f:
            lignestxt = []
            for line in f:
                lignetxtstrip = line.strip()
                lignestxt.append(lignetxtstrip)
            return lignestxt

    elif file_type == "csv":
        with open(fichier, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            return list(reader)
    else:
        raise ValueError("Type de fichier non supporte")
    
#cherche des problèmes
def analyze_structure(data, file_type):
    """
    si ligne vide → erreur
    si len(ligne) != len(en-tête) → erreur
    si champ == "" → erreur
    si int(champ) échoue → erreur
    si trop de lignes avec erreurs → warning / fail
    
    1 regles = if 
    pas de correction automatiques 
    tout est socker dans dico ou listes donc creer toujours avant
    """

    """
    Tu dois avoir au minimum ces éléments :

    une variable expected_cols

    une boucle for

    un if len(...) != expected_cols

    un errors.append({...})

    un return errors
    
    """
    #regle 1 si ligne vide → erreur
    errors = []

    if file_type == "txt":
        for line_number, line in enumerate(data, start=1):
            if line.strip() == "":
                errors.append({
                    "rule": "empty_line",
                    "line": line_number,
                    "message": "Ligne vide détectée"
                })

    elif file_type == "csv":
        for line_number, line in enumerate(data[1:], start=2):
            if not line or all(cell.strip() == "" for cell in line):
                errors.append({
                    "rule": "empty_line",
                    "line": line_number,
                    "message": "Ligne vide détectée"
                })


    #regle 2 si len(ligne) != len(en-tête) → erreur csv
        
    if file_type == "csv":
        expected_cols = len(data[0])

        for line_number, line in enumerate(data[1:], start=2):
            if not line or all(cell.strip() == "" for cell in line):
                continue  # déjà traité par règle 1

            if len(line) != expected_cols:
                errors.append({
                    "rule": "invalid_column_count",
                    "line": line_number,
                    "message": "Nombre de colonnes incorrect"
                })


    #regle 3 si champ == "" → erreur

    if file_type == "csv":
        expected_cols = len(data[0])

        for line_number, line in enumerate(data[1:], start=2):
            if not line or all(cell.strip() == "" for cell in line):
                continue 

            if len(line) != expected_cols:
                continue  

            for column_number, cell in enumerate(line, start=1):
                if cell.strip() == "":
                    errors.append({
                        "rule": "missing_value",
                        "line": line_number,
                        "column": column_number,
                        "message": "Champ vide détecté"
                    })


    
    # regle 4 si int(champ) échoue → erreur

    if file_type == "csv":
        expected_cols = len(data[0])

        for line_number, line in enumerate(data[1:], start=2):
            if not line or all(cell.strip() == "" for cell in line):
                continue  # règle 1

            if len(line) != expected_cols:
                continue  # règle 2

            for column_number, cell in enumerate(line, start=1):
                if cell.strip() == "":
                    continue  # règle 3
                
                # regle 4
                try:
                    int(cell)
                except ValueError:
                    errors.append({
                        "rule": "invalid_integer",
                        "line": line_number,
                        "column": column_number,
                        "value": cell,
                        "message": "Valeur numérique invalide"
                    })
        
    return errors


#décide si le fichier est fiable
def decision(errors):
    total_errors = len(errors)
    if total_errors == 0:
        return "OK"
    elif total_errors == 1:
        return "WARN"
    elif total_errors > 1:
        return "Totaly FAIL"

#écrit un rapport.
def rapport(fichier, errors, status):
    with open("rapport.txt", "w", encoding="utf-8") as f:
        f.write(f"NovaValidator Report\n")
        f.write(f"File analysed : {fichier}\n")
        f.write(f"Status : {status}\n")
        f.write(f"Number of errors : {len(errors)}\n")

if __name__ == "__main__":
    main()""