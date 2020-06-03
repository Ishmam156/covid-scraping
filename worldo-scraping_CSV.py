# Scraping COVID data from Worldometers

# Necessary Imports
from bs4 import BeautifulSoup
from csv import DictWriter
import requests

# Scraping URL
url = "https://www.worldometers.info/coronavirus/"

# Getting HTML from URL
html = requests.get(url)

# Converting HTML to readable data
raw_data = BeautifulSoup(html.text, "html.parser")

# Initializing data list
data = []

# Loading all country data as per class in HTML. Found after checking HTML code through browser inspector
source_code = raw_data.find_all(class_="mt_a")

# Initializing country counter
count = 0

# Loop for getting information
for i in source_code:
	# Country count checked from HTML
	if count == 213:
		break
	name = i.get_text()
	total_case_count = i.find_parent().find_next_sibling()
	total_new_cases = total_case_count.find_next_sibling()
	total_deaths = total_new_cases.find_next_sibling()
	rev_total_deaths = total_deaths.get_text().split()
	# Check for countries without total deaths. Splitting deaths tally as there is a trailing whitespace in source HTML
	if len(rev_total_deaths) == 0:
		rev_total_deaths.append("")
	new_deaths = total_deaths.find_next_sibling()
	total_recovered = new_deaths.find_next_sibling()
	active_cases = total_recovered.find_next_sibling()
	# Add all data to initiated list
	data.append({"Country": name,
	 "Total Cases": total_case_count.get_text(),
	  "New Cases" : total_new_cases.get_text()[1:],
	  "Total Deaths": rev_total_deaths[0],
	  "New Deaths": new_deaths.get_text(),
	  "Total Recovered": total_recovered.get_text(),
	  "Active Cases": active_cases.get_text()})
	count += 1

# Preparing CSV to write data to
with open('COVID.csv', "w") as file:
	headers = ["Country", "Total Cases", "New Cases", "Total Deaths", "New Deaths", "Total Recovered", "Active Cases"]
	writer = DictWriter(file, fieldnames=headers)
	writer.writeheader()
	for i in data:
		writer.writerow(i)

# End note to guide steps complted without error
print("Scraping done!")
