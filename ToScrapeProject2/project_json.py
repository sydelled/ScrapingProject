from bs4 import BeautifulSoup
import requests
import re
import json


page = 1
books_list = []
while page != 51:
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    reg = requests.get(url)
    soup = BeautifulSoup(reg.text, 'lxml')
    page = page + 1
    

    books= soup.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

    
    for book in books:  

        book_titles = book.find('a', title = True)
        get_book_titles = book_titles.get('title') 

        book_url = book.find('a', href = True)
        get_book_url = book_url.get('href') 
        
        book_rating = book.select_one('p', class_= 'star-rating.One.Two.Three.Four.Five')
        
        star_rating = re.search("star-rating (One|Two|Three|Four|Five)", str(book_rating)).group()
        
        book_price = book.find("p", class_ = "price_color").text.replace('Â£', '')
        
        stock = book.find('p', class_='instock availability').text.replace(' ', '').replace('\n', '')
        

    #convert to json file
        
    #put info in a dictionary

        print_books = {
            'title': get_book_titles,
            'url': get_book_url,
            'rating': star_rating,
            'price': book_price,
            'availability': stock
        }
        
        #append the dictionary info into a list

        books_list.append(print_books)

        #open and write to a json file
        
        with open('book_data.json', 'w') as f:
            
            json.dump(books_list, f)





