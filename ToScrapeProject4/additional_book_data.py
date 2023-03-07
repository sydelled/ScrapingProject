from bs4 import BeautifulSoup
import requests
import re
import pandas as pd



#getting the main page url through requests and beautifulsoup


page = 1
while page != 51: #iterates through all 50 pages
    homepage_url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    request_1 = requests.get(homepage_url)
    soup_1 = BeautifulSoup(request_1.text, 'lxml')
    page = page + 1 #adds the page number 1-50 to url
        


#getting the product page url for all 1000 books 
#needed to get the mainpage url plus url for each product page
#the parent being the h3 heading and child a href tag

    books= soup_1.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for book in books:
        product = book.find('article', class_ ='product_pod')
        book_title = product.find('h3')
        book_url = book_title.find('a', href = True)
        get_book_url = book_url.get('href')
        productpage_url = 'https://books.toscrape.com/catalogue/' + str((get_book_url))#adds mainpage url and product page url together
        #print(productpage_url)
    
    #putting the product page url through requests 
    #that way data can be obtain from each of these urls

        request_2 = requests.get(productpage_url)
        soup_2 = BeautifulSoup(request_2.text, 'lxml')


        book_product = soup_2.find_all('div', class_='content')  
            
        for product in book_product:
            content_inner = product.find('div', id_='content_inner')
            #replace data instock availabity with this data
            #shows how much product is in stock
        
            product_title = product.find('h1')
            instock_availability = product.find('i', class_='icon-ok').decompose() #gets rid of i class='icon-ok'
            product_description = product.find('p', class_='instock availability').text.replace('\n', '').strip(' ') #replaces and stips all the uneeded whitespace
            #print(product_description)

            #put data into a dictionary so it can be made into a dataframe
            product_data = [{
                'Product Title': product_title,
                'Product Availability': product_description 


            }]
            
            print(product_data)
            #create dataframe with product_data

            #product_dataframe = pd.DataFrame(product_data, index=True)
            
            #display_min_rows = pd.set_option('display.min_rows', 10)
            
            #print(product_dataframe)
            #print(product_dataframe.head(10))