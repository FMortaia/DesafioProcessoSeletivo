from bs4 import BeautifulSoup
import requests
import json

def extrair_categorias(soup):
    return [li.get_text().strip() for li in soup.select('.breadcrumb a')]

def extrair_skus(soup):
    nome = soup.find('meta', {'itemprop': 'name'})
    preco_atual = soup.find('div', {'class': 'prod-pnow'})
    preco_antigo = soup.find('div', {'class': 'prod-pold'})
    disponivel = True
    
    item = {
        'nome': nome['content'],
        'current_price': preco_atual.get_text().strip(),
        'old_price': preco_antigo.get_text().strip(),
        'available': disponivel,
    }
    return item

def extrair_propriedades(soup):
    return [li.get_text().strip() for li in soup.select('.pure-table-bordered td')]

def extrair_reviews(soup):
    pass

def extrair_average_score(soup):
    pass

def raspar_informacoes_produto(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titulo = soup.select_one('h2#product_title')
    brand = soup.select_one('div.brand')
    description = soup.select_one('div.proddet')
    
    informacoes_produto = {
        'title': titulo.get_text(),
        'brand': brand.get_text(),
        'categories': extrair_categorias(soup),
        'description': description.get_text(),
        'skus': extrair_skus(soup),
        'properties': extrair_propriedades(soup),
            
    }
      
    return informacoes_produto

def main():
    url = 'https://infosimples.com/vagas/desafio/commercia/product.html'
    informacoes_produto = raspar_informacoes_produto(url)
    
    with open('produto.json', 'w', encoding='utf-8') as f:
        json.dump(informacoes_produto, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
