# -*- coding: utf-8 -*-
"""
Created on Thu May  7 18:05:58 2020

@author: meule
"""
import pickle
from os import path
import os
import pandas as pd

os.chdir(r"DeinPFAD")

file_name="07-05-2020_02-47-44_responses.pkl"
file = open(file_name, 'rb')
response= pickle.load(file)

#Ist eigene Klasse
type(response)
#Help für response objekt 
# https://amadeus4dev.github.io/amadeus-python/index.html?highlight=amadeus%20shopping#response

#Die Antwort der API sollte 200 sein
response.status_code

#Alle inputs des Request siehe auch 
# https://amadeus4dev.github.io/amadeus-python/index.html?highlight=amadeus%20shopping#request
dir(response.request)
response.request.host
response.request.params
response.request.params["searchCriteria"]
# daher später nur 5 Offers pro Response 
#etc
#results
response.result
type(response.result)
#drei Elemente
response.result.keys()
response.result["data"]
type(response.result["data"])
#Eventuell müsse man das später noch parsen und reducen, wobei es mich der Inhalt nicht so interessiert 
response.result["dictionaries"]
#Das dasselbe wie das andere Data objekt? 
response.data==response.result["data"]
#data
response.data
type(response.data)
#Da sind 5 Elemente drin, weil ich max offer 5 hatte
len(response.data)
response.data[0].keys()
response.data[0]["type"]
response.data[0]["itineraries"]

#Lets start with the scalar values in each dict 
scalar_export=[]
for j in (response.data[0]):
     # print(type(response.data[0][j]))
     # print(len(response.data[0][j]))
     if (isinstance(response.data[0][j],(str,bool, int))):
         scalar_export.append(j)

dict_scalar = { your_key: response.data[0][your_key] for your_key in scalar_export }
pd_scalar=pd.DataFrame([dict_scalar])

#Continue with the dict of the reponse.data
dict_export=[]
for j in (response.data[0]):
     # print(type(response.data[0][j]))
     # print(len(response.data[0][j]))
     if (isinstance(response.data[0][j],(dict))):
         dict_export.append(j)

#Wie mach ich das jetzt clever, dass ich die beiden unterschiedliche fees types flatte? oder halt als long format bekomme
response.data[0]["price"]
pd.DataFrame.from_dict(response.data[0]["price"])
#z.B. hier die spalte fees splitte?

response.data[0]["pricingOptions"]
pd.DataFrame.from_dict(response.data[0]["pricingOptions"])


#Next we look at the lists
list_export=[]
for j in (response.data[0]):
     # print(type(response.data[0][j]))
     # print(len(response.data[0][j]))
     if (isinstance(response.data[0][j],(list))):
         list_export.append(j)

response.data[0]["itineraries"]
pd.DataFrame.from_dict(response.data[0]["itineraries"])
#Hier dasselbe Problem Index 0 ist der Hinflug und Index 1 der Rückflug 

response.data[0]["validatingAirlineCodes"]
#können warhscheinlich bei mehr offers mehr sein 


response.data[0]["travelerPricings"]
pd.DataFrame.from_dict(response.data[0]["travelerPricings"])
