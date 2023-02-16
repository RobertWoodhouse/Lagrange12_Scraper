'''
Lagrange12 Web Scraper
Author: Robert Woodhouse
Created: 25/01/2023
Modified: 16/02/2023
'''

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas
import sqlite3

browser = webdriver.Chrome('/Applications/chromedriver_mac64/chromedriver')
browser.delete_all_cookies()
gender = ("men/", "women/")
category = ("new-arrivals", "clothing", "shoes", "bags", "accessories", "jewels", "objects")
number_of_products = 0
links = []
product_list = []

def open_browser_soup(url):
    browser.get(url)
    return BeautifulSoup(browser.page_source, "html.parser")

# Link Builder
'''
print("[0] Men | [1] Women \nEnter Gender: ")
gender_input = input()
print("[0] New Arrivals | [1] Clothing | [2] Shoes  | "
      "[3] Bags  | [4] Accessories  | [5] Jewels  | [6] Objects \nEnter Category:")
category_input = input()

browser.get("https://www.lagrange12.com/en_uk/"+gender[int(g_input)]+category[int(c_input)]+".html")
'''

def build_link_list(url, num_of_results):
    count = 1
    while(len(links) <= num_of_results):
        soup = open_browser_soup(url)
        result = soup.find('ol', class_='small-12 products list items product-items')
        results = result.find_all('li')

        for res in results:
            links.append(res.find('a').get('href'))
            #print("Number of links = " + str(len(links)) + " out of " + str(num_of_results))
            if len(links) == num_of_results:
                break

        if len(links) == num_of_results:
            break
        else:
            count += 1
            url = url + "?p=" + str(count)
            #print(url)

# Hard Coded URL
build_link_list('https://www.lagrange12.com/en_uk/men/shoes.html', num_of_results=2)

product_dict = {"name": [],
                "sku": [],
                "value": [],
                "brand": [],
                "description": []}

for link in links:
    #print(link)
    soup = open_browser_soup(link)
    res = soup.find('div', class_="product-detail small-12 medium-offset-1 medium-11 large-offset-2 large-10")
    title_id = res.find_all('p', class_="title")
    value = res.find('span', class_="price") #TODO stop json from changing char uni code
    brand = res.find('span', class_="base")
    description = res.find('div', class_="description").find('p') #TODO change to find_all list and seperate with /n

    product_dict["name"] += [title_id[0].getText()]
    product_dict["sku"] += [title_id[1].getText()]
    product_dict["value"] += [value.getText().replace('\u00a3', '£')]
    product_dict["brand"] += [brand.getText().strip()]
    product_dict["description"] += [description.getText()]


#TODO write save_as functions
df = pandas.DataFrame(data=product_dict)
df.to_json('l12.json', indent=3, orient='records')
df.to_csv('l12.csv', index=False)
#df.to_sql(name='l12.sql', con=sqlite3.Connection)

browser.close()

#TODO
'''
[+] Go through links array, load pages of products and scrape info from them
[+] Scrape the following: div class="product-detail small-12 medium-offset-1 medium-11 large-offset-2 large-10"
[+] product_name | p class="title"
[+] sku | p class="title"
[+] value | span class="price"
[+] product_brand | span class="base"
[+] Description | div data-content-type="row" / div data-content-type="text"
[+] category | {category var}
[+] product_gender | {gender var}
[+] Save info to a List of Dictionaries
[-] Convert from Dictionary to SQL file
[+] Scrape the first 100 available search results
    > Build the code to fetch the first 100 search results.
    > Write functions that allow you to specify the gender, category, and amount of results as arguments
[+] Generalize your code to allow searching for different gender and category
[+] Pick out information about the URL, gender, and category
[+] Save the results to a file
[+] Build web-scraping models using Python.
[-] Gather data from multiple sources and pull it into a SQL database.

'''