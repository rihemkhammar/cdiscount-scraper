"""- fonction pour changer les critéres (filtre)
- fonction pour le loop Item
- fonction pour l'extraction des donnèes
- fonction pour exporter sous Excel
- fonction pour la pagination
"""
import logging
from fileinput import filename

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(level=logging.INFO,
                    filename="cdiscount.log",
                    filemode="w",
                    format= "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%d-%b-%y | %H:%M:%S"
)
def change_criterias(page, url):
    page.goto(url)
    #Acepter les cookies
    try:
        page.wait_for_selector('xpath=//button[@id="footer_tc_privacy_button_2"]', timeout=10000)
        page.locator('xpath=//button[@id="footer_tc_privacy_button_2"]').click()
    except PlaywrightTimeoutError as e:
        logging.error(f"le bouton 'Accepter les cookies n'existe pas':{e}")
        raise
    #Cliquer sur 'Tout Supprimer'
    try:
        page.wait_for_selector('xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/div[1]/button/span', timeout=10000)
        page.locator('xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/div[1]/button/span').click()
    except PlaywrightTimeoutError as e:
        logging.error(f"le bouton 'Tout Supprimer  n'existe pas':{e}")
        raise
    # Cliquer sur 'taille'
    try:
       page.wait_for_selector(
                'xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/section[5]/label',
                timeout=10000)
       page.locator('xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/section[5]/label').click()
    except PlaywrightTimeoutError as e:
        logging.error(f" le bouton taille  n'existe pas:{e}")
        raise

        # Cliquer sur '12 pouces'
    try:
         page.wait_for_selector('xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/section[5]/div/div/label[1]', timeout=50000)
         page.locator(
                'xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/section[5]/div/div/label[1]').click()
    except PlaywrightTimeoutError as e:
        logging.error(f" le bouton 12 pouces  n'existe pas:{e}")
        raise

    # Verification des changement
    # Extraire le nombre de filtre

    try:
        nbr_filtre =  page.locator('xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/div[2]').locator('xpath=./*').count()
    except PlaywrightTimeoutError as e:
        logging.error(f"le nombre de filtre  n'existe pas:{e}")
        raise
    # Extraire la catregorie

    try:
        catregories = page.locator(
                'xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/div[2]/button/span[1]').text_content().strip()
    except PlaywrightTimeoutError as e:
         logging.error(f"la catregorie n'existe pas:{e}")
         raise


   # Extraire le nombre de produit
    try:
        nbr_produit = page.locator(
            'xpath=/html/body/div[3]/div/section/div[1]/div[1]/div[1]/section[1]/section[5]/div/div/label[1]/span[2]/span').text_content().strip()
    except PlaywrightTimeoutError as e:
        logging.error(f"le nombre de produit n'existe pas:{e}")
        raise
    if "1" not in nbr_produit or "12 pouces" not in catregories:
        logging.error("la catregorie ou le nombre de filtre  n'est pas le bon.")
        raise ValueError
    logging.info(f"il ya {nbr_filtre} la catégorie  {catregories} contient {nbr_produit} produit")

    return page


def main():
    url = "https://www.cdiscount.com/informatique/r-pc+portable+14+pouces.html?nav_menu=227::PC%20Portable%2012%22%20%C3%A0%2014%22"
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        page = browser.new_page()
        #Changer les filtres
        change_criterias(page, url)

        browser.close()


if __name__ == '__main__':
    main()
