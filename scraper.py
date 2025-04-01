import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd


# Function to collect data from the dinamic website
def scrape_site(url):
    
    options = Options()
    options.add_argument("--headless")
    
    # Creating a webdriver of chrome
    navigator = webdriver.Chrome(options=options) 
    navigator.get(url)
    # Waiting all data load
    sleep(5)

    # Extracting contry from the selector TAG by click
    country = navigator.find_element(By.CLASS_NAME, 'select2')
    country.click()
    sleep(3)
    
    # Writing contry name on the Input TAG 
    search = navigator.find_element(By.CLASS_NAME, 'select2-search__field')
    # Write here: 
    search.send_keys('brazil')
    sleep(5)
    # Sanding by 'Enter'
    search.send_keys(Keys.RETURN)
    sleep(5)

    # Creating a BeautifulSoup object to analyze the HTML
    site = BeautifulSoup(navigator.page_source, "html.parser")
    #print(site.prettify())

    # Extracting url of 5 itens in the selected contry page
    product_url = site.find_all("a", class_="list_product_a")[:100]
    list_product = []
    
    # Catching only href atribute
    for url in product_url:
        list_product.append(url['href'])
    
    navigator.quit()
    # Returning a list of urls
    return list_product

# Function to collect data from the website using url of a product
def scrape_product(urls_products):
    
    # Send an HTTP request to the website
    request = requests.get(urls_products)

    # Returning request status
    status = request.status_code
    
    # Dicionary to be returned at the end
    final_product = {}
    # Checking if the request was successful
    if status == 200:
        
        # Creating a BeautifulSoup object to analyze the HTML
        site = BeautifulSoup(request.text, "html.parser")
        #print(site.prettify())
        
        # Extracting informations: name, barcode, ingredients
        # Assuming we are searching for a specific product
        
        # Extracting product name
        product = site.find("h2", class_="title-1")
        
        # checking if the product name was found
        if product:
            # Using '.split()' because the tag 'h2' contains more than one text
            final_product["name"] = product.get_text().split("\n")[0]
        else:
           final_product["name"] = "Product name not found!"
        
        # Extracting product barcode
        barcode = site.find("span", id="barcode")
        
        if barcode:
            final_product["barcode"] = barcode.get_text(strip=True)
        else:
            final_product["barcode"] = "Product barcode not found!"
            
        # Extracting product ingredients
        # Narrowing down the search scope
        ingredients_div = site.find("div", id="panel_ingredients_content")
        
        if ingredients_div:
            ingredients = ingredients_div.find("div", class_="panel_text")
            
            if ingredients:
                final_product["ingredients"] = ingredients.get_text(strip=True)
            else: 
                final_product["ingredients"] = "Product ingredients not found!"
        else: 
           final_product["ingredients"] = "Product ingredients not found!"
    else:
        print(f"Error: {status} on URL {urls_products}")

    # Returning extracted data in the form of a dicionary
    return final_product

# Function to save the data on csv archive 
def save_to_csv(data, filename="scraped_data.csv"):

    # Converting the scraped data on a DataFrame 
    data_df = pd.DataFrame(data)
    
    # Converting the DataFrame on csv
    data_df.to_csv(filename, index=False, encoding="utf-8")


def main():
    # URL from website that you want to scan 
    url = "https://world.openfoodfacts.org"
    
    # Returned list of URLs
    urls = scrape_site(url)
    
    # List to save the product data
    products = []
    
    # Extracting data from URL
    for url in urls:
        sleep(2)
        product = scrape_product(url)  

        if product:
            products.append(product)
            
    # Saving data to csv
    save_to_csv(products)

# Main function 
if __name__ == "__main__":
    main()
