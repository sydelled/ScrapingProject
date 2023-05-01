from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time
import random
from datetime import datetime

#####################################################
#csv file that saves all debug errors to the file
#####################################################

def debug_file(message):
   
    try:
        current_date = datetime.today()
        debug_dict = [{'Debug:':message,
        "Date Execution:": str(current_date)}]
        
        debug_dataframe = pd.DataFrame(debug_dict)

    except Exception as v:
        print(f'{v} error was raised. Please check error.')
    
    return debug_dataframe.to_csv('WebScrapDebug.csv', mode='a', index=False)


################################################################################
#function below gets first BeautifulSoup request to find
#all the urls for the product pages that display all the information
#on all 1000 books
################################################################################

###################################################################################
#function that grabs all 50 mainpage urls that each has a url for product pages
###################################################################################

def get_homepage_urls(url):
    retry_count_1 = 0
    page_number = 0
    soup_1_list = []
    page_load = True

    #loop that checks to see whether page load is false
    while page_load == True:
        try:
            #while pages load is true it adds 1 page to the page number
            page_number += 1
            homepage_urls = url + f'catalogue/page-{page_number}.html'
            page_request_1 = requests.get(homepage_urls, timeout=(10))
            soup_1 = BeautifulSoup(page_request_1.text, 'html.parser') #it can display mainpage_url html code
            #checks url for status code 200 which means the url is correct
            if page_request_1.status_code == 200:
                soup_1_list.append(soup_1)
                
            #checks url for status code 404 which means the url is incorrect and is false
            elif page_request_1.status_code == 404:
                #pages don't load and is now false
                page_load = False
                debug_file(f'Code: {page_request_1.status_code} on url: {homepage_urls}.')
            else:
                #check if any other code comes up
                debug_file(f'Code: {page_request_1.status_code} on url: {homepage_urls}.')
        #if any code has come up as an exception to retry the request to see if page loads later
        except Exception as e:
            #if the retry count is less or equal to 2 (after 2 it will stop since it is false)
            if retry_count_1 <= 2:
                #will iterate one after each retry
                retry_count_1 += 1
                #random wait time generated
                random_wait_time = random.uniform(2,4)
                #the time to retry is randomly generated
                time.sleep(random_wait_time)
                debug_file(f'Code: {page_request_1.status_code} on url: {homepage_urls} with exception error: {e}. Trying again in {random_wait_time} seconds. Has retried {retry_count_1} times. ')
            else:
                debug_file(f'Code: {page_request_1.status_code} on url: {homepage_urls} with exception error: {e}. Trying again in {random_wait_time} seconds. Has retried {retry_count_1} times. Max try has exceeded. ')
    
    #shows how many urls have been saved in file
    debug_file(f'The amount of homepage urls that have been saved is {len(soup_1_list)} urls.')
    return soup_1_list#returns list of all 50 mainpages url


################################################################################################
#function that finds each product page url by combining the homepage url with book titles url
################################################################################################

def get_productpages_urls(soup_1, productpage_url):#parameters calls for soup_1(mainpages html) and productpage_urls
    product_urls = [] #booktitle_urls goes into this list below

    #for loop extracts urls from soup_1 list to find class col-xs-6 col-sm-4 col-md-3 col-lg-3
    for soup in soup_1:
        books= soup.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')#find all of this class
        #the code below is the child of the above class and loops through the above list class
        for book in books: #to find the data, it needs to be in a for loop so it can loop through all the data
            product = book.find('article', class_ ='product_pod')
            book_title = product.find('h3')
            book_url = book_title.find('a', href = True)
            get_book_url = book_url.get('href')
            booktitle_urls = productpage_url + str((get_book_url))#adds mainpage url and product page url together
            product_urls.append(booktitle_urls)#append urls to the product_urls list
    return product_urls #returns the product list

###############################################################
#function that calls back ten product urls to test data with
###############################################################
def ten_product_urls(soup_1, productpage_url):
    product_urls=[]
    for soup in soup_1:
        books= soup.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')#find all of this class
        #the code below is the child of the above class and loops through the above list class
        for book in books: #to find the data, it needs to be in a for loop so it can loop through all the data
            product = book.find('article', class_ ='product_pod')
            book_title = product.find('h3')
            book_url = book_title.find('a', href = True)
            get_book_url = book_url.get('href')
            booktitle_urls = productpage_url + str((get_book_url))
            product_urls.append(booktitle_urls)
        return product_urls[0:10]#returns back 10 product urls list

########################################################################################################
#function that requests product urls from get_productpage_urls function and puts it into BeautifulSoup
########################################################################################################

