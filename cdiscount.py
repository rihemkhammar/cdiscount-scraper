
import logging

from path_selectors import get_all, get_text_by_name, get_count_by_name, click_by_name

logging.basicConfig(level=logging.INFO,
                    filename="cdiscount.log",
                    filemode="w",
                    format= "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d-%b-%y | %H:%M:%S"
)



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

