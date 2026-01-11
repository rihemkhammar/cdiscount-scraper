import selectors

from playwright.sync_api import sync_playwright
from cdiscount import load_selectors, click_by_name, get_text_by_name, get_count_by_name, change_criterias, loop_item


def main():
    item_data=[]

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        page = browser.new_page()
        # Charger les sélecteurs
        df = load_selectors("selectors.xlsx")

        # Récupérer l’URL depuis Excel
        url = df.iloc[0]["url_site"]

        # Navigation
        page.goto(url)

        # Appliquer les critères
        info = change_criterias(page, df)
        item_data = loop_item(page, df)
        #return page
        browser.close()


if __name__ == '__main__':
    main()