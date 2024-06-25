# Scrape and Analyse Events from Manage2Sail.com

## How to
1. Create a MongoDB database
   1.1. Create a Cluster
   1.2. Connect to MongoDB Compass
   1.3. Create a database named "manage2sail"
   1.4. Create a config file named: "dbconfig.json" (see template!)
2. Install the requirements.txt
3. Get Chrome and Chromedriver (maybe you need to change the directory in the scripts to wherever you placed the chromedriver)
4. Run the script "ScrapeEventList.ipynb"
   (optional) Set the filters you need. Therefore, go to the website and copy them from the URL.
5. Run the script "ScrapeEventDetailsAndResults.ipynb"
6. Analyse the data inside the MongoDB database

# License
The scripts are free to use for personal and educational purposes. I don't ensure that it is legal!!!
