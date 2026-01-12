import logging
from playwright.sync_api import  TimeoutError as PlaywrightTimeoutError

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

