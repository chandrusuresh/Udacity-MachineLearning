import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def filter_data(data, condition):
    """
    Remove elements that do not match the condition provided.
    Takes a data list as input and returns a filtered list.
    Conditions should be a list of strings of the following format:
      '<field> <op> <value>'
    where the following operations are valid: >, <, >=, <=, ==, !=
    
    Example: ["Sex == 'male'", 'Age < 18']
    """

    field, op, value = condition.split(" ")
    
    # convert value into number or strip excess quotes if string
    try:
        value = float(value)
    except:
        value = value.strip("\'\"")
    
    # get booleans for filtering
    if op == ">":
        matches = data[field] > value
    elif op == "<":
        matches = data[field] < value
    elif op == ">=":
        matches = data[field] >= value
    elif op == "<=":
        matches = data[field] <= value
    elif op == "==":
        matches = data[field] == value
    elif op == "!=":
        matches = data[field] != value
    else: # catch invalid operation codes
        raise Exception("Invalid comparison operator. Only >, <, >=, <=, ==, != allowed.")
    
    # filter data and outcomes
    data = data[matches].reset_index(drop = True)
    return data

def survival_stats(data, outcomes, key, filters = []):
    """
    Print out selected statistics regarding survival, given a feature of
    interest and any number of filters (including no filters)
    """
    
    # Check that the key exists
    if key not in data.columns.values :
        print "'{}' is not a feature of the Titanic data. Did you spell something wrong?".format(key)
        return False

    # Return the function before visualizing if 'Cabin' or 'Ticket'
    # is selected: too many unique categories to display
    if(key == 'Cabin' or key == 'PassengerId' or key == 'Ticket'):
        print "'{}' has too many unique categories to display! Try a different feature.".format(key)
        return False

    # Merge data and outcomes into single dataframe
    all_data = pd.concat([data, outcomes], axis = 1)
    
    # Apply filters to data
    for condition in filters:
        all_data = filter_data(all_data, condition)

    # Create outcomes DataFrame
    all_data = all_data[[key, 'Survived']]
    
    # Create plotting figure
    plt.figure(figsize=(8,6))

    # 'Numerical' features
    if(key == 'Age' or key == 'Fare'):
        
        # Remove NaN values from Age data
        all_data = all_data[~np.isnan(all_data[key])]
        
        # Divide the range of data into bins and count survival rates
        min_value = all_data[key].min()
        max_value = all_data[key].max()
        value_range = max_value - min_value

        # 'Fares' has larger range of values than 'Age' so create more bins
        if(key == 'Fare'):
            bins = np.arange(0, all_data['Fare'].max() + 20, 20)
        if(key == 'Age'):
            bins = np.arange(0, all_data['Age'].max() + 10, 10)
        
        # Overlay each bin's survival rates
        nonsurv_vals = all_data[all_data['Survived'] == 0][key].reset_index(drop = True)
        surv_vals = all_data[all_data['Survived'] == 1][key].reset_index(drop = True)
        plt.hist(nonsurv_vals, bins = bins, alpha = 0.6,
                 color = 'red', label = 'Did not survive')
        plt.hist(surv_vals, bins = bins, alpha = 0.6,
                 color = 'green', label = 'Survived')
    
        # Add legend to plot
        plt.xlim(0, bins.max())
        plt.legend(framealpha = 0.8)
    
    # 'Categorical' features
    else:
       
        # Set the various categories
        if(key == 'Pclass'):
            values = np.arange(1,4)
        if(key == 'Parch' or key == 'SibSp'):
            values = np.arange(0,np.max(data[key]) + 1)
        if(key == 'Embarked'):
            values = ['C', 'Q', 'S']
        if(key == 'Sex'):
            values = ['male', 'female']

        # Create DataFrame containing categories and count of each
        frame = pd.DataFrame(index = np.arange(len(values)), columns=(key,'Survived','NSurvived'))
        for i, value in enumerate(values):
            frame.loc[i] = [value, \
                   len(all_data[(all_data['Survived'] == 1) & (all_data[key] == value)]), \
                   len(all_data[(all_data['Survived'] == 0) & (all_data[key] == value)])]

        # Set the width of each bar
        bar_width = 0.4

        # Display each category's survival rates
        for i in np.arange(len(frame)):
            nonsurv_bar = plt.bar(i-bar_width, frame.loc[i]['NSurvived'], width = bar_width, color = 'r')
            surv_bar = plt.bar(i, frame.loc[i]['Survived'], width = bar_width, color = 'g')

            plt.xticks(np.arange(len(frame)), values)
            plt.legend((nonsurv_bar[0], surv_bar[0]),('Did not survive', 'Survived'), framealpha = 0.8)

    # Common attributes for plot formatting
    plt.xlabel(key)
    plt.ylabel('Number of Passengers')
    plt.title('Passenger Survival Statistics With \'%s\' Feature'%(key))
    plt.show()

    # Report number of passengers with missing values
    if sum(pd.isnull(all_data[key])):
        nan_outcomes = all_data[pd.isnull(all_data[key])]['Survived']
        print "Passengers with missing '{}' values: {} ({} survived, {} did not survive)".format( \
              key, len(nan_outcomes), sum(nan_outcomes == 1), sum(nan_outcomes == 0))
		  
