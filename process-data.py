import requests
from bs4 import BeautifulSoup
import re
import json

sust_url = "https://sustainability.asu.edu/people/scientists-scholars10/"
print("URL for Sustainability Scientists, Scholars and Fellows - https://sustainability.asu.edu/people/scientists-scholars10/")
print("Getting raw data from URL ...")
html_text = requests.get(sust_url).text
soup = BeautifulSoup(html_text, 'html.parser')
print("Building data in csv file ...")
with open("sustainability-persons.csv", 'w') as f:
    for div in soup.find_all('div', "person-blurb-text col-xs-12 col-sm-10"):
        for link in div.find_all('a'):
            f.write(link.string+', '+link.get('href')+'\n')


expertise_data = []

print("Processing Data for Expertise and Research Areas ... \n")
with open("sustainability-persons.csv", 'r') as f:
    lines = f.readlines()
    for line in lines:
        single_entry = {}
        url = line.split(',')[-1].strip()
        #url = "https://sustainability.asu.edu/person/amber-wutich/"
        #url = "https://sustainability.asu.edu/person/maria-cruz-torres/"
        if len(line) == 3:
            name = line.split(',')[0] + line.split(',')[1]
        name = line.split(',')[0]
        print("Processing for", name)
        single_entry['name'] = name
        single_entry['profile-link'] = url
        html_res = requests.get(url).text
        soup = BeautifulSoup(html_res, 'html.parser')
        soup.encode("ascii", 'ignore')

        expertise = []
        links = soup.find_all(href=re.compile("^/people/expert-search"))
        with open("test.txt", 'w') as f:
            f.write(str(soup))
        for link in links:
            expertise.append(link.get_text())
        single_entry['expertise'] = expertise
        research_area = []
        research = soup.find_all(id='projects')
        if not research:
            research_area.append("No Data Available")
        else:
            for div in research:
                for link in div.find_all('a'):
                    # Removing any special characters like copyright.
                    research_area.append(re.sub(r'[^\x00-\x7F]+', '', link.get_text()))
        single_entry['research-area'] = research_area
        expertise_data.append(single_entry)
        # break

with open("expertise_data.json", 'w') as f:
    print("Writing data to expertise_data.json file")
    json.dump(expertise_data, f)
    print("Process completed.")
