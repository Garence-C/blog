import os

# Fonction pour lister les fichiers logs disponibles dans le répertoire courant
def list_log_files():
    """Liste les fichiers logs dans le répertoire courant."""
    files = [f for f in os.listdir(".") if f.startswith("log_proxy") and f.endswith(".txt")]
    return files


def parse_log_file(filepath):
    """Analyse un fichier log et retourne les données extraites."""
    data = []
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 5:
                date_time, ip_address, method_http, code_response, url = parts[:5]
                data.append((date_time, ip_address, url, method_http, code_response))
    return data

# Fonction pour générer un script SQL
def generate_sql_script(data, output_file):
    """Génère un script SQL à partir des données extraites."""
    with open(output_file, "w") as file:
        file.write("-- Script SQL généré automatiquement\n")
        for entry in data:
            date_time, ip_address, url, method_http, code_response = entry
            sql = (
                f"INSERT INTO journaux_acces (horodatage, adresse_ip_employe, url_consultee, methode_http, code_reponse)\n"
                f"VALUES ('{date_time}', '{ip_address}', '{url}', '{method_http}', {code_response});\n"
            )
            file.write(sql)

# Fonction principale
def main():
    # Lister les fichiers logs dans le répertoire courant
    log_files = list_log_files()
    if not log_files:
        print("Aucun fichier log trouvé.")
        return

    # Affichage des fichiers logs disponibles
    print("Fichiers logs disponibles :")
    for i, file in enumerate(log_files):
        print(f"{i + 1}. {file}")

    # Sélection d'un fichier log
    try:
        choice = int(input("Entrez le numéro du fichier à analyser : ")) - 1
        if choice < 0 or choice >= len(log_files):
            raise ValueError("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return

    selected_file = log_files[choice]
    print(f"Fichier sélectionné : {selected_file}")

    # Analyse et génération du script SQL
    log_data = parse_log_file(selected_file)
    output_file = f"insert_{selected_file.replace('.txt', '.sql')}"
    generate_sql_script(log_data, output_file)

    print(f"Script SQL généré : {output_file}")

main()