def find_titles(names,survived):
	titles = []
	madeIt = []
	total = []
	count = -1
	for i in range(len(names)):
		count = count + 1
		x = names[i].split(',')
		tmp = x[1].split('.')
		
		if not tmp[0] in titles:
			titles.insert(len(titles),tmp[0])
			total.insert(len(total),1)
			if survived[count] == 1:
				madeIt.insert(len(madeIt),1)
			else:
				madeIt.insert(len(madeIt),0)
		else:
			ind = titles.index(tmp[0])
			total[ind] = total[ind] + 1
			if survived[count] == 1:
				madeIt[ind] = madeIt[ind] + 1
				
	return titles, madeIt, total

def filter_lastName(names, survived):
	lastName = []
	madeIt = []
	total = []
	count = -1
	for i in range(len(names)):
		count = count + 1
		x = names[i].split(',')
		
		if not x[0] in lastName:
			lastName.insert(len(lastName),x[0])
			total.insert(len(total),1)
			if survived[count] == 1:
				madeIt.insert(len(madeIt),1)
			else:
				madeIt.insert(len(madeIt),0)
		else:
			ind = lastName.index(x[0])
			total[ind] = total[ind] + 1
			if survived[count] == 1:
				madeIt[ind] = madeIt[ind] + 1
				
	return lastName, madeIt, total
	
def filter_fare(fares, survived, min_val, max_val):
	min_fare = min_val
	max_fare = max_val
	bin_size = 0.2
	madeIt = [0 for i in range(int(1/bin_size))]
	total = [0 for i in range(int(1/bin_size))]
	count = -1

	for i in range(len(fares)):
		if np.isnan(fares[i]):
			continue
		else:
			bin_num = int(np.floor(fares[i]/(max_fare - min_fare)/bin_size))-1
			if survived[i] == 1:
				madeIt[bin_num] = madeIt[bin_num] + 1
			total[bin_num] = total[bin_num] + 1
						
	return madeIt, total	
	
def filter_SibSp(SibSp, survived):
	max_SibSp = int(np.max(SibSp))
	bin_size = 1
	madeIt = [0 for i in range(max_SibSp+1)]
	total = [0 for i in range(max_SibSp+1)]

	count = -1

	for i in range(len(SibSp)):
		if survived[i] == 1:
			madeIt[SibSp[i]] = madeIt[SibSp[i]] + 1
			
		total[SibSp[i]] = total[SibSp[i]] + 1
						
	return madeIt, total	

