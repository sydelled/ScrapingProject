import os
from google.cloud import bigquery
import time

#########
#LOADING CSV FILE TO GOOGLE BIGQUERY
#########

#file to the credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/selledge/Documents/keh_data_credentials.json'
client = bigquery.Client()

#set the table id (projectname.dataset.name.table.name)
table_id = 'keh-data.crawl_data.Web_Scrapping_Project'

#file path to the csv file
file_path = '/Users/selledge/Documents/pythonproject/ScrapingProject-main/ToScrapeProject3/project3_classes_file_complete.csv'

#this executes the job
job_config = bigquery.LoadJobConfig(
    source_format = bigquery.SourceFormat.CSV,
    #this skips the header if it is in the file
    skip_leading_rows = 1,
    autodetect=True
)

with open(file_path, 'rb') as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

#while loop that checks whether the job is completed every 2 seconds and once it is complete it will print the result
while job.state != 'DONE':
    time.sleep(2)
    job.reload()
    print(job.state)

print(job.result())

#this code block makes sure that once the table is created
# it uses the bigquery api to retrieve the table to make sure it uploaded successfully

table = client.get_table(table_id) #make an api request
print(
    "Loaded {} rows and {} columns to {}".format(table.num_rows, len(table.schema), table_id)
)
