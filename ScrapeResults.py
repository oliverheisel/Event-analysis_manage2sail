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

def scrape_event_results(base_url):
    driver = webdriver.Chrome()  # Ensure you have a driver like Chrome or Firefox set up
    wait = WebDriverWait(driver, 10)  # Adjust wait time as necessary
    results = []  # Initialize a list to store the results

    try:
        results_url = base_url + '/results'
        driver.get(results_url)  # Load the results page

        # Wait for the dropdown to be clickable and select it
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#results > div > div > select')))
        select = Select(dropdown)

        # Iterate through all options in the dropdown
        for index in range(len(select.options)):
            select.select_by_index(index)
            time.sleep(3)  # Wait for the page to update (adjust time as needed)

            # Find and process the table data
            selector = '#results > div > div > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > table:nth-child(4)'
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            table = driver.find_element(By.CSS_SELECTOR, selector)

            # Extract headers
            headers = [th.text for th in table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')]
            header_classes = [th.get_attribute('class') for th in table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')]

            # Process each row in the table
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells:
                    row_data = {headers[i]: cells[i].text for i in range(min(len(headers), len(cells)))}
                    results.append(row_data)  # Append each row to results list

        # Filter out columns marked with 'ng-hide'
        visible_headers = [header for header, cls in zip(headers, header_classes) if 'ng-hide' not in cls]
        filtered_results = [{k: v for k, v in entry.items() if k in visible_headers} for entry in results]

        return filtered_results
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()  # Ensure the driver is closed after scraping

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
    event_results = scrape_event_results(url)
    print(event_results)
    # event_header = get_table_headers(url)
    # print(event_header)
    driver.quit()
    #Write results to a JSON file
    # with open('manage2sail_results.json', 'w') as file:
    #     json.dump(event_results, file, indent=4)
