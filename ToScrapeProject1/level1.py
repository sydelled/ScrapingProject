from bs4 import BeautifulSoup
import requests

url_text = requests.get('http://books.toscrape.com/').text
soup = BeautifulSoup(url_text, 'lxml')

books= soup.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')

for book in books:
    book_titles = book.find('a', title = True)
    book_price = book.find("p", class_ = "price_color").text

    f = open('bookstext/booktitles.txt', 'a')
    f.write("Title: " + book_titles.get('title') + "\n\n")        
    f.write("Price: " + book_price[2:] + "\n\n")
    
f.close()


