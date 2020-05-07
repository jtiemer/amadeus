# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:32:12 2020

@author: meule
"""
import json
from amadeus import Client, ResponseError
from amadeus import Location
import pandas as pd
import numpy as np
import os
from os import path
import time
import itertools
import pickle
from datetime import datetime

#set wd
os.chdir(r"C:\Users\meule\Desktop\DB FV Analyse\Code\20 Webscrapping\Amadeus")
exec(open('Python_Referenzen.py').read())

#Authorize client 
amadeus = Client(
    client_id=client_id,
    client_secret=client_secret
)
#load airports
db_cities = pd.read_csv(r_data_file_iata) 
airports=pd.unique(db_cities.get("IATA_codes"))
#Create list of permutated ODs of Airports
ab = list(itertools.product(airports,airports))
OD_flights=pd.DataFrame(ab, columns=("Origin","Destination"))
OD_flights=OD_flights[OD_flights["Origin"]!=OD_flights["Destination"]]
OD_flights=OD_flights[0:4]
#Set one date as example
OD_flights["DepartureDate"]="2020-07-01"
OD_flights["ReturnDate"]="2020-07-14"
#create json query , max 10 offers
json_string_place = '{ "currencyCode": "EUR", "originDestinations": [ { "id": "1", "originLocationCode": "%s", "destinationLocationCode": "%s", "departureDateTimeRange": { "date": "%s", "time": "00:00:00" } }, { "id": "2", "originLocationCode": "%s", "destinationLocationCode": "%s", "departureDateTimeRange": { "date": "%s", "time": "00:00:00" } } ], "travelers": [ { "id": "1", "travelerType": "ADULT" } ], "sources": [ "GDS" ]}'


json_string_place = '{ "currencyCode": "EUR", "originDestinations": [ { "id": "1", "originLocationCode": "%s", "destinationLocationCode": "%s", "departureDateTimeRange": { "date": "%s", "time": "00:00:00" } }, { "id": "2", "originLocationCode": "%s", "destinationLocationCode": "%s", "departureDateTimeRange": { "date": "%s", "time": "00:00:00" } } ], "travelers": [ { "id": "1", "travelerType": "ADULT" } ], "sources": [ "GDS" ], "searchCriteria": {"maxFlightOffers": 5 }}'


#Loop to create the Json String
OD_flights["Json_string"]=""
for index, row in OD_flights.iterrows():
    name_temp=(row["Origin"],row["Destination"],row["DepartureDate"],row["Destination"],row["Origin"],row["ReturnDate"])
    row["Json_string"]=json_string_place%name_temp
 
#Test json string..
# body = json.loads(OD_flights.loc[1]["Json_string"])
# amadeus.shopping.flight_offers_search.post(body)

# responses=[]
for index, row in OD_flights.iterrows():
    body = json.loads(row["Json_string"])
    timestamp = datetime.now().strftime("%d-%m-%Y_%I-%M-%S")
    file_name = "Responses/" + timestamp +'_responses.pkl'
    try:

        response = amadeus.shopping.flight_offers_search.post(body)
        #print(response.data[0])
        with open(file_name, 'wb') as f:
             pickle.dump(response, f)

    except ResponseError as error:

        raise error
    
    
    # responses.append(response)
       





#wie speichere ich das jetzt? 