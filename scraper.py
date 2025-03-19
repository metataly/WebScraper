import requests
from bs4 import BeautifulSoup

# Função para coletar os dados do site
def scrape_site(url):
        
    # Enviar uma solicitação HTTP para o site
    request = requests.get(url)

    # Retornando o status da requisição
    status = request.status_code
   
    # Verificar se a solicitação foi bem-sucedida (status code 200)
    if status == 200:
        # Dicionário a ser retornado no final
        final_product = {}
        
        # Criar o objeto BeautifulSoup para analisar o HTML
        site = BeautifulSoup(request.text, "html.parser")
        #print(site.prettify())
        
        # Extraindo as informações: nome, codigo de barras, ingredientes
        # Supondo que estamos buscando por um produto específico
        
        # Extraindo o Nome do produto
        product = site.find("h2", class_="title-1")
        # Uso do split porque que a tag <h2> possui mais de um texto
        final_product["name"] = product.get_text().split("\n")[0]
        
        # Extraindo o Codigo de barras
        barcode = site.find("span", id="barcode")
        final_product["barcode"] = barcode.get_text()

        # Extraindo os ingredientes
        # Identificação muito geral, reduzindo o ambiente de pesquisa
        ingredients_div = site.find("div", id="panel_ingredients_content")
        
        if ingredients_div:
            ingredients = ingredients_div.find("div", class_="panel_text")
            final_product["ingredients"] = ingredients.get_text(strip=True)
        else: 
            print("'Elemento Pai' não encontrado!") #Melhorar e adicionar mensagens de erro
    
    # Retornar os dados extraídos em forma de dicionário
    return final_product;
    
def main():
    # Lista de URLs dos produtos que você quer escanear
    urls = ["https://world.openfoodfacts.org/product/7622210584724",
            "https://world.openfoodfacts.org/product/5449000131805", 
            "https://world.openfoodfacts.org/product/6111252860077"]
    
    # Lista para armazenar os dados coletados
    scraped_data = []

    # Iterar sobre as URLs e coletar os dados
    for url in urls:
        data = scrape_site(url)
        
        if data:
            scraped_data.append(data)
    
    
#chamando a função main
if __name__ == "__main__":
    main()
