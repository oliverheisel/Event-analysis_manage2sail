from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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


def get_table_headers(driver, wait, header_selector):
    try:
        headers = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, header_selector)))
        header_texts = [th.text for th in headers.find_elements(By.TAG_NAME, 'th') if 'ng-hide' not in th.get_attribute('class')]
        return header_texts
    except Exception as e:
        print(f"An error occurred while fetching headers: {e}")
        return []

def replace_column_keys(data, headers):
    new_data = []
    for record in data:
        new_record = {}
        for (key, value), header in zip(record.items(), headers):
            new_record[header] = value
        new_data.append(new_record)
    return new_data


def scrape_eventresults(base_url, driver, wait):
    results = []
    driver.get(base_url + 'results')
    dropdown_selector = '#results > div > div > select'
    table_selector = '#results > div > div > div:nth-child(3) > div:nth-child(5) > div:nth-child(2) > div:nth-child(3) > table:nth-child(4)'
    header_selector = table_selector + ' > thead'

    try:
        dropdown = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, dropdown_selector)))
        select = Select(dropdown)
    except Exception as e:
        print(f"No selectable dropdown found: {e}")
        return results

    for index in range(len(select.options)):
        try:
            # Re-select dropdown and option to avoid staleness
            dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_selector)))
            select = Select(dropdown)
            select.select_by_index(index)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, table_selector)))

            temp_results = []
            table = driver.find_element(By.CSS_SELECTOR, table_selector)
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                columns = row.find_elements(By.TAG_NAME, 'td')
                row_data = {f"column_{i}": col.text for i, col in enumerate(columns) if 'ng-hide' not in col.get_attribute('class')}
                if any(value.strip() for value in row_data.values()):
                    temp_results.append(row_data)

            headers = get_table_headers(driver, wait, header_selector)
            processed_results = replace_column_keys(temp_results, headers)
            results.extend(processed_results)
        except Exception as e:
            print(f"Error processing option index {index}: {e}")

    return results


if __name__ == "__main__":
    options = Options()
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://www.manage2sail.com/en-US/event/2c2c10ce-db40-4402-97fb-4fd120e071f1#!/'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    event_details = scrape_eventdetails()
    print(event_details)
    data = scrape_eventresults(url, driver, wait)
    print(data)
    driver.quit()
