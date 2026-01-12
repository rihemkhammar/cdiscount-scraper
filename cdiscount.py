"""x - fonction pour changer les critéres (filtre)
xfonction pour le loop Item
x fonction pour l'extraction des donnèes
- fonction pour exporter sous Excel
- fonction pour la pagination
"""
import logging
import pandas as pd
from playwright.sync_api import  TimeoutError as PlaywrightTimeoutError


logging.basicConfig(level=logging.INFO,
                    filename="cdiscount.log",
                    filemode="w",
                    format= "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d-%b-%y | %H:%M:%S"
)

def load_selectors(excel_path):

    df = pd.read_excel(excel_path)

    required = {"name", "xpath", "url_site"}
    if not required.issubset(df.columns):
        raise ValueError("Le fichier Excel doit contenir : name | xpath | url_site")

    return df

def click_by_name(page, df, name, timeout=10000):

    row = df[df["name"] == name]
    url = df.iloc[0]["url_site"]
    page.goto(url)

    if row.empty:
        raise ValueError(f"Sélecteur '{name}' introuvable dans selectors.xlsx")

    xpath = row.iloc[0]["xpath"]

    try:
        page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
        page.locator(f"xpath={xpath}").click()
        logging.info(f"Click OK : {name}")
    except PlaywrightTimeoutError as e:
        logging.error(f"Impossible de cliquer sur {name} : {e}")
        raise


def get_text_by_name(page, df, name, timeout=10000):
    row = df[df["name"] == name]
    if row.empty:
        raise ValueError(f"Sélecteur '{name}' introuvable dans le DataFrame")

    xpath = row.iloc[0]["xpath"]

    try:
        page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
        element = page.locator(f"xpath={xpath}")
        text = element.text_content().strip()
        logging.info(f"Récupération OK : {name} -> {text}")
        return text
    except PlaywrightTimeoutError as e:
        logging.error(f"Impossible de récupérer le texte de '{name}' : {e}")
        raise

def get_count_by_name(page, df, name, timeout=10000):

    row = df[df["name"] == name]
    if row.empty:
        raise ValueError(f"Sélecteur '{name}' introuvable dans le DataFrame")

    xpath = row.iloc[0]["xpath"]

    try:
        page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
        element = page.locator(f"xpath={xpath}")
        count = element.locator('xpath=./*').count()  # compte tous les enfants directs
        logging.info(f"Count OK : {name} -> {count}")
        return count
    except PlaywrightTimeoutError as e:
        logging.error(f"Impossible de récupérer le count de '{name}' : {e}")
        raise
def get_all(page, df, name, timeout=10000):

    row = df[df["name"] == name]
    if row.empty:
        raise ValueError(f"Sélecteur '{name}' introuvable dans le DataFrame")

    xpath = row.iloc[0]["xpath"]

    try:
        page.wait_for_selector(f"xpath={xpath}", timeout=timeout)
        element = page.locator(f"xpath={xpath}")
        items = element.locator('xpath=./*').all()  # compte tous les enfants directs
        logging.info(f"Count OK : {name} -> {len(items)}")
        return items
    except PlaywrightTimeoutError as e:
        logging.error(f"Impossible de récupérer le count de '{name}' : {e}")
        raise


def loop_item(page,df):
    item_data = []
    items = get_all(page, df, "product-list")

    current_page = get_text_by_name(page, df, "current_page")

    nbr_filtre = get_count_by_name(page, df, "category")

    logging.info(f"Il y {nbr_filtre} Filtre(s) sur la page {current_page} qui contient {len(items)} éléments.")

    for item in items:
        # Link
        link = None
        link_loc = item.locator('xpath=.//section/a')
        if link_loc.count() > 0:
            link = link_loc.first.get_attribute("href")

        # Title
        title = None
        title_loc = item.locator("xpath=.//h2[@data-e2e='lplr-title']")
        if title_loc.count() > 0:
            title = title_loc.first.text_content().strip()

        # Ancien prix
        ancien_prix = None
        ancien_prix_loc = item.locator('xpath=.//div[@class="sc-83lijy-1 hPUKzb SecondaryPrice-wrapper"]')
        if ancien_prix_loc.count() > 0:
            ancien_prix = ancien_prix_loc.first.text_content().strip()

        # Prix actuel
        prix_actuel = None
        prix_actuel_loc = item.locator('xpath=.//span[@class="sc-e4stwg-1 gIpMGn"]')
        if prix_actuel_loc.count() > 0:
            prix_actuel = prix_actuel_loc.first.text_content().strip()

        # Ajouter au résultat
        product_details = {
            "url": link,
            "title": title,
            "prix": prix_actuel,
            "ancien_prix": ancien_prix
        }
        item_data.append(product_details)

    return item_data


def calcul_prix_final(s):
    if s is None:  # ou pd.isna(s)
        return None
    s = s.replace(" ", "")  # retirer les espaces
    # Extraire le prix
    prix_str = s.split("€")[0].replace(",", ".")
    prix = float(prix_str)

    # Vérifier si remise existe
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

def pagination(page):


    try:
        page.wait_for_selector(f"xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[2]/div[2]/div[2]/nav/div[3]/button", timeout=10000)
        page.locator(f"xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[2]/div[2]/div[2]/nav/div[3]/button").click()
        page.wait_for_selector("xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[2]/div[2]/div[1]/section")
        page.wait_for_timeout(2000)
        logging.info(f"Click OK : suivant")
        return True
    except PlaywrightTimeoutError as e:
        logging.error(f"Impossible de cliquer sur suivant : {e}")
        return False





def change_criterias(page, df):


    # --- Cliquer sur les éléments dans l'ordre ---
    click_by_name(page, df, "cookies_button", timeout=10000)
    click_by_name(page, df, "delete_all_filtre", timeout=50000)
    click_by_name(page, df, "taille_label", timeout=50000)
    click_by_name(page, df, "douze_pouces", timeout=500000)

    # --- Récupérer texte et count ---
    try:
        categorie = get_text_by_name(page, df, "category",50000)
        nbr_produit = get_text_by_name(page, df, "number_products")
        nbr_filtre = get_count_by_name(page, df, "category")  # 'category' = nom dans Excel
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des données : {e}")
        raise

    if "1" not in nbr_produit or 'Moins de 12"' not in categorie:
        logging.error("La catégorie ou le nombre de filtre n'est pas le bon.")
        raise ValueError("Filtres ou catégorie incorrects")

    logging.info(f"Il y a {nbr_filtre} filtre(s), la catégorie '{categorie}' contient {nbr_produit} produit(s).")

    # Retourner un dictionnaire avec toutes les infos
    return {
        "categorie": categorie,
        "nbr_produit": nbr_produit,
        "nbr_filtre": nbr_filtre
    }

