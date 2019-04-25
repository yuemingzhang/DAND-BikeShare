# import all packages and set plots to be embedded inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from os import listdir 

%matplotlib inline


# load in the dataset into a pandas dataframe
folder_name_of_csvs = 'Data'
list_csvs = []
for file_name in listdir(folder_name_of_csvs):
    list_csvs.append(pd.read_csv(folder_name_of_csvs+'/'+file_name))
df = pd.concat(list_csvs, ignore_index=True)

# high-level overview of data shape and composition
print(df.shape)
print(df.dtypes)
df.head(5)

# create new field 'duration_min' to convert bike share duration seconds to minutes
df['duration_min'] = round(df['duration_sec'] / 60,0).astype(int)

# create new fields 'start_year', 'start_month', 'start_day', 'start_hour', 'start_dayofweek' to breakdown 'start_time' information
df['start_year'] = pd.to_datetime(df.start_time, errors='coerce').dt.year
df['start_month'] = pd.to_datetime(df.start_time, errors='coerce').dt.month
df['start_day'] = pd.to_datetime(df.start_time, errors='coerce').dt.day
df['start_hour'] = pd.to_datetime(df.start_time, errors='coerce').dt.hour
df['start_dayofweek'] = pd.to_datetime(df.start_time, errors='coerce').dt.day_name()

# order day of week from Monday to Sunday
df.start_dayofweek = pd.Categorical(df.start_dayofweek, ordered=True, 
                                    categories=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
# confirm this field's data type
df['start_dayofweek'].dtype.name

# calculate member's age based on their birth year
df['member_age'] = 2019 - df['member_birth_year']

# explore member age structure
df['member_age'].describe(percentiles = [.1, .2, .3, .4, .5, .6, .7, .8, .9])

# create a new field to reflect member age range
df['member_age_bins'] = df['member_age'].apply(lambda x: '10 - 20' if 10<x<=20
                                                  else '20 - 30' if 20<x<=30
                                                  else '30 - 40' if 30<x<=40
                                                  else '40 - 50' if 40<x<=50
                                                  else '50 - 60' if 50<x<=60
                                                  else '> 60')
                                                  
# After generating new field, drop abundant fields
df.drop(['duration_sec', 'start_time', 'end_time', 'start_station_name', 'start_station_latitude', 'start_station_longitude', 
         'end_station_name', 'end_station_latitude', 'end_station_longitude', 'member_birth_year'], axis = 1, inplace = True)

# high-level overview of data shape and composition
print(df.shape)
print(df.dtypes)
df.head(5)

# group data by start_hour
trip_by_hour_df = df.groupby('start_hour').agg({'bike_id':'count'}).reset_index()
trip_by_hour_df['bike_id'] = (trip_by_hour_df['bike_id']/trip_by_hour_df['bike_id'].sum())*100
trip_by_hour_df.head()

# plot ride count percentage for each hour of the day
plt.figure(figsize=(15,9))
sb.pointplot(x='start_hour', y='bike_id', scale=.7, color='blue', data=trip_by_hour_df)
plt.title('Percentage of all bike rides by hour of the day', fontsize=22, y=1.015)
plt.xlabel('Hour [day]', labelpad=16)
plt.ylabel('Percentage(%) [rides]', labelpad=16);

# group data by day of week
trip_by_weekday_df = df.groupby('start_dayofweek').agg({'bike_id':'count'})
trip_by_weekday_df['bike_id'] = (trip_by_weekday_df['bike_id']/trip_by_weekday_df['bike_id'].sum())*100
trip_by_weekday_df

# plot ride count percentage for each day of week
weekday_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
colors = ['lightskyblue','lightskyblue','lightskyblue','lightskyblue','lightskyblue','lightsteelblue','lightsteelblue']
trip_by_weekday_df.reindex(weekday_index)['bike_id'].plot(kind='bar', color=colors, figsize=(12,8), legend=False)
plt.title('Percentage of all bike rides per weekday', fontsize=22, y=1.015)
plt.xlabel('Day of the Week', labelpad=16)
plt.ylabel('percentage(%) [rides]', labelpad=16)
plt.xticks(rotation=360);

# get only 2018 data
df_2018 = df[df['start_year'] == 2018]

# plot ride counts for each month of the year
plt.figure(figsize=(14,8))
sb.countplot(x='start_month', palette="Blues", data=df_2018.sort_values(by='start_month'))
plt.title('The monthly trend of bike rides', fontsize=22, y=1.015)
plt.xlabel('Month of the Year', labelpad=16)
plt.ylabel('Count [rides]', labelpad=16);

# group data by member age groups
trip_by_age_df = df.groupby('member_age_bins').agg({'bike_id':'count'})
trip_by_age_df['bike_id'] = (trip_by_age_df['bike_id']/trip_by_age_df['bike_id'].sum())*100
trip_by_age_df

# plot ride count percentage for each age group
colors = ['Thistle','Plum','Violet','Orchid','MediumOrchid','DarkOrchid']
trip_by_age_df['bike_id'].plot(kind='bar', color = colors, figsize=(12,8))
plt.title('Percentage of all bike rides per age group', fontsize=22, y=1.015)
plt.xlabel('member age group', labelpad=16)
plt.ylabel('pecentage(%) [rides]', labelpad=16)
plt.xticks(rotation=360);

# group data by member gender
trip_by_gender_df = df.groupby('member_gender').agg({'bike_id':'count'})
trip_by_gender_df['bike_id'] = (trip_by_gender_df['bike_id']/trip_by_gender_df['bike_id'].sum())*100
trip_by_gender_df

# plot ride count percentage for each gender
colors = ['pink', 'steelblue', 'lightgrey']
trip_by_gender_df['bike_id'].plot(kind='barh', color=colors, figsize=(12,6))
plt.title('Percentage of all bike rides per gender', fontsize=22, y=1.015)
plt.ylabel('member gender', labelpad=16)
plt.xlabel('pecentage(%) [rides]', labelpad=16)
plt.xticks(rotation=360)
plt.xlim(0,100);

# group data by user type
rides_per_user_type = df.groupby('user_type').size().reset_index(name='perc')
rides_per_user_type['perc'] = (rides_per_user_type['perc']/rides_per_user_type['perc'].sum())*100
rides_per_user_type

# calculate average trip duration by user type
duration_min_per_user_type = df.groupby('user_type')['duration_min'].mean()
duration_min_per_user_type

# plot average trip duration for each user type
new_color=['deepskyblue', 'navy']
duration_min_per_user_type.plot(kind='barh', color=new_color, figsize=(13,7))
plt.title('Average trip duration per user type', fontsize=20, y=1.015)
plt.ylabel('user type', labelpad=16)
plt.xlabel('minutes [trip duration]', labelpad=16)

for i,j in enumerate(duration_min_per_user_type):
    plt.text(.7,i,str(round(j,2))+' minutes', weight='bold', ha='left', fontsize=16, color="white");
    
