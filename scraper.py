import requests # for making standard html requests
from bs4 import BeautifulSoup # for parsing html data
import pandas as pd # for data organization
import csv # for saving and updating data
from datetime import datetime # for logging date data was accessed and archived


# 2 functions: 1) get request and 2) DataFrames


# Request CDC data and parse it using BeautifulSoup
url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Find daily case and death counts
counts = soup.find_all(class_ = 'count')

# Remove commas from counts and cast string to int
counts_list = []
for count in counts:
    count = count.string # Access string content in 'count' tag
    count = int(count.replace(',', ''))
    counts_list.append(count)

# Get current time as month,day,year
current_time = datetime.now()
current_time = current_time.strftime("%m/%d/%Y")

# Create list of data for making new row in a DataFrame
d = [{'Total Cases': counts_list[0], 'Total Deaths': counts_list[1], 'Date': current_time}]

# Create temp DataFrame containing data to add
dfTemp = pd.DataFrame(data=d)

# Load existing CSV as DataFrame
dfTotalCount = pd.read_csv ('Total_Count.csv', index_col=0)

# Create list of DataFrames to concatenate
frames = [dfTotalCount, dfTemp]

# Concatenate DataFrames
dfTotalCount = pd.concat(frames, ignore_index=True)

# Export to CSV
dfTotalCount.to_csv('Total_Count.csv')