def request_two (booktitle_urls):
    soup_2_list = []
    #loops through booktitle_urls list
    try:
        for urls in booktitle_urls:
        #calls the product_urls into requests through booktitle_urls
        #timeout gives it 20 seconds to connect to the server, and sends an error if timeout occurs
            request_2 = requests.get(urls, timeout=(20))
            soup_2 = BeautifulSoup(request_2.text, 'html.parser')#displays product_urls html
            if request_2.status_code == 200:
                soup_2_list.append(soup_2)#appends soup_2 to soup_2_list
            elif request_2.status_code == 404:
                print(f'Code: {request_2.status_code} on url: {urls}. It needs to be checked.')
            else:
                print(f'Code: {request_2.status_code} on url: {urls}. It needs to be checked.')
    except TypeError as t:
        print(f'Error: {t} has been raised. Urls do not exist from some error.')
    return soup_2_list #returns list of all product pages parsed html

########################################################################################################
#function that gets data from product pages and puts it into a list of dictionaries
########################################################################################################

def get_productpages_data(soup_2):
    products_data_dict_list = []
    for soup in soup_2:
        book_product = soup.find_all('article', class_='product_page') #finds all div's with class content 
        
    #goes through all the div class content in a loop        
        for paragraphs in book_product:
            #finds product title in h1 tag
            product_title = paragraphs.find('h1').text
            _ = paragraphs.find('p', class_='price_color').decompose()#gets rid of price color tag since it isn't needed
            _ = paragraphs.find('i', class_='icon-ok').decompose() #gets rid of i class='icon-ok' since it isn't needed

            #finds instock availability in 'p' tag
            product_availability = paragraphs.find('p', class_='instock availability').text.replace('\n', '').strip(' ')#replaces and stips all the uneeded whitespace 
            _ = paragraphs.find('p', class_='instock availability').decompose()#deletes unnecessary data in 'p' tags
            _ = paragraphs.select_one('p', class_= 'star-rating.One.Two.Three.Four.Five').decompose()#get rid of star-rating class
            
            #finds product descriptions in 'p' tag
            book_summary = paragraphs.find('p').text.replace("â\x80\x99", "'").replace("â\x80\x94", "-").replace("â\x80\x9c", '"').replace("â\x80\x9d", '"').replace('â\x80\x98â\x80', '…').replace('â\x80\x98', "'")

        #put data into a dictionary 
        
            products_data = {
                'Product Title': product_title,
                'Product Availability': product_availability,
                'Product Description': book_summary,
                
            
            }
            
            #appends products_data dictionaries to to products_data_dict_list
            products_data_dict_list.append(products_data)
             
    return products_data_dict_list #returns the list of dictionaries of the product's data

########################################################################
#function that update the list of dictionaries from a list of urls
########################################################################

def put_urls_into_dictionary(urls_list, data_dict_list):
    #loops through the range of indicies in the urls_list
    try:
        for index in range(len(urls_list)):   
            if len(urls_list) == len(data_dict_list):
                #adds new url key to the list of dictionaries
                (data_dict_list[index])['Url']=urls_list[index]
    except TypeError as t:
        print(f'Error: {t} has been raised. The lists length do not match.')
    return data_dict_list#returns list of dictionaries with urls added


########################################################################
#function that converts products data dictionary into a dataframe
########################################################################
def turn_data_into_dataframe(data):
    dataframe = pd.DataFrame(data)
    return dataframe

def dataframe_to_csv(dataframe):
    return dataframe.to_csv('additional_book_data1.csv', mode='a', index=False)


def main():
    #calls back all homepage urls
    mainpage_soup_1 = get_homepage_urls(f'https://books.toscrape.com/')

    #calls back ALL product urls
    product_urls = get_productpages_urls(mainpage_soup_1, f'https://books.toscrape.com/catalogue/')

    #calls back ten product urls for testing purposes ONLY
    ten_products = ten_product_urls(mainpage_soup_1, f'https://books.toscrape.com/catalogue/')

    #calls function that requests product urls into BeautifulSoup
    productpage_soup_2 = request_two(ten_products)

    #calls the function that gets the data for the products from the product pages
    productpages_data = get_productpages_data(productpage_soup_2)

    #calls function that adds url_list to the list of dictionaries
    productdictionary = put_urls_into_dictionary(ten_products, productpages_data)

    #calls function that turns data from product pages into a dataframe
    df = turn_data_into_dataframe(productdictionary)
    print(df)

    #calls function that converts dataframe into csv
    #data_to_csv = dataframe_to_csv(df)

if __name__ == "__main__":
    main()


        