'''
input: string
output: database
'''
import csv
import jsonlines
import pandas as pd
import numpy as np
import json
import os
import re
import mysql
import mysql.connector as msql
import demoji

MYSQL_HOSTNAME = "MYSQL_HOSTNAME"
MYSQL_USERNAME = "MYSQL_USERNAME"
MYSQL_PASSWORD = "MYSQL_PASSWORD"

def remove_emoji(string):
    # Remove emoji using demoji library
    cleaned_string = demoji.replace_with_desc(string)

    # Remove any remaining Unicode characters outside the Basic Multilingual Plane (BMP)
    cleaned_string = re.sub(r'[\U00010000-\U0010FFFF]', '', cleaned_string)

    return cleaned_string

def flights_db_loader():
    file_path = "/<YOUR_OWN_PATH>/ToolQA/data/external_corpus/flights/Combined_Flights_2022.csv"
    data = pd.read_csv(file_path)
    data = data.fillna("---")
    
    conn = msql.connect(host=MYSQL_HOSTNAME, user=MYSQL_USERNAME, password=MYSQL_PASSWORD)#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE flights")
        print("Database is created")
    
    conn = msql.connect(database='flights', host=MYSQL_HOSTNAME, user=MYSQL_USERNAME, password=MYSQL_PASSWORD)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS flights_data;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        org_columns = ['FlightDate', 'Airline', 'Origin', 'Dest', 'Cancelled', 'Diverted',
       'CRSDepTime', 'DepTime', 'DepDelayMinutes', 'DepDelay', 'ArrTime',
       'ArrDelayMinutes', 'AirTime', 'CRSElapsedTime', 'ActualElapsedTime',
       'Distance', 'Year', 'Quarter', 'Month', 'DayofMonth', 'DayOfWeek',
       'Marketing_Airline_Network', 'Operated_or_Branded_Code_Share_Partners',
       'DOT_ID_Marketing_Airline', 'IATA_Code_Marketing_Airline',
       'Flight_Number_Marketing_Airline', 'Operating_Airline',
       'DOT_ID_Operating_Airline', 'IATA_Code_Operating_Airline',
       'Tail_Number', 'Flight_Number_Operating_Airline', 'OriginAirportID',
       'OriginAirportSeqID', 'OriginCityMarketID', 'OriginCityName',
       'OriginState', 'OriginStateFips', 'OriginStateName', 'OriginWac',
       'DestAirportID', 'DestAirportSeqID', 'DestCityMarketID', 'DestCityName',
       'DestState', 'DestStateFips', 'DestStateName', 'DestWac', 'DepDel15',
       'DepartureDelayGroups', 'DepTimeBlk', 'TaxiOut', 'WheelsOff',
       'WheelsOn', 'TaxiIn', 'CRSArrTime', 'ArrDelay', 'ArrDel15',
       'ArrivalDelayGroups', 'ArrTimeBlk', 'DistanceGroup',
       'DivAirportLandings']
        columns = [org_columns[i]+" varchar(255)" for i in range(len(org_columns))]
        columns = ','.join(columns)
        sql_cmd = "CREATE TABLE flights_data({})".format(columns)
        # print(sql_cmd)
        cursor.execute(sql_cmd)
        print("Table is created....")
        #loop through the data frame
        for i,row in data.iterrows():
            #here %S means string values 
            row_data = [row[i] for i in org_columns]
            sql = "INSERT INTO flights.flights_data VALUES ({})".format(','.join(['%s']*len(row_data)))
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()

