from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
import pandas as pd
import types

addresses = pd.read_csv('name.csv')
original_df= pd.read_csv('./csv/housing.csv')

# Tell pandas to print all rows and columns of a dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Array that will collect all found zestimates/tax value
zestimate_column = []
# Array that keeps track of indexes where a zestimate couldn't be found (can't mutate the dataframe while looping through it)
no_zestimate = []


# --------------------------------------------------------------------------------
# FIND HOUSE ESTIMATES OR TAX VALUE
# --------------------------------------------------------------------------------
# Traverse through addresses
for i in addresses.index:
    splitAddress = addresses['address'][i].split(",")

    # Get the zip code
    zipcodeElement = splitAddress[-2:-1][0]
    zipcodeElementSplitted = zipcodeElement.split(" ")
    zipcode = zipcodeElementSplitted[2]

    # Get the address w/o zipcode and country
    address = splitAddress[0] + splitAddress[1] + ", " + zipcodeElementSplitted[1]

    try:    
        deep_search_response = zillow_data.get_deep_search_results(address,zipcode)
        result = GetDeepSearchResults(deep_search_response)

        # Print zestimate of the property
        if type(result.zestimate_amount) == str:
            zestimate_column.append(float(result.zestimate_amount))

        # If no zestimate, get the tax value
        # TAX ASSESSOR'S VALUE
        # Depending on the jurisdiction where you live, this value could be the tax assessed, 
        # tax appraised, or market assessed value. This value comes from the taxing authority of the city, 
        # county or state where you live; this is not Zillow's value.
        # Note: Tax assessor's values differ from Zillow's Zestimate, which is computed by entering numerous 
        # data points into a proprietary formula, often resulting in a more accurate value estimate.
        elif type(result.tax_value) == str and int(result.tax_year) > 2015:
            zestimate_column.append(float(result.tax_value))

        # If no zestimate or tax value, property doesn't exist rip
        else:
            print(address + ": has no zestimate " + result.tax_value)
            no_zestimate.append(addresses['address'][i])

    except:
        print(address + ": unable to find an estimate")
        no_zestimate.append(addresses['address'][i])

# Dropping the rows where a zestimate/tax value could not be found (.drop takes an array of row indexes)
addresses = addresses[~addresses['address'].isin(no_zestimate)]


# --------------------------------------------------------------------------------
# APPEND ZESTMATE WITH THEIR ADDRESSES
# --------------------------------------------------------------------------------
# If the amount of rows in DataFrame do not match number of rows in zestimate_column, something wrong is happening
if len(zestimate_column) != len(addresses):
	print('There appears to be a difference in size:\n', len(zestimate_column), len(addresses))
else:
	# Otherwise add the zestimates
	addresses['zestimate/tax_value'] = zestimate_column

# Resetting the index of the rows
addresses = addresses.reset_index(drop=True)


# --------------------------------------------------------------------------------
# CREATING 1ST DATA WITH ADDRESS
# --------------------------------------------------------------------------------
# Create an empty dataframe that contains only the relevant data of each address in addresses
column_names = ["longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income", "median_house_value", "ocean_proximity"]
data_from_original_df = pd.DataFrame(columns=column_names)

# Retrieve the row data from the original dataset
for index in addresses['row']:
    data = original_df.iloc[[index]]
    data_from_original_df = data_from_original_df.append(data, ignore_index=True)

# Combine the original dataframe with the new dataframe
combined_df = pd.concat([data_from_original_df, addresses], axis=1, join='inner')
del combined_df['row']

# Create csv with addresses, zestimate/tax value and original data
combined_df.to_csv('combined_data.csv', index=False)


# --------------------------------------------------------------------------------
# CREATING 2ND DATA WITH ZIP AND CITY
# --------------------------------------------------------------------------------
# Create an empty dataframe that contains zip and city column
column_names = ["city", "zip"]
city_and_zip_df = pd.DataFrame(columns=column_names)

# Traverse through addresses
for i in addresses.index:
    splitAddress = addresses['address'][i].split(",")

    #  Retrieve the zip code
    zipcodeElement = splitAddress[-2:-1][0]
    zipcodeElementSplitted = zipcodeElement.split(" ")
    zipcode = int(zipcodeElementSplitted[2])

    # Retrieve the city
    city = splitAddress[1].strip()

    # Add city and zip to city_and_zip_df
    city_and_zip_df = city_and_zip_df.append({'zip' : zipcode, 'city' : city}, ignore_index=True)

combined_df = pd.concat([combined_df, city_and_zip_df], axis=1, join='inner')
del combined_df['address']

# Create csv with addresses, zestimate/tax value and original data
combined_df.to_csv('combined_data_zip_city.csv', index=False)