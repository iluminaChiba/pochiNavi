from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback

URL = "https://pochipass.com/member/"

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  Run in headless mode
driver = None

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    print("Page loaded successfully.")

except Exception:
    print("An error occurred:")
    traceback.print_exc()
finally:
    if driver:
        driver.quit()
