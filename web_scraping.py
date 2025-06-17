import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")  


service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=options)
browser.get("https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW")
browser.maximize_window()

data = []

for i in range(1, 5):
    rows = browser.find_elements(By.XPATH, "//*[@id='table']/div/table[2]/tbody/tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns:
            row_data = [col.text for col in columns]
            data.append(row_data)
    browser.find_element(By.XPATH, "//*[@id='a-page']/main/div/div/nav/ul/li[3]/a").click()     
    sleep(2)    
browser.quit()

new_data = [row[1:4] for row in data]
df = pd.DataFrame(new_data, columns=['Title', 'Worldwide Gross', 'Release Date'])

df.to_csv('top_1000_movies.csv', index=False)
print("Data was saved successfully")
