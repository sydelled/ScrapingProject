import os
from google.cloud import storage

#######
#LOADING CSV FILE TO GOOGLE CLOUD STORAGE
######


#setting up credentials using JSON file located directly on computer
client_storage = storage.Client.from_service_account_json(json_credentials_path='/Users/selledge/Documents/keh_data_credentials.json')

#getting the keh_sandbox bucket
sandbox_bucket = client_storage.get_bucket('keh_sandbox')

#name of the object to be stored into the keh_sandbox under folder webscrapping_project
object_name_in_bucket = sandbox_bucket.blob('webscrapping_project/webscrapping_project_book_data.csv')

#the path to the file object to be uploaded to the system
object_name_in_bucket.upload_from_filename('/Users/selledge/Documents/pythonproject/ScrapingProject-main/ToScrapeProject3/project3_classes_file_complete.csv')