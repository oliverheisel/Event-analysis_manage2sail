# Libaries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo

# Database connection
""" in case you want to create your on database, just change this 3 variables according to your database. 
Database and collections will be created automatically."""
username = "globaladmin"
password = "UEKaeSc8Q3LK5naw"
db_url = "cluster1.etdy2wm.mongodb.net"

# database string
CNX_STR = f"mongodb+srv://{username}:{password}@{db_url}/?connectTimeoutMS=50000"
client = pymongo.MongoClient(CNX_STR)

# heck if the database exists
if "manage2sail" in client.list_database_names():
    print("Database exists!")
    db = client.manage2sail
else:
    print("Database does not exist!")


def scrape_eventdetails(wait, driver):
    eventdetails = []
    selector = '#details > table'
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    table = driver.find_element(By.CSS_SELECTOR, selector)
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        columns = row.find_elements(By.TAG_NAME, 'td')
        if len(columns) >= 2:  # Ensure there are at least two columns
            key = columns[0].text.strip(': ')
            value = columns[1].text
            eventdetails.append({key: value})  # Append each key-value pair to results list

    return eventdetails


def get_table_headers(driver, wait, header_selector):
    try:
        headers = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, header_selector)))
        header_texts = [th.text for th in headers.find_elements(By.TAG_NAME, 'th') if
                        'ng-hide' not in th.get_attribute('class')]
        return header_texts
    except Exception as e:
        #print(f"An error occurred while fetching headers: {e}")
        return []


def replace_column_keys(data, headers):
    new_data = []
    for record in data:
        new_record = {}
        for (key, value), header in zip(record.items(), headers):
            if key.strip() and value.strip():  # Check if both key and value are not empty
                new_record[header] = value
        new_data.append(new_record)
    return new_data


# # Function to scrape event results
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
#
# def scrape_eventresults(base_url, driver):
#     # Ergebnis-URL definieren und mit dem WebDriver öffnen
#     results = {}
#     results_url = base_url + '#!/results'
#     driver.get(results_url)
#     wait = WebDriverWait(driver, 10)
#
#     # CSS-Selektoren definieren
#     regatta_name_selector = '#results > div > div > div.regattaName'
#     table_selector = '#results > div > div > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > table:nth-child(4)'
#     header_selector = table_selector + ' > thead'
#
#     # Versuch, das Dropdown-Element zu finden und zu verarbeiten
#     try:
#         dropdown_selector = '#results > div > div > select'
#         dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector)))
#         select = Select(dropdown)
#
#         # Texte der Dropdown-Optionen in einer Liste speichern
#         option_texts = [option.text for option in select.options if option.text]
#
#         if not option_texts:
#             raise Exception("No options found in dropdown")
#
#         for option_text in option_texts:
#             try:
#                 select = Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))))
#                 select.select_by_visible_text(option_text)
#                 wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, table_selector)))
#
#                 results[option_text] = []
#                 table = driver.find_element(By.CSS_SELECTOR, table_selector)
#                 headers = get_table_headers(driver, wait, header_selector)
#
#                 for row in table.find_elements(By.TAG_NAME, 'tr'):
#                     columns = row.find_elements(By.TAG_NAME, 'td')
#                     row_data = {f"column_{i}": col.text for i, col in enumerate(columns) if 'ng-hide' not in col.get_attribute('class')}
#                     if any(value.strip() for value in row_data.values()):
#                         results[option_text].append(row_data)
#
#                 results[option_text] = replace_column_keys(results[option_text], headers)
#             except Exception as e:
#                 results[option_text] = "no results due to error: " + str(e)
#
#     except:
#         # Kein Dropdown, nur die aktuelle Seite scrapen
#         try:
#             regatta_name = driver.find_element(By.CSS_SELECTOR, regatta_name_selector).text
#             results[regatta_name] = []
#             table = driver.find_element(By.CSS_SELECTOR, table_selector)
#             headers = get_table_headers(driver, wait, header_selector)
#
#             for row in table.find_elements(By.TAG_NAME, 'tr'):
#                 columns = row.find_elements(By.TAG_NAME, 'td')
#                 row_data = {f"column_{i}": col.text for i, col in enumerate(columns) if 'ng-hide' not in col.get_attribute('class')}
#                 if any(value.strip() for value in row_data.values()):
#                     results[regatta_name].append(row_data)
#
#             results[regatta_name] = replace_column_keys(results[regatta_name], headers)
#         except Exception as e:
#             results[regatta_name] = "no results due to error: " + str(e)
#
#     return results

from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def scrape_eventresults(base_url, driver):
    # Ergebnis-URL definieren und mit dem WebDriver öffnen
    results = {}
    results_url = base_url + '#!/results'
    driver.get(results_url)
    wait = WebDriverWait(driver, 10)

    # CSS-Selektoren definieren
    regatta_name_selector = '#results > div > div > div.regattaName'
    table_selector = '#results > div > div > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > table:nth-child(4)'
    header_selector = table_selector + ' > thead'

    # Überprüfen, ob das Dropdown existiert
    dropdown_selector = '#results > div > div > select'
    dropdown_elements = driver.find_elements(By.CSS_SELECTOR, dropdown_selector)

    if dropdown_elements:
        # Dropdown vorhanden, verarbeite jede Option
        select = Select(dropdown_elements[0])
        option_texts = [option.text for option in select.options if option.text]

        if not option_texts:
            raise Exception("No options found in dropdown")

        for option_text in option_texts:
            try:
                select = Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector))))
                select.select_by_visible_text(option_text)
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, table_selector)))

                results[option_text] = []
                table = driver.find_element(By.CSS_SELECTOR, table_selector)
                headers = get_table_headers(driver, wait, header_selector)
                if len(headers) == 0:
                    raise Exception("Header length is zero")

                for row in table.find_elements(By.TAG_NAME, 'tr'):
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    row_data = {f"column_{i}": col.text for i, col in enumerate(columns) if 'ng-hide' not in col.get_attribute('class')}
                    if any(value.strip() for value in row_data.values()):
                        results[option_text].append(row_data)

                results[option_text] = replace_column_keys(results[option_text], headers)
            except Exception as e:
                results[option_text] = "no results"
    else:
        # Kein Dropdown, nur die aktuelle Seite scrapen
        try:
            regatta_name = driver.find_element(By.CSS_SELECTOR, regatta_name_selector).text
            results[regatta_name] = []
            table = driver.find_element(By.CSS_SELECTOR, table_selector)
            headers = get_table_headers(driver, wait, header_selector)
            if len(headers) == 0:
                raise Exception("Header length is zero")


            for row in table.find_elements(By.TAG_NAME, 'tr'):
                columns = row.find_elements(By.TAG_NAME, 'td')
                row_data = {f"column_{i}": col.text for i, col in enumerate(columns) if 'ng-hide' not in col.get_attribute('class')}
                if any(value.strip() for value in row_data.values()):
                    results[regatta_name].append(row_data)

            results[regatta_name] = replace_column_keys(results[regatta_name], headers)
        except:
            results[regatta_name] = "no results"

    return results


if __name__ == "__main__":
    # Setup WebDriver
    options = Options()
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 5)

    collection = db.events
    try:
        for document in collection.find().limit(1):
            url = document['link']
            driver.get(url)
            event_details = scrape_eventdetails(wait, driver)
            update_result = collection.update_one({'_id': document['_id']}, {'$set': {'eventdetails': event_details}})

            results = scrape_eventresults(url, driver)
            # Update the MongoDB document with the results structured by class names
            update_result = collection.update_one({'_id': document['_id']}, {'$set': {'resultsByClass': results}})
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()