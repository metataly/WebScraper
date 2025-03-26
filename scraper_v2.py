import requests
from bs4 import BeautifulSoup

# Function to collect data from the website
def scrape_site(url):
    
    # Send an HTTP request to the website
    request = requests.get(url)

    # Returning request status
    status = request.status_code
   
    # Checking if the request was successful
    if status == 200:
        # Dicionary to be returned at the end
        final_product = {}
        
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
            final_product["barcode"] = barcode.get_text()
        else:
            final_product["barcode"] = "Product barcode not found!"
            
        # Extracting product ingredients
        # Narrowing down the search scope
        ingredients_div = site.find("div", id="panel_ingredients_content")
        
        if ingredients_div:
            ingredients = ingredients_div.find("div", class_="panel_text")
            final_product["ingredients"] = ingredients.get_text(strip=True)
        else: 
            print("Product ingredients not found!")
    
    print(final_product) ### apenas para fins de teste
    
    # Returning extracted data in the form of a dicionary
    return final_product
      
def main():
    # List of products URLs that you want to scan 
    urls = ["https://world.openfoodfacts.org/product/7622210584724",
            "https://world.openfoodfacts.org/product/5449000131805", 
            "https://world.openfoodfacts.org/product/3175680011480"]
    
    # List to store collected data
    scraped_data = []

    # Iterate over the URLs and collect the data
    for url in urls:
        data = scrape_site(url)
        
        if data:
            scraped_data.append(data)
    
    
# Main function 
if __name__ == "__main__":
    main()
