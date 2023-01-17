
import pandas as pd

#only has one class DataFrame

class DataFrame:
    def __init__(self, datafile):
        #read the datafile in class ReadData
        self.datafile = pd.read_csv(datafile)


#rows

    def min_amount_rows(self, number):
        #number variable is the number of rows min. displayed
        self.number = number
        pd.set_option('display.min_rows', number)

    def replace_rating_rows(self, datarows):
        #datarows variable is the rows that need to be replaced
        self.datarows = datarows
        self.datafile['rating'] = self.datafile['rating'].replace(datarows)

    def change_availability_row(self):
        #change all items in availability row to lower case
        self.datafile['availability'] = self.datafile['availability'].str.lower()


#columns 

    def change_columns_lower_to_upper(self):
        #self.upper_columns = upper_columns
        self.datafile.columns = [x.upper() for x in self.datafile.columns]

        
    def rename_price_column(self):
        #rename price column to price GBP

        self.datafile.rename(columns = {'PRICE': 'PRICE GBP'}, inplace=True)

    def change_rating_to_category(self):   
        #changes rating column to a category
        self.datafile['RATING'] = self.datafile['RATING'].astype('category')
        self.datafile['RATING'] = self.datafile['RATING'].cat.set_categories(['one', 'two', 'three', 'four', 'five'], ordered=True)
        #sorts the rating row
        self.datafile = self.datafile.sort_values('RATING')


    def rerange_column_order(self):   
        #rerange order of the columns
        self.datafile = self.datafile[['TITLE', 'URL', 'RATING', 'AVAILABILITY', 'PRICE GBP', 'PRICE USD']]

    def print_dataframe(self):
        print(self.datafile)

#calls ReadData class and puts it in dataframe -- it calls up the datafile
filepath = '/Users/selledge/Documents/pythonproject/ScrapingProject-main/book_data.csv'
dataframe = DataFrame(filepath)

#calls min_rows method and places it min 20 rows
minrows = dataframe.min_amount_rows(20)

#calls replace_rows method and replaces the rating rows from star-rating to its number
replace_star_rating = dataframe.replace_rating_rows({'star-rating One': 'one','star-rating Two': 'two','star-rating Three': 'three','star-rating Four': 'four','star-rating Five': 'five'})

#calls the change_availability_row method and changes the availability row to all lowercase
lower_case_availability_row = dataframe.change_availability_row()

#calling method to change the columns from lower case to uppercase
upper_column = dataframe.change_columns_lower_to_upper()



#calling the method to rename PRICE column to PRICE GBP
rename_columns = dataframe.rename_price_column()

#calling method to change RATING column to a category method to sort it by number (one through five) in order
rating_category = dataframe.change_rating_to_category()

def price_usd(currency):

    exchange_rate = 1.1451 #static exhange rate taken from google

    currency = currency / exchange_rate #dividing exchange rate to PRICE GBP (currency)

    return round(currency, 2) #rounds it to 2 decimal places

#creates new row with usd price by using the apply method based on the function price_usd
dataframe.datafile['PRICE USD'] = dataframe.datafile['PRICE GBP'].apply(price_usd)

#calls method to rerange column order
rerange_column = dataframe.rerange_column_order()
dataframe.print_dataframe()