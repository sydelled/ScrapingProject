from bs4 import BeautifulSoup
import requests

page = 2
while page != 51:
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    print(url)
    page = page + 1







#url_text = ['http://books.toscrape.com/', 'http://books.toscrape.com/catalogue/page-2.html', 'https://books.toscrape.com/catalogue/page-50.html']

#for url in range(0, 3):
#    reg = requests.get(url_text[url])
#    soup = BeautifulSoup(reg.text, 'lxml')

#    books= soup.find_all('li', class_= 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
#    for book in books:  
#        book_titles = book.find('a', title = True)

#        print(book_titles.get('title'))