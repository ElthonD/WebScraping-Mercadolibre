import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time
import csv

def obtener_titulo(soup):
    
    #Extraer los títulos de las variantes del producto

    try:
        
        titulo = soup.find("h1", attrs={"class":'ui-pdp-title'}).text.strip()

    except AttributeError:
        titulo = "Sin Título"

    return titulo

def obtener_precio(soup):        

    try:
        # Extraer precios
        product_price_fraction = soup.find("span", attrs={"class":'andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact'}).find("span", attrs={"class": "andes-money-amount__fraction"}).text.strip(',')
        product_price_cents = soup.find("span", attrs={"class":'andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact'}).find("span", attrs={"class": "andes-money-amount__cents andes-money-amount__cents--superscript-36"}).text
        precio = product_price_fraction + '.' + product_price_cents

    except:
        precio = "Sin Precio"

    return precio

def obtener_tipo_producto(soup):
    # Extraer el tipo de producto 
    try:
    
        tipo = soup.find("span", attrs={"class":'ui-pdp-variations__selected-text'}).text.strip()

    except AttributeError:
        tipo = "Sin Detalle"

    return tipo


def obtener_disponibilidad(soup):
    
    # Extraer Disponibilidad del Producto
    
    try:
        
        disponibilidad = soup.find("p", attrs={"class":'ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--SEMIBOLD ui-pdp-stock-information__title'}).text.strip()

    except AttributeError:
        
        disponibilidad = "No se cuenta con Inventario Disponible"
    
    return disponibilidad

def obtener_cantidad(soup):
    
    #Extraer Cantidad del producto
    
    try:
        cantidad = soup.find("span", attrs={"class":'ui-pdp-buybox__quantity__available'}).text.strip('() disponibles')
        
    except AttributeError:
        
        cantidad = "No Disponible"

    return cantidad

if __name__ == '__main__':
    
    while True:
        
        today = datetime.datetime.now()
        hoy = today.strftime('%Y-%m-%d %H:%M:%S')
    
        # agregar user agent 
        HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

        # URL Mercadolibre
        URL = 'https://www.mercadolibre.com.mx/colchon-luuna-memory-foam-individual-hecho-en-mexico/p/MLM15569488'

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object que contiene todo el HTML
        soup = BeautifulSoup(webpage.content, "html.parser")
    
        # Fetch links como Lista (Objetos Tag)
        links1 = soup.find_all("a", attrs={'class':'ui-pdp-thumbnail ui-pdp-variations--thumbnail ui-pdp-thumbnail--SELECTED'})
        links2 = soup.find_all("a", attrs={'class':'ui-pdp-thumbnail ui-pdp-variations--thumbnail ui-pdp-thumbnail--DISABLED'})
        links = links1 + links2

        # Almacenar los links
        links_list = []

        # Loop para extraer los links de las variantes de un producto
        for link in links:
            links_list.append(link.get('href'))

        d = {"Fecha": [], "Título":[], "Precio":[], "Tipo":[], "Disponibilidad":[],"Cantidad":[]}
        
        with open('AmazonLuunaDataset.csv', 'w', encoding='latin1', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(d.keys())
    
        # Loop para extraer los detalles de las variantes de un producto por cada link
        for link in links_list:
            new_webpage = requests.get("https://www.mercadolibre.com.mx" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
    
            # Aplicar funciones para agregar fecha y extraer titulo, precio, tipo, disponibilidad y cantidad
            d['Fecha'].append(hoy)
            d['Título'].append(obtener_titulo(new_soup))
            d['Precio'].append(obtener_precio(new_soup))
            d['Tipo'].append(obtener_tipo_producto(new_soup))
            d['Disponibilidad'].append(obtener_disponibilidad(new_soup))
            d['Cantidad'].append(obtener_cantidad(new_soup)) 
        
        #df = pd.DataFrame.from_dict(d)
        #df.to_csv("AmazonLuunaDataset.csv", header=True, index=False)
        
        #Para agregar diariamente la información extraída
        with open('AmazonLuunaDataset.csv', 'a+', encoding='latin1', newline='') as f:
            writer = csv.writer(f)
            for iteration in range(len(d.keys())):
                writer.writerow([val[iteration] for val in d.values()])
        
        #Timer para ejecución del script una vez por dia
        time.sleep(86400)
        
        break