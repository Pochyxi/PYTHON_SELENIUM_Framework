from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.edge.service import Service as EdgeService

edge_options = webdriver.EdgeOptions()
edge_options.add_argument('--inprivate')

service_obj = EdgeService("/Users/a.lopez/Documents/msedgedriver")

driver = webdriver.Edge(service=service_obj, options=edge_options)

driver.get("https://rahulshettyacademy.com/AutomationPractice/")
checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

print(len(checkboxes))

for checkbox in checkboxes:
    if checkbox.get_attribute("value") == "option2":
        checkbox.click()
        assert checkbox.is_selected()
        break
