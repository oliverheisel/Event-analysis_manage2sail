import json
import requests
from lxml import html

base_url = 'https://www.manage2sail.com/de-CH/search'
params = {
    'filterYear': '2023',
    'filterMonth': '',
    'filterCountry': 'SUI',
    'filterRegion': 'e3165406-2424-470e-9ec2-d9dac6c9b742',
    'filterClass': '',
    'filterClubId': '',
    'filterScoring': '',
    'paged': 'false',
    'filterText': ''
}

all_data = []
response = requests.get(base_url, params=params)

if response.status_code == 200:
    # Parse the HTML content
    tree = html.fromstring(response.content)
    table = tree.xpath('/html/body/div[2]/div[3]/div[2]/div/table')[0]
    data = []

    for row in table.xpath('./tbody/tr'):
        row_data = [cell.text_content().strip() for cell in row.xpath('./td')]
        link = row.xpath('./td[4]/a/@href')
        row_data.append(link[0] if link else None)
        data.append(row_data)

    all_data.extend(data)
else:
    print(f"Failed to retrieve page")

# print(all_data)

formatted_data = [
    {
        'year': row[0],
        'startdate': row[1],
        'enddate': row[2],
        'nameevent': row[3],
        'status': row[4],
        'nation': row[5],
        'city': row[6],
        'hostclub': row[7],
        'link': row[8]
    } for row in all_data
]

# To visualize the formatted data
print(formatted_data[:5])  # Print the first 5 for brevity

# Save formatted data as JSON
with open('manage2sail_eventlist.json', 'w') as f:
   json.dump(formatted_data, f, indent=4)

print("Formatted data saved as manage2sail_eventlist.json")