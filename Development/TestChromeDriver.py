# Libraries
import json
import pymongo
import requests
from lxml import html

# Load database credentials from json file
with open('../dbconfig.json') as config_file:
    config = json.load(config_file)

username = config['username']
password = config['password']
db_url = config['db_url']

# Database connection string
CNX_STR = f"mongodb+srv://{username}:{password}@{db_url}/?connectTimeoutMS=50000"
client = pymongo.MongoClient(CNX_STR)

# Check if the database exists
db_name = "manage2sail"
if db_name in client.list_database_names():
    print("Database exists!")
    db = client[db_name]
else:
    print("Database does not exist!")
    exit()

# Scrape the data
base_url = 'https://www.manage2sail.com/en-US/search'
params = {
    'filterYear': '2023',
    'filterMonth': '',
    'filterCountry': 'SUI',
    'filterRegion': '',
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
    print("Failed to retrieve page")
    exit()

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

# Print the first 5 formatted data entries for visualization
print(formatted_data[:5])

# Load data to database
insert_result = db.events.insert_many(formatted_data)
print(insert_result)
