from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

################################################################################
#function below gets first BeautifulSoup request to find
#all the urls for the product pages that display all the information
#on all 1000 books
################################################################################

################################################################################################
#function that grabs all 50 mainpage urls that each has a url for product pages
################################################################################################

def get_homepage_urls(main_index):
    homepage_urls_list = []
    page = 1 #starts at page while and each page adds 1 to it has it go through belows loop
    
    while page != 51: #produces pages 1 - 50 to put into homepage_url so it can be placed into requests
        homepage_url = main_index + f'/catalogue/page-{page}.html'#goes into mainpage_url and gets called here
        #timeout gives it 10 seconds to connect to ther server, and timeout if server does not send any data
        homepage_urls_list.append(homepage_url)
        page = page + 1 #adds 1 to each page number until it reaches 50 pages
    return homepage_urls_list #returns list of all 50 mainpages url

################################################################################################
#function requests homepage_urls_list into BeautifulSoup to parse urls into html
################################################################################################

def request_one(homepage_urls_list):
    soup_1_list = []
    for url in homepage_urls_list:
        request_1 = requests.get(url, timeout=(10)) 
        soup_1 = BeautifulSoup(request_1.text, 'html.parser') #it can display mainpage_url html code
        soup_1_list.append(soup_1)#appends soup_1 into a the soup_1_list
    return soup_1_list

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

    for urls in booktitle_urls:
    #calls the product_urls into requests through booktitle_urls
    #timeout gives it 20 seconds to connect to the server, and sends an error if timeout occurs
        request_2 = requests.get(urls, timeout=(20))
        soup_2 = BeautifulSoup(request_2.text, 'html.parser')#displays product_urls html
        soup_2_list.append(soup_2)#appends soup_2 to soup_2_list
    return soup_2_list #returns list of all product pages parsed html

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
            book_summary = paragraphs.find('p').text

            replacements = [("â\x80\x99", "'"), ("â\x80\x94", "-"), ("â\x80\x9c", '"'),("â\x80\x9d", '"'), ('â\x80\x98â\x80', '…'), ('â\x80\x98', "'")]#symbols that need replacing in a list
        #for loop that iterates over replacements list to replace the symbols in the book summary paragraph
            for characters, replacement in replacements:
                if characters in book_summary:
                    book_summary = book_summary.replace(characters, replacement)#the characters in tuple must be replaced into a string variable replaceme

        
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
    for index in range(len(urls_list)):
        #adds new url key to the list of dictionaries
       (data_dict_list[index])['Url']=urls_list[index]
    return data_dict_list#returns list of dictionaries with urls added


########################################################################
#function that converts products data dictionary into a dataframe
########################################################################
def turn_data_into_dataframe(data):
    dataframe = pd.DataFrame(data)
    return dataframe

def dataframe_to_csv(dataframe):
    return dataframe.to_csv('additional_book_data1.csv', mode='a', index=False)

def print_ten_rows_dataframe(ten_rows_data):
    return print (ten_rows_data.head(10))

def main():
    #calls back all homepage urls
    mainpage_urls = get_homepage_urls(f'https://books.toscrape.com')

    #calls function that requests all homepage urls into BeautifulSoup
    mainpage_soup_1 = request_one(mainpage_urls)

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
    data_to_csv = dataframe_to_csv(df)

if __name__ == "__main__":
    main()


        