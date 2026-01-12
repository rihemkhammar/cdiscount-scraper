

from playwright.sync_api import sync_playwright
from cdiscount import   change_criterias, loop_item
from excel_utils import export_to_excel
from pagination import pagination
from path_selectors import load_selectors


def main():
    item_data=[]
    all_items = []

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        page = browser.new_page()
        # Charger les sélecteurs
        df = load_selectors("selectors.xlsx")

        # Récupérer l’URL depuis Excel
        url = df.iloc[0]["url_site"]

        # Navigation
        #page.goto(url)

        # Appliquer les critères
        page_criterias = change_criterias(page, df)

        for i in range(20):
            # Extraire les données
            produits = loop_item(page, df)
            all_items.extend(produits)
            # Exporter les données Excel
            export_to_excel(all_items)
            if not pagination(page):
                break

        #return page
        browser.close()


if __name__ == '__main__':
    main()