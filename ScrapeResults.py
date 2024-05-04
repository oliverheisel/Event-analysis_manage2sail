from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json  # Import the JSON module


def scrape_eventdetails():
    eventdetails = []
    selector = '#details > table'
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    table = driver.find_element(By.CSS_SELECTOR, selector)
    for row in table.find_elements(By.TAG_NAME, 'tr'):
        columns = row.find_elements(By.TAG_NAME, 'td')
        if len(columns) >= 2:  # Ensure there are at least two columns
            key = columns[0].text
            value = columns[1].text
            eventdetails.append((key, value))  # Append each key-value pair to results list

    return eventdetails

def scrape_eventresults(base_url):
    results = []  # Initialize a list to store the results
    try:
        results_url = base_url + '/results'
        driver.get(results_url)
    except:
        print("no resultspage found")
# Wait for the dropdown to be clickable and select it
    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#results > div > div > select')))
        select = Select(dropdown)

        # Iterate through all options in the dropdown
        for index in range(len(select.options)):
            # Refresh the dropdown and select object each iteration
            dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#results > div > div > select')))
            select = Select(dropdown)
            select.select_by_index(index)
            time.sleep(5)  # Adjust the sleep time if necessary

            # Find and process the table data
            selector = '#results > div > div > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > table:nth-child(4)'
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            table = driver.find_element(By.CSS_SELECTOR, selector)
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                columns = row.find_elements(By.TAG_NAME, 'td')
                row_data = {col.text for i, col in enumerate(columns)}
                results.append(row_data)  # Append each row to results list

    except:
        selector = '#results > div > div > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > table:nth-child(4)'
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        table = driver.find_element(By.CSS_SELECTOR, selector)
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            columns = row.find_elements(By.TAG_NAME, 'td')
            row_data = {f"column_{i}": col.text for i, col in enumerate(columns)}
            results.append(row_data)  # Append each row to results list

    return results


if __name__ == "__main__":
    options = Options()
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://www.manage2sail.com/en-US/event/2c2c10ce-db40-4402-97fb-4fd120e071f1#!'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    event_details = scrape_eventdetails()
    print(event_details)
    event_results = scrape_eventresults(url)
    driver.quit()
print(event_results)
    # # Write results to a JSON file
    # with open('manage2sail_results.json', 'w') as file:
    #     json.dump(event_results, file, indent=4)
