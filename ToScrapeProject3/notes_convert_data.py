import pandas as pd

#opening csv file book_data.csv into a dataframe
dataframe = pd.read_csv('/Users/selledge/Documents/pythonproject/ScrapingProject-main/book_data.csv')

#change column names to all upper case
dataframe.columns = [x.upper() for x in dataframe.columns]

#change all data in availability row to lower case
dataframe['AVAILABILITY'] = dataframe['AVAILABILITY'].str.lower()

#change the RATING row to show that rating for each book as one, two, etc., instead star rating: One, etc.
dataframe['RATING']= dataframe['RATING'].replace({'star-rating One': 'one','star-rating Two': 'two','star-rating Three': 'three','star-rating Four': 'four','star-rating Five': 'five'})

#rename PRICE column to price GBP (british pounds)
dataframe.rename(columns = {'PRICE': 'PRICE GBP'}, inplace=True)

#change british pounds to usd dollars


def price_usd(currency):

    exchange_rate = 1.1451 #static exchange rate found on google

    currency = currency / exchange_rate

    return round(currency, 2)

#creates new row with usd price by using the apply method based on the function price_usd
dataframe['PRICE USD'] = dataframe['PRICE GBP'].apply(price_usd)

#changes rating column to a category so all stars rated one can be together, then two stars, etc....
dataframe['RATING'] = dataframe['RATING'].astype('category')
dataframe['RATING'] = dataframe['RATING'].cat.set_categories(['one', 'two', 'three', 'four', 'five'], ordered=True)

#sorts the rating row so books rated one starts first in the row, then books rated two comes after, etc...
dataframe = dataframe.sort_values('RATING')

#rerange order of the columns so the price columns are together
dataframe = dataframe[['TITLE', 'URL', 'RATING', 'AVAILABILITY', 'PRICE GBP', 'PRICE USD']]

#group the rating first (for example: all books rated one star gets grouped together, then two stars, etc...)
rating_grp = dataframe.groupby(['RATING'], as_index=False)

#returns the median price for each rating (example: all books rated one star as a median rating, then two stars, etc...)
median_rating = rating_grp['PRICE USD'].median()

#resets all indexes in the dataframe
dataframe.reset_index(drop=True, inplace=True)

#puts median data for each rating into a Pandas Series from original dataframe
median_data = pd.Series([median_rating], name = 'MEDIAN PRICE PER BOOK RATING')


#puts dataframe into a csv file convert_data.csv
#dataframe.to_csv('/Users/selledge/Documents/pythonproject/ScrapingProject-main/convert_data.csv', index=False)

#puts the Series containing the median price per rating into another csv file median_price_per_rating
median_data.to_csv('/Users/selledge/Documents/pythonproject/ScrapingProject-main/median_price_per_rating.csv', index=False)

#print(median_rating)
