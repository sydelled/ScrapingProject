
import pandas as pd
import csv

#THE FILE PROJECT3_CLASSES_FILE_COMPLETE has the complete data



#has several classes to show inhertience
#I can put ReadData class and Rows class in one class but I'm practicing class inheritance

#class ReadData that reads the data in the filepath
class ReadData:
    def __init__(self, datafile):
        #read the file book_data.csv and put it in datafile 
        self.datafile = pd.read_csv(datafile)

        
#calls ReadData class and puts it in dataframe -- it calls up the datafile
filepath = '/Users/selledge/Documents/pythonproject/ScrapingProject-main/book_data.csv' #path to the book_data file
#calls method ReadData and puts it in dataframe
dataframe = ReadData(filepath)

#class Rows that has function that changes the rows and uses the filepath book_data.csv
class Rows(ReadData):

   #this init function has to match the parameters of the ReadData function
   #init function should always be called in classes

    def __init__(self, datafile):

        #this super function calls the intermediate class (ReadData) and has to have
        #the same amount of positioninal argument (minus self since the super function doesn't take self)

        super().__init__(datafile)
        
    def replace_rating_rows(self, datarows):
        #datarows variable is the rating rows that need to be replaced
        self.datarows = datarows
        self.datafile['rating'] = self.datafile['rating'].replace(datarows)

    def change_availability_row(self):
        #change all items in availability row to lower case
        self.datafile['availability'] = self.datafile['availability'].str.lower()
        

#calls Rows class and it inherits ReadData class in order to use the same book_data.csv filepath
rows_data = Rows(filepath)

#calls replace_rows method and replaces the rating rows from star-rating to its number
replace_star_rating = rows_data.replace_rating_rows({'star-rating One': 'one','star-rating Two': 'two','star-rating Three': 'three','star-rating Four': 'four','star-rating Five': 'five'})

#calls the change_availability_row method and changes the availability row to all lowercase
lower_case_availability_row = rows_data.change_availability_row()

#function to change BRITISH currency to USA currency
def price_usd(currency):

    exchange_rate = 1.1451 #static exhange rate taken from google

    currency = currency / exchange_rate #dividing exchange rate to PRICE GBP (currency)

    return round(currency, 2) #rounds it to 2 decimal places

#creates new row with usd price by using the apply method based on the function price_usd
#creates row that shows the prices for USA currency
rows_data.datafile['price usd'] = rows_data.datafile['price'].apply(price_usd)

#saves rows_data class object changes to a csv file
rows_data.datafile.to_csv('/Users/selledge/Documents/pythonproject/ScrapingProject-main/project3_classes_file1.csv', index=False)

#class Columns has function that changes the data in the columns and uses the filepath project3_classes_file1
class Columns:

    def __init__(self, rows_datafile):
        #reading rows_data csv file to make changes to it
        self.rows_datafile = pd.read_csv(rows_datafile)

    def change_columns_lower_to_upper(self):
        self.rows_datafile.columns = [x.upper() for x in self.rows_datafile.columns]

    def rename_price_column(self):
        #rename price column to price GBP
        self.rows_datafile.rename(columns = {'PRICE': 'PRICE GBP'}, inplace=True)

    def change_rating_to_category(self):   
        #changes rating column to a category so each rating can be sorted in order (example: one, two, three...)
        self.rows_datafile['RATING'] = self.rows_datafile['RATING'].astype('category')
        self.rows_datafile['RATING'] = self.rows_datafile['RATING'].cat.set_categories(['one', 'two', 'three', 'four', 'five'], ordered=True)
        #sorts the rating row so each rating is sorted in order
        self.rows_datafile = self.rows_datafile.sort_values('RATING')

    def rerange_order_columns(self):
        #rerange order of the columns
        self.rows_datafile = self.rows_datafile[['TITLE', 'URL', 'RATING', 'AVAILABILITY', 'PRICE GBP', 'PRICE USD']]

#filepath project3_classes_file1.csv for rows dataframe  
rows_filepath = '/Users/selledge/Documents/pythonproject/ScrapingProject-main/project3_classes_file1.csv'

#calling method for Columns class object
columns_data = Columns(rows_filepath)

#calling method for changing columns to uppercase
upper_column = columns_data.change_columns_lower_to_upper()

#calling the method to rename PRICE column to PRICE GBP
rename_columns = columns_data.rename_price_column()

#calling method to change RATING column to a category method to sort it by number (one through five) in order
rating_category = columns_data.change_rating_to_category()

#below functions takes the PRICE GBP row and applies the exchange rate to convert it to US DOLLARS
#price_usd function
def price_usd(currency):

    exchange_rate = 1.1451 #static exhange rate taken from google

    currency = currency / exchange_rate #dividing exchange rate to PRICE GBP (currency)

    return round(currency, 2) #rounds it to 2 decimal places

#creates new row with usd price by using the apply method based on the function price_usd
columns_data.rows_datafile['PRICE USD'] = columns_data.rows_datafile['PRICE GBP'].apply(price_usd)

#calls method to rerange the columns
order_columns = columns_data.rerange_order_columns()

#resets all indexes in the dataframe
columns_data.rows_datafile.reset_index(drop=True, inplace=True)

#saving changes to rows_dataframe and resaving it to a new csv file project3_classes_file_complete.csv
columns_data.rows_datafile.to_csv('/Users/selledge/Documents/pythonproject/ScrapingProject-main/project3_classes_file_complete.csv', index=False)










               


























