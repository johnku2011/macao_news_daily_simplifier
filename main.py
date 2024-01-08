from functions import extract_title_and_contents,chinese_summarization,preprocess_text
import datetime
import warnings
import requests
import pandas as pd
from bs4 import BeautifulSoup

warnings.simplefilter(action='ignore', category=FutureWarning)

#Define dates for crawling
current_date = datetime.date.today()

#For extracting specific dates
#from datetime import datetime
#current_date = datetime(2024, 1, 1)

formatted_date = current_date.strftime("%Y-%m/%d/")
export_date = current_date.strftime("%Y%m%d")

print(formatted_date)

entry_link = "http://www.macaodaily.com/html/" + formatted_date

print('Kickoff: ' + entry_link)

#-----------------------------Collect all news links for the day-----------------------#

# Send a GET request to the desired page
response = requests.get(entry_link + "node_1.htm")

# Create a BeautifulSoup object with the response content
soup = BeautifulSoup(response.content, "html.parser")

# Find all div elements with class name "listblock"
listblock_divs = soup.find_all("div", class_="listblock")

# Initialize a list to store the href values
link_list = []

# Extract href values for each listblock div
for listblock_div in listblock_divs:
    # Find all child <a> elements within the div
    child_links = listblock_div.find_all("a")

    # Extract href values from the child <a> elements and append to the list
    link_list.extend([link["href"] for link in child_links])

    print(len(link_list))

# Initiatize the data collection process
# Create an empty dataframe
df = pd.DataFrame(columns=['Title', 'Content', 'Link'])

# Start collecting data
for link in link_list:
    title, child_texts = extract_title_and_contents(entry_link + link)

    # Create a dictionary with the data to append
    data_to_append = {'Title': title, 'Content': "".join(child_texts), 'Link': entry_link + link}

    # Convert the dictionary to a DataFrame
    data_to_append = pd.DataFrame(data_to_append, index=[0])

    # Concatenate the data to the original DataFrame
    df = pd.concat([df, data_to_append], ignore_index=True)

    print(len(df))

# Apply the summarization function to the 'Text' column
df['Summary'] = df['Content'].apply(lambda x: chinese_summarization(x))

# Apply preprocessing to the 'Content' column
df['Preprocessed_Content'] = df['Content'].apply(preprocess_text)

# Concatenate all the content into a single string
combined_text = ' '.join(df['Preprocessed_Content'])

df.to_csv("./data/" + export_date + "_output.csv", index=False, encoding="utf-8-sig")

