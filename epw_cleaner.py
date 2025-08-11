
import re

def clean_epw(input_path, output_path):
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    header_lines = []
    data_lines = []

    for line in lines:
        if line.strip() == "":
            continue
        if not re.match(r'^\d{4}', line):
            header_lines.append(line.strip())
        else:
            data_lines.append(line.strip())

    cleaned_data = []
    for line in data_lines:
        # Remplacer les tabulations par des virgules
        line = line.replace("\t", ",")

        # Supprimer les séquences de caractères non valides
        line = re.sub(r"[\*\?]+", "0", line)

        # Remplacer les valeurs extrêmes ou manquantes
        line = line.replace("9999", "0").replace("99999", "0").replace("999999999", "0")

        # Nettoyer les espaces multiples
        line = re.sub(r"\s+", ",", line)

        # Forcer 33 champs par ligne
        fields = line.split(",")
        if len(fields) > 33:
            fields = fields[:33]
        elif len(fields) < 33:
            fields += ["0"] * (33 - len(fields))

        cleaned_line = ",".join(fields)
        cleaned_data.append(cleaned_line)

    # Écriture du fichier nettoyé
    with open(output_path, "w", encoding="utf-8") as f_out:
        for line in header_lines:
            f_out.write(line + "\n")
        for line in cleaned_data:
            f_out.write(line + "\n")

# Exemple d'utilisation
clean_epw("Ziguinchor_2050.epw", "Ziguinchor2050.epw")
