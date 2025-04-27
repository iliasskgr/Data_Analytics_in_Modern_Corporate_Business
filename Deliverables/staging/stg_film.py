#!/usr/bin/env python
# coding: utf-8

# # Setup - Install Libraries

# In[15]:


# Run the following commands once, in order to install libraries - DO NOT Uncomment this line.

# Uncomment below lines

# !pip3 install --upgrade pip
# !pip install google-cloud-bigquery
# !pip install pandas-gbq -U
# !pip install db-dtypes
# !pip install packaging --upgrade


# In[16]:


get_ipython().system('pip install --upgrade pip')


# In[17]:


get_ipython().system('pip install google-cloud-bigquery')


# In[18]:


get_ipython().system('pip install pandas-gbq -U')


# In[19]:


get_ipython().system('pip install db-dtypes')


# In[20]:


get_ipython().system('pip install packaging --upgrade')


# In[21]:


pip install --upgrade pip


# # Import libraries

# In[22]:


# Import libraries
from google.cloud import bigquery
import pandas as pd
from pandas_gbq import to_gbq
import os

print('Libraries imported successfully')


# In[23]:


# Set the environment variable for Google Cloud credentials
# Place the path in which the .json file is located.

# Example (if .json is located in the same directory with the notebook)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "at-arch-416714-6f9900ec7.json"

# -- YOUR CODE GOES BELOW THIS LINE
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/antonesangelakes/scripts/mineral-voyage-442817-m2-1de3ad04cf72.json" # Edit path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/Myrmidons/Desktop/Data Analytics in Modern Corporate Business/6. Capstone Project/Scripts/Json_credentials/spiritual-hour-458020-c6-1514d7eb6010.json" # Edit path

# -- YOUR CODE GOES ABOVE THIS LINE


# In[24]:


# Set your Google Cloud project ID and BigQuery dataset details

# -- YOUR CODE GOES BELOW THIS

project_id = 'spiritual-hour-458020-c6' # Edit with your project id
dataset_id = 'staging_db' # Modify the necessary schema name: staging_db, reporting_db etc.
table_id = 'stg_film' # Modify the necessary table name: stg_customer, stg_city etc.

# -- YOUR CODE GOES ABOVE THIS LINE


# # SQL Query

# In[25]:


# Create a BigQuery client
client = bigquery.Client(project=project_id)

# -- YOUR CODE GOES BELOW THIS LINE

# Define your SQL query here
query = """
with base as (
  select *
  from `spiritual-hour-458020-c6.pagila_prodpublic.film` --Your table path
  )

  , final as (
    select
       title as film_title
      ,description as film_description
      ,language_id as film_language_id
      ,original_language_id as film_original_language_id
      ,rental_duration as film_rental_duration
      ,rental_rate as film_rental_rate
      ,length as film_length
      ,replacement_cost as film_replacement_cost
      ,rating as film_rating
      ,last_update as film_last_update
      ,special_features as film_special_features
      ,fulltext as film_fulltext

   FROM base
  )

  select * from final
"""

# -- YOUR CODE GOES ABOVE THIS LINE

# Execute the query and store the result in a dataframe
df = client.query(query).to_dataframe()

# Explore some records
df.head()


# # Write to BigQuery

# In[ ]:


# Define the full table ID
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

# -- YOUR CODE GOES BELOW THIS LINE
# Define table schema based on the project description

schema = [
    bigquery.SchemaField('film_title', 'STRING'),
    bigquery.SchemaField('film_description', 'STRING'),
    bigquery.SchemaField('film_language_id', 'INTEGER'),
    bigquery.SchemaField('film_original_language_id', 'INTEGER'),
    bigquery.SchemaField('film_rental_duration', 'INTEGER'),
    bigquery.SchemaField('film_rental_rate', 'NUMERIC'),
    bigquery.SchemaField('film_length', 'INTEGER'),
    bigquery.SchemaField('film_replacement_cost', 'NUMERIC'),
    bigquery.SchemaField('film_rating', 'STRING'),
    bigquery.SchemaField('film_last_update', 'DATETIME'),
    bigquery.SchemaField('film_special_features', 'STRING'),
    bigquery.SchemaField('film_fulltext', 'STRING'),
]


# -- YOUR CODE GOES ABOVE THIS LINE


# In[27]:


# Create a BigQuery client
client = bigquery.Client(project=project_id)

# Check if the table exists
def table_exists(client, full_table_id):
    try:
        client.get_table(full_table_id)
        return True
    except Exception:
        return False

# Write the dataframe to the table (overwrite if it exists, create if it doesn't)
if table_exists(client, full_table_id):
    # If the table exists, overwrite it
    destination_table = f"{dataset_id}.{table_id}"
    # Write the dataframe to the table (overwrite if it exists)
    to_gbq(df, destination_table, project_id=project_id, if_exists='replace')
    print(f"Table {full_table_id} exists. Overwritten.")
else:
    # If the table does not exist, create it
    job_config = bigquery.LoadJobConfig(schema=schema)
    job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
    job.result()  # Wait for the job to complete
    print(f"Table {full_table_id} did not exist. Created and data loaded.")


# In[28]:


# Below line converts your i.pynb file to .py python executable file. Modify the input and output names based
# on the table you are processing.
# Example:
# ! jupyter nbconvert stg_customer.ipynb --to python

# -- YOUR CODE GOES BELOW THIS LINE

get_ipython().system('python -m jupyter nbconvert stg_film.ipynb --to python')

# -- YOUR CODE GOES ABOVE THIS LINE


# In[29]:


get_ipython().system('python -m pip install nbconvert')


# In[30]:


get_ipython().system('python -m pip install nbconvert -U')


# In[ ]:




