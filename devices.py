import requests
from bs4 import BeautifulSoup
import json

def scrape_smartphone_info(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Initialize lists to store names and codenames
        names = []
        codenames = []
        
        # Find all tables on the page
        tables = soup.find_all('table')
        
        # Iterate over each table
        for table in tables:
            # Extract model and codename information from table rows
            for row in table.find_all('tr')[1:]:  # Skip the first row (header row)
                columns = row.find_all('td')
                name = columns[0].strong.text.strip()
                codename = columns[1].text.strip()
                names.append(name)
                codenames.append(codename)
        
        return names, codenames
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return [], []

# Example usage
url = 'https://tech-latest.com/android-device-codenames/'
names, codenames = scrape_smartphone_info(url)

# Store the extracted data in a dictionary
data = []
for name, codename in zip(names, codenames):
    data.append({"name": name, "codename": codename})

# Write the data to a JSON file
with open("smartphones.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Data stored in smartphones.json")
