'''
Lagrange12 Web Scraper
Author: Robert Woodhouse
Last Modified: 29/01/2023
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import json

browser = webdriver.Chrome('/Applications/chromedriver_mac64/chromedriver')
browser.delete_all_cookies()
gender = ("men/", "women/")
category = ("new-arrivals", "clothing", "shoes", "bags", "accessories", "jewels", "objects")
product_list = []


def cook_soup(url):
    browser.get(url)
    return BeautifulSoup(browser.page_source, "html.parser")

'''
print("[0] Men | [1] Women \nEnter Gender: ")
g_input = input()
print("[0] New Arrivals | [1] Clothing | [2] Shoes  | "
      "[3] Bags  | [4] Accessories  | [5] Jewels  | [6] Objects \nEnter Category:")
c_input = input()

browser.get("https://www.lagrange12.com/en_uk/"+gender[int(g_input)]+category[int(c_input)]+".html")
'''

# Hard Coded URL:
soup = cook_soup("https://www.lagrange12.com/en_uk/men/shoes.html")

#headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

result = soup.find('ol', class_='small-12 products list items product-items')
#results = result.find_all('li', class_='medium-6 large-3 item product product-item small-6')
results = result.find_all('li')

links = []

for res in results:
    links.append(res.find('a').get('href'))

i = 0

for link in links:
    soup = cook_soup(link)
    res = soup.find('div', class_="product-detail small-12 medium-offset-1 medium-11 large-offset-2 large-10")
    title_id = res.find_all('p', class_="title")
    value = res.find('span', class_="price")
    brand = res.find('span', class_="base")
    description = res.find('div', class_="description").find('p') #TODO change to find_all list and seperate with /n

    product_dict = {"name": title_id[0].getText(),
                 "sku": title_id[1].getText(),
                 "value": value.getText().replace('\u00a3', '£'),
                 "brand": brand.getText().strip(),
                 "description": description.getText()}
                #"category": category[c_input],
                #"gender": gender[g_input]}

    print(value.getText())
    product_list.append(product_dict)
'''
    i += 1
    if i > 2:
        break
'''

product_json = json.dumps(product_list, indent=3)

with open("lagrange_products.json", "w") as outfile:
    outfile.write(product_json)

print(product_json)

browser.close()

#TODO
'''
+ Go through links array, load pages of products and scrape info from them
+ Scrape the following: div class="product-detail small-12 medium-offset-1 medium-11 large-offset-2 large-10"
[+] product_name | p class="title"
[+] sku | p class="title"
[+] value | span class="price"
[+] product_brand | span class="base"
[+] Description | div data-content-type="row" / div data-content-type="text"
[+] category | {category var}
[+] product_gender | {gender var}
+ Save info to a List of Dictionaries
- Convert from List of Dictionaries to SQL file
'''

'''
- Scrape the first 100 available search results
+ Generalize your code to allow searching for different locations/jobs
+ Pick out information about the URL, job title, and job location
+ Save the results to a file


- Build web-scraping models using Python.
- Gathering data from multiple sources and pulling it into a SQL database.
- Collaborating with the Data Science team and preparing the data for their use, allowing
'''