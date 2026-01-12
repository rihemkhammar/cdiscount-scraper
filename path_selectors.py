import logging

import pandas as pd
from playwright.sync_api import  TimeoutError as PlaywrightTimeoutError



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
