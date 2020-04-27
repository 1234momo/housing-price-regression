from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
import pandas as pd
import types

addresses = pd.read_csv('name.csv')
original_df= pd.read_csv('./csv/housing copy.csv')
zillow_data = ZillowWrapper('X1-ZWz1fjckjdd8gb_a2eph')

# Tell pandas to print add rows and columns of a dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Array that will collect all found zestimates/tax value
zestimate_column = []
# Array that keeps track of indexes where a zestimate couldn't be found (can't mutate the dataframe while looping through it)
no_zestimate = []

for i in addresses.index:
    splitAddress = addresses['address'][i].split(",")

    zipcodeElement = splitAddress[-2:-1][0]
    zipcodeElementSplitted = zipcodeElement.split(" ")
    zipcode = zipcodeElementSplitted[2]

    address = splitAddress[0] + splitAddress[1] + ", " + zipcodeElementSplitted[1]

    try:    
        deep_search_response = zillow_data.get_deep_search_results(address,zipcode)
        result = GetDeepSearchResults(deep_search_response)

        # Print zestimate of the property
        if type(result.zestimate_amount) == str:
            print(address + ": " + result.zestimate_amount)
            zestimate_column.append(result.zestimate_amount)
            # print(zestimate_column)

        # If no zestimate, get the tax value
        # TAX ASSESSOR'S VALUE
        # Depending on the jurisdiction where you live, this value could be the tax assessed, 
        # tax appraised, or market assessed value. This value comes from the taxing authority of the city, 
        # county or state where you live; this is not Zillow's value.

        # Note: Tax assessor's values differ from Zillow's Zestimate, which is computed by entering numerous 
        # data points into a proprietary formula, often resulting in a more accurate value estimate.
        elif type(result.tax_value) == str and int(result.tax_year) > 2010:
            print(address + " tax estimate for year " + result.tax_year + ": " + result.tax_value)
            zestimate_column.append(result.tax_value)
            # print(zestimate_column)

        # If no zestimate or tax value, property doesn't exist rip
        else:
            print(address + ": has no zestimate " + result.tax_value)
            no_zestimate.append(addresses['address'][i])
			
    except:
        print(address + ": unable to find an estimate")
        no_zestimate.append(addresses['address'][i])


# print('Properties with found Zestimates/Tax Values:\n', zestimate_column)
# print(no_zestimate)

# Dropping the rows where a zestimate/tax value could not be found (.drop takes an array of row indexes)
addresses = addresses[~addresses['address'].isin(no_zestimate)]

# If the amount of rows in DataFrame do not match number of rows in zestimate_column, something weird is happening
if len(zestimate_column) != len(addresses):
	print('There appears to be a difference in size:\n', len(zestimate_column), len(addresses))
else:
	# Otherwise add the zestimates
	addresses['zestimate/tax_value'] = zestimate_column

# Resetting the index of the rows
addresses = addresses.reset_index(drop=True)

# Create an empty dataframe that contains only the relevant data of each address in addresses
column_names = ["housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income", "median_house_value", "ocean_proximity"]
data_from_original_df = pd.DataFrame(columns=column_names)

for index in addresses['row']:
    data = original_df.iloc[[index]]
    data_from_original_df = data_from_original_df.append({'housing_median_age' : data['housing_median_age'], 'total_rooms' : data['total_rooms'], 'total_bedrooms' : data['total_bedrooms'], 'population' : data['population'], 'households' : data['households'], 'median_income' : data['median_income'], 'median_house_value' : data['median_house_value'], 'ocean_proximity' : data['ocean_proximity']}, ignore_index=True)

# Combine the original dataframe with the new dataframe
combined_df = pd.concat([addresses, original_df], axis=1, join='inner')
del combined_df['row']

print(combined_df)