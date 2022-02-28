#Import dependencies
import pandas as pd
import requests

#API pull for latest salary info from www.levels.fyi
salaryData = requests.get('https://www.levels.fyi/js/salaryData.json').json()
salary_df = pd.DataFrame(salaryData)

#dropping columns that are not relevant to project
salary_df = salary_df.drop(['cityid', 'dmaid','rowNumber','otherdetails','tag', 'basesalary', 'stockgrantvalue', 'bonus', 'gender'], axis=1)

#converting to float to allow for summary stats
salary_df["totalyearlycompensation"] = pd.to_numeric(salary_df["totalyearlycompensation"])
salary_df["yearsofexperience"] = pd.to_numeric(salary_df["yearsofexperience"])
salary_df["yearsatcompany"] = pd.to_numeric(salary_df["yearsatcompany"])

#coverting timestamp from object to datetime
salary_df['timestamp'] =  pd.to_datetime(salary_df['timestamp'], infer_datetime_format=True)

# Create separate cols for city, state and country
def split_location(location):
    items = location.split(', ')
    city = items[0]
    state = items[1]
    
    if len(items)==2:
        country = 'US'
    elif len(items)==3:
        country = items[2].strip()
    elif len(items)==4:
        country = ', '.join([i.strip() for i in items[2:]])
    else:
        country = None
        print(location)
        
    return [city, state, country]

salary_df['loc_items'] = salary_df.location.apply(lambda x: split_location(x))
salary_df['city'] = salary_df.loc_items.apply(lambda x: x[0])
salary_df['state'] = salary_df.loc_items.apply(lambda x: x[1])
salary_df['country'] = salary_df.loc_items.apply(lambda x: x[2])

# dropping location column  
salary_df = salary_df.drop(['location','loc_items'], axis=1)

#isolating US data for further exploration
us_df = salary_df[salary_df.country=='US'].copy()

#isolating us data to data scientist titles
us_df = us_df[us_df.title=='Data Scientist'].copy()


#merging dataframes into on collection
#cleaned_data = pd.concat([apple_df, amazon_df, fb_df, google_df, micro_df ])

#import dependency
#import pymongo
#from pymongo import MongoClient
#establish connection to pymongo
#conn ="mongodb://127.0.0.1:27017/"
#client = MongoClient(conn)
#db = client.ds_salaries
#collection = db.top5
#cleaned_dict = cleaned_data.to_dict("records")
#collection.insert_many(cleaned_dict)