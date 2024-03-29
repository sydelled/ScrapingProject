from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

################################################################################
#function below gets first BeautifulSoup request to find
#all the urls for the product pages that display all the information
#on all 1000 books
################################################################################

def get_homepage_urls(main_index):
    page = 1 #starts at page while and each page adds 1 to it has it go through belows loop
    mainpage_urls = []
    
    while page != 51: #produces pages 1 - 50 to put into homepage_url so it can be placed into requests
        homepage_url = main_index + f'/catalogue/page-{page}.html'#goes into mainpage_url and gets called here
        #main part of url that gets called into def_productpages_urls function
        
        mainpage_urls.append(homepage_url)
        page = page + 1 #adds 1 to each page number until it reaches 50 pages
    return mainpage_urls

def request_one(mainpage_url):#parameter calls the all 50 pages of the homepage url
        #calls mainpage_url through requests
        #timeout gives it 10 seconds to connect to ther server, and timeout if server does not send any data
       
        
        for url in mainpage_url:
            request_1 = requests.get(url, timeout=(10, 200))
            soup_1 = BeautifulSoup(request_1.text, 'html.parser') #it can display mainpage_url html code
        print(soup_1)
            
        return soup_1 #returns html of all 50 mainpages

def get_productpages_urls(soup_1, productpage_url):#parameters calls for soup_1(mainpages html) and productpage_urls
    product_urls = [] #booktitle_urls goes into this list below
    books= soup_1.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')#find all of this class
    
    #the code below is the child of the above class and loops through the list class
    for book in books: #to find the data, it needs to be in a for loop so it can loop through all the data
        product = book.find('article', class_ ='product_pod')
        book_title = product.find('h3')
        book_url = book_title.find('a', href = True)
        get_book_url = book_url.get('href')
        booktitle_urls = productpage_url + str((get_book_url))#adds mainpage url and product page url together
        product_urls.append(booktitle_urls)#append urls to the product_urls list
    return product_urls #returns the product list

def request_two (booktitle_urls):
    #calls the product_urls into requests through booktitle_urls
    #timeout gives it 10 seconds to connect to ther server, and timeout if server does not send any data
    request_2 = requests.get(booktitle_urls, timeout=(10, 200))
    soup_2 = BeautifulSoup(request_2.text, 'html.parser')#displays product_urls html
    return soup_2 #returns html of all product pages urls

def get_productpages_data(soup_2):
    products_data =[]
    book_product = soup_2.find_all('div', class_='content_inner') #finds all div's with class content 

    #goes through all the div class content in a loop        
    for product in book_product:
        #content_inner = product.find('div', id_='content_inner')
        #replace data instock availabity with this data
        #shows how much product is in stock
        product_title = product.find('h1')#finds product titles
        instock_availability = product_title.find('i', class_='icon-ok').decompose() #gets rid of i class='icon-ok'
        #replaces and stips all the uneeded whitespace
        availability_number = instock_availability.find('p', class_='instock availability').text.replace('\n', '').strip(' ') 
        products_data.append(product_title, availability_number)
    return products_data #returns the descriptions of all the books (products)



mainpage_urls = get_homepage_urls(f'https://books.toscrape.com/')

book_request_one = request_one(mainpage_urls)   
print(book_request_one)


#loops through all 50 homepage urls in while loop and calls
# book_request_one and get_product_pages _urls functions
#for url in range(0,51):
#for url in mainpage_urls:
#    book_request_one = request_one(url)#calls book_request_one to displays mainpage_urls html
#    urls = get_productpages_urls(book_request_one, f'https://books.toscrape.com/catalogue/') #calls the function in the while looping through all 50 pages
    #print(urls)
#    for request in urls:
#        book_request_two = request_two(request)
#        productpages = get_productpages_data(book_request_two)
        #print(productpages)



           




   