def coffee_db_loader():
    file_path = "/<YOUR_OWN_PATH>/ToolQA/data/external_corpus/coffee/coffee_price.csv"
    data = pd.read_csv(file_path)
    column_names = data.columns.to_list()
    data = data.fillna("---")
    
    conn = msql.connect(host=MYSQL_HOSTNAME, user=MYSQL_USERNAME,  
                        password=MYSQL_PASSWORD)#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE coffee")
        print("Database is created")
    
    conn = msql.connect(database='coffee', host=MYSQL_HOSTNAME, user=MYSQL_USERNAME, password=MYSQL_PASSWORD)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS coffee_data;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        org_columns = column_names
        columns = [org_columns[i]+" varchar(255)" for i in range(len(org_columns))]
        columns = ','.join(columns)
        sql_cmd = "CREATE TABLE coffee_data({})".format(columns)
        # print(sql_cmd)
        cursor.execute(sql_cmd)
        print("Table is created....")
        #loop through the data frame
        for i,row in data.iterrows():
            #here %S means string values 
            row_data = [row[i] for i in org_columns]
            sql = "INSERT INTO coffee.coffee_data VALUES ({})".format(','.join(['%s']*len(row_data)))
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()

def airbnb_db_loader():
    file_path = "/<YOUR_OWN_PATH>/ToolQA/data/external_corpus/airbnb/Airbnb_Open_Data.csv"
    data = pd.read_csv(file_path)
    column_names = data.columns.to_list()
    data = data.fillna("---")
    
    conn = msql.connect(host=MYSQL_HOSTNAME, user=MYSQL_USERNAME,  
                        password=MYSQL_PASSWORD)#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE airbnb")
        print("Database is created")
    
    conn = msql.connect(database='airbnb', host=MYSQL_HOSTNAME, user=MYSQL_USERNAME, password=MYSQL_PASSWORD)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS airbnb_data;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        org_columns = column_names
        org_columns = [i.replace(" ","_").replace("lat", "latitude").replace("long", "longitude") for i in org_columns]
        columns = [org_columns[i]+" varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL" for i in range(len(org_columns))]
        columns = ', '.join(columns)
        sql_cmd = "CREATE TABLE airbnb_data({})".format(columns)
        print(sql_cmd)
        cursor.execute(sql_cmd)
        print("Table is created....")
        #loop through the data frame
        for i,row in data.iterrows():
            #here %S means string values 
            pattern = r"\\x[0-9A-Fa-f]{2}"
            # clean_string = re.sub(pattern, '', string)
            row_data = [remove_emoji(str(row[column_names[j]]))[:250] for j in range(len(org_columns))]
            # print(row_data)
            sql = "INSERT INTO airbnb.airbnb_data VALUES ({})".format(','.join(['%s']*len(row_data)))
            # print(sql)
            cursor.execute(sql, tuple(row_data))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()

def yelp_db_loader():
    data_file = open("/<YOUR_OWN_PATH>/ToolQA/data/external_corpus/yelp/yelp_academic_dataset_business.json")
    data = []
    for line in data_file:
        data.append(json.loads(line))
    data = pd.DataFrame(data)
    column_names = data.columns.to_list()
    data = data.fillna("---")
    
    conn = msql.connect(host=MYSQL_HOSTNAME, user=MYSQL_USERNAME,  
                        password=MYSQL_PASSWORD)#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE yelp")
        print("Database is created")
    
    conn = msql.connect(database='yelp', host=MYSQL_HOSTNAME, user=MYSQL_USERNAME, password=MYSQL_PASSWORD)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS yelp_data;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        org_columns = column_names
        columns = [org_columns[i]+" varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL" for i in range(len(org_columns))]
        columns = ','.join(columns)
        sql_cmd = "CREATE TABLE yelp_data({})".format(columns)
        # print(sql_cmd)
        cursor.execute(sql_cmd)
        print("Table is created....")
        #loop through the data frame
        for i,row in data.iterrows():
            #here %S means string values 
            row_data = [str(row[i])[:250] for i in org_columns]
            # print(row_data)
            sql = "INSERT INTO yelp.yelp_data VALUES ({})".format(','.join(['%s']*len(row_data)))
            cursor.execute(sql, tuple(row_data))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()

def main():
    flights_db_loader()
    coffee_db_loader()
    airbnb_db_loader()
    yelp_db_loader()

if __name__ == "__main__":
    main()