def filter_SexSibSp(SibSp, sex, survived, filter):
	max_SibSp = int(np.max(SibSp))
	bin_size = 1
	madeIt = [0 for i in range(max_SibSp+1)]
	total = [0 for i in range(max_SibSp+1)]

	count = -1

	for i in range(len(SibSp)):
		if survived[i] == 1 and sex[i] == filter:
			madeIt[SibSp[i]] = madeIt[SibSp[i]] + 1
		if sex[i] == filter:
			total[SibSp[i]] = total[SibSp[i]] + 1
						
	return madeIt, total
	
# Load the dataset
in_file = 'titanic_data.csv'
full_data = pd.read_csv(in_file)

# Print the first few entries of the RMS Titanic data
print full_data.head()


# From a sample of the RMS Titanic data, we can see the various features present for each passenger on the ship:
# - **Survived**: Outcome of survival (0 = No; 1 = Yes)
# - **Pclass**: Socio-economic class (1 = Upper class; 2 = Middle class; 3 = Lower class)
# - **Name**: Name of passenger
# - **Sex**: Sex of the passenger
# - **Age**: Age of the passenger (Some entries contain `NaN`)
# - **SibSp**: Number of siblings and spouses of the passenger aboard
# - **Parch**: Number of parents and children of the passenger aboard
# - **Ticket**: Ticket number of the passenger
# - **Fare**: Fare paid by the passenger
# - **Cabin** Cabin number of the passenger (Some entries contain `NaN`)
# - **Embarked**: Port of embarkation of the passenger (C = Cherbourg; Q = Queenstown; S = Southampton)
# 
# Since we're interested in the outcome of survival for each passenger or crew member, we can remove the **Survived** feature from this dataset and store it as its own separate variable `outcomes`. We will use these outcomes as our prediction targets.  
# Run the code cell below to remove **Survived** as a feature of the dataset and store it in `outcomes`.

# Store the 'Survived' feature in a new variable and remove it from the dataset
outcomes = full_data['Survived']
data = full_data.drop('Survived', axis = 1)

# Show the new dataset with 'Survived' removed
print data.head()

names = data["Name"]

##############################################################
############### Find patterns in title of name ###############
##############################################################
print "By Title"
titles, madeIt, total = find_titles(full_data['Name'],full_data['Survived'])
#print titles

for i in range(len(titles)):
	print titles[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " survived!!!"
#	if madeIt[i]/(total[i]+0.0) > 0.8:
#		print titles[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " survived!!!"
	
# Not much improvement can be made by filtering titles
print
print

###############################################################################
################# Find patterns by last name for the survived #################
###############################################################################
print "Filter of Survivors By Last Name"

lastName, madeIt, total = filter_lastName(full_data['Name'],full_data['Survived'])
#print titles

for i in range(len(lastName)):
	#print lastName[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " survived!!!"
	if madeIt[i]/(total[i]+0.0) >= 0.70 and total[i] > 1:
		print lastName[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " survived!!!"
	
print
print
	
###############################################################################
################# Find patterns by last name for the perished #################
###############################################################################
print "Filter of Non-Survivors By Last Name"

lastName, madeIt, total = filter_lastName(full_data['Name'],full_data['Survived']+1)
#print titles

for i in range(len(lastName)):
	#print lastName[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " did not survive!!!"
	if madeIt[i]/(total[i]+0.0) > 0.70 and total[i] > 1:
		print lastName[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " did not survive!!!"
		
## Noticed that names ending in son, sen perished.
print
print

# find out the % of son, sen that perished.
print "% of son, sen that perished"

survived = full_data["Survived"]
lastName = []
madeIt = []
total = []
count = -1
for i in range(len(names)):
	count = count + 1
	x = names[i].split(',')
	
	last3 = ""
	if "sen" == x[0][-3:]:
		last3 = "sen"
	elif "son" == x[0][-3:]:
		last3 = "son"
	else:
		continue
	
	if last3 == "":
		continue
	
	if (not x[0][-3:] in lastName) or (lastName == []):
		lastName.insert(len(lastName),x[0][-3:])
		total.insert(len(total),1)
		if survived[count] == 0:
			madeIt.insert(len(madeIt),1)
		else:
			madeIt.insert(len(madeIt),0)
	else:
		ind = lastName.index(x[0][-3:])
		total[ind] = total[ind] + 1
		if survived[count] == 0:
			madeIt[ind] = madeIt[ind] + 1
				
for i in range(len(lastName)):
	#if madeIt[i]/(total[i]+0.0) > 0.80 and total[i] > 1:
	print lastName[i] + " : " + str(madeIt[i]) + " out of " + str(total[i]) + " did not survive!!!"

# 47 out of 65 whose name ends in son did not survive
# 12 out of 14 whose name ends in sen did not survive
	
print
print

##############################################################
################# Find patterns by fare #################
##############################################################
print "Fares"
madeIt, total = filter_fare(full_data['Fare'],full_data['Survived'], np.min(full_data['Fare']), np.max(full_data['Fare']))

print madeIt
print total

# 36 out of 50 whose ticket fare was less than 40% bracket survived.
print
print

##########################################################
################# Find patterns by SibSp #################
##########################################################
print "SibSp"
madeIt, total = filter_SibSp(full_data['SibSp'],full_data['Survived'])

print madeIt
print total

# Nothing significant
print
print

#################################################################
################# Find patterns by SibSp & Male #################
#################################################################
print "SibSp & Male"
madeIt, total = filter_SexSibSp(full_data['SibSp'],full_data['Sex'],full_data['Survived'],"male")

print madeIt
print total

# Nothing significant
print
print

###################################################################
################# Find patterns by SibSp & Female #################
###################################################################
print "SibSp & Female"
madeIt, total = filter_SexSibSp(full_data['SibSp'],full_data['Sex'],full_data['Survived'],"female")

print madeIt
print total

# 77% of females that have less than or equal to 2 siblings survived
print
print

########################################################
################# Find patterns by age #################
########################################################
print "Age"
madeIt, total = filter_fare(full_data['Age'],full_data['Survived'],0,100)

print madeIt
print total

# Nothing significant
print
print

########################################################
################# Find patterns by Parch #################
########################################################
print "Parch"
madeIt, total = filter_SibSp(full_data['Parch'],full_data['Survived'])

print madeIt
print total

# Nothing significant
print
print

#####################################################################
################# Find patterns by Parch and Female #################
#####################################################################
print "Parch & Female"
madeIt, total = filter_SexSibSp(full_data['Parch'],full_data['Sex'],full_data['Survived'],"female")

print madeIt
print total

# Nothing significant
print
print

#############################################################################
################# Find patterns by Parch and Female and Age #################
#############################################################################
print "Parch & Female & 20<Age<60"
ind1 = np.where(full_data["Age"] > 30)[0]
ind2 = np.where(full_data["Age"] < 50)[0]
#ind3 = np.where(full_data["SibSp"] > 0)[0]
ind4 = np.where(full_data["Parch"] > 0)[0]
ind5 = np.where(full_data["Sex"] == "female")[0]
ind = list(set(ind1).intersection(ind2))
#ind = list(set(ind).intersection(ind3))
ind = list(set(ind).intersection(ind4))
ind = list(set(ind).intersection(ind5))
madeIt = 0
total = 0
for i in ind:
	if full_data['Survived'][i] == 1:
		madeIt = madeIt + 1
	total = total + 1

print madeIt
print total

# Nothing significant
print
print

#############################################################
################# Find patterns by Embarked #################
#############################################################
print "Embarked"
embarked = list(set(full_data["Embarked"]))
print embarked

madeIt = [0 for i in embarked]
total = [0 for i in embarked]

for i in range(len(full_data["Embarked"])):
	ind = embarked.index(full_data["Embarked"][i])
	
	if full_data["Survived"][i] == 1:
		madeIt[ind] = madeIt[ind] + 1
	total[ind] = total[ind] + 1

print madeIt
print total

# Nothing significant
print
print