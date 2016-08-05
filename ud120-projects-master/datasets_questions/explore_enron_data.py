#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle
import numpy as np

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

# Number of data points (people) in the dataset
print len(enron_data.keys())

# For each data point(person), how many features are available
print enron_data[enron_data.keys()[0]].keys()
print
print len(enron_data[enron_data.keys()[0]].keys())

# How many poi are present in the dataset
poi = []
for i in enron_data.keys():
	if enron_data[i]["poi"] == 1:
		poi.append(i)
		
print poi
print
print len(poi)
print

# Total value of the stock belonging to James Prentice?
james_prentice_stock_value = dict()

for i in enron_data.keys():
	name = i.lower()
	if "prentice" in name and "james" in name:
		james_prentice_stock_value[i] = enron_data[i]["total_stock_value"]
		
print james_prentice_stock_value
print

# How many email messages do we have from Wesley Colwell to persons of interest?
for i in enron_data.keys():
	name = i.lower()
	if "colwell" in name and "wesley" in name:
		print enron_data[i]["from_this_person_to_poi"]
		break
		
print

# Whats the value of stock options exercised by Jeffrey K Skilling?
jeffrey_k_skilling_stock_options = dict()

for i in enron_data.keys():
	name = i.lower()
	if "jeffrey" in name and "skilling" in name:
		jeffrey_k_skilling_stock_options[i] = enron_data[i]["exercised_stock_options"]
		
print jeffrey_k_skilling_stock_options
print

# Whats the total payments of kenneth lay?
kenneth_lay_total_payments = dict()

for i in enron_data.keys():
	name = i.lower()
	if "kenneth" in name and "lay" in name:
		kenneth_lay_total_payments[i] = enron_data[i]["total_payments"]
		
print kenneth_lay_total_payments
print

# Number of people with a quantified salary
quantified_salary = []

for i in enron_data.keys():

	if not np.isnan(float(enron_data[i]["salary"])):
		quantified_salary.append(enron_data[i]["salary"])
		
		
print len(quantified_salary)
print

# Number of people with an email address
email_address = []

for i in enron_data.keys():
	
	if not enron_data[i]["email_address"] == "NaN":
		email_address.append(enron_data[i]["email_address"])
		
		
print len(email_address)
print

# How many people in the E+F dataset (as it currently exists) have 'NaN' for their total payments? What percentage of people in the dataset as a whole is this?
NaN_payments = []

for i in enron_data.keys():
	if np.isnan(float(enron_data[i]["total_payments"])):
		NaN_payments.append(i)
		
print len(NaN_payments)
print len(NaN_payments)/(0.0 + len(enron_data.keys()))*100
print
		
# How many poi in the E+F dataset (as it currently exists) have 'NaN' for their total payments? What percentage of poi in the dataset as a whole is this?
poi_NaN_payments = []

for i in poi:
	if np.isnan(float(enron_data[i]["total_payments"])):
		poi_NaN_payments.append(i)
		
print len(poi_NaN_payments)
print len(poi_NaN_payments)/(0.0 + len(poi)) * 100.0