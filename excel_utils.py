import pandas as pd
import logging



def calcul_prix_final(s):
    if s is None:
        return None
    s = s.replace(" ", "")
    # Extraire le prix
    prix_str = s.split("€")[0].replace(",", ".")
    prix = float(prix_str)


    if "-" in s:
        remise_str = s.split("-")[1].replace("%", "")
        remise = float(remise_str) / 100
    else:
        remise = 0.0

    return round(prix * (1 - remise), 2)



def export_to_excel(produits):

    df = pd.DataFrame(produits)
    #Modifier la colone prix
    if "prix" in df.columns:
        df["prix"] = df["prix"].str.replace("€", ",", regex=False)
    else:
        logging.error("la colonne 'prix' n'existe pas")
        raise KeyError
    if "ancien_prix" in df.columns:
         df["ancien_prix_remise"] = df["ancien_prix"].apply(calcul_prix_final)
    else:
         logging.error("la colonne 'ancien_prix' n'existe pas")
         raise KeyError

    #Enregistrer la DataFrame
    try:
        df.to_excel("cdiscount.xlsx", index=False)
        logging.info("le DataFrame complet a bien enregistré.")
    except ValueError as e:
        logging.error(f"Le DataFrame n'a pas été enregistre:{e}")
        raise