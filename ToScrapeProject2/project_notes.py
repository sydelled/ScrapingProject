#notes used in ToScrapeProject2

from bs4 import BeautifulSoup
import requests
import re
import json


page = 1

while page != 51:
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    reg = requests.get(url)
    soup = BeautifulSoup(reg.text, 'lxml')
    page = page + 1
    

    books= soup.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

    
    for book in books:  

        #find book titles
        book_titles = book.find('a', title = True)
        get_book_titles = book_titles.get('title') 

        #find book url
        book_url = book.find('a', href = True)
        get_book_url = book_url.get('href') 
        
        #select correct class from mutiple classes
        book_rating = book.select_one('p', class_= 'star-rating.One.Two.Three.Four.Five')
        
        #search for a specific string in a larger string
        star_rating = re.search("star-rating (One|Two|Three|Four|Five)", str(book_rating))
        #star_rating = re.findall("star-rating (One|Two|Three|Four|Five)", str(book_rating))
        #if star_rating is not None:
        #    star_rating.group() 
        

        #find book price
        book_price = book.find("p", class_ = "price_color")
        #get_book_price = book_price[2:] 
        #get_book_price = book_price.getText()
        #split_book_price = get_book_price.split()[-1]

        #find whether book is in stock
        stock = book.find('p', class_='instock availability')
        availability = re.search("In stock", str(stock))
        #availability = re.findall("In stock", str(stock))

        #if availability is not None:
        #     availability.group() 
        

    #convert to json file
        
        books_list = []

        
        
        print_books = {
            'title': get_book_titles,
            'url': get_book_url,
            'rating': str(star_rating),
            'price': book_price,
            'availability': str(availability)
        }
        
        #data = {'rating': star_rating.text, 'availability': availability.text}
        books_list.append(print_books)
        
        
        #with open('book_data.json', 'w') as f:
            
        #    json.dump(books_list, f)

type(print_books)
    
    
    #convert into text file
    
    #f = open('bookinformation.txt', 'a')
    #f.write("Title: " + book_titles.get('title') + '\n')
    #f.write("URL: " + book_url.get('href') + '\n')
    #if star_rating is not None:
    #    f.write("Rating: " + star_rating.group() + '\n')
    #if availability is not None:
    #    f.write("Availability: " + availability.group() + '\n\n')
#f.close()

#print(type(get_book_titles))
#print(type(get_book_url))
#print(type(star_rating))
#print(type(book_price))
#print(type(stock))

#print(books_list)
        
        

        
        
        
        
        
        
    
        
        

        
        
        
        
     






