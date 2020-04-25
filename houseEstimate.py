from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults
import pandas as pd
import types

addresses = pd.read_csv('name.csv')

# TODO: Change the API KEY. This is some1 else's but i can't change my API KEY clearance bc servers r down
zillow_data = ZillowWrapper('X1-ZWz1fjckjdd8gb_a2eph')

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

        # If no zestimate, get the tax value
        # TAX ASSESSOR'S VALUE
        # Depending on the jurisdiction where you live, this value could be the tax assessed, 
        # tax appraised, or market assessed value. This value comes from the taxing authority of the city, 
        # county or state where you live; this is not Zillow's value.

        # Note: Tax assessor's values differ from Zillow's Zestimate, which is computed by entering numerous 
        # data points into a proprietary formula, often resulting in a more accurate value estimate.
        elif type(result.tax_value) == str:
            print(address + ": " + result.tax_value)

        # If no zestimate or tax value, property doesn't exist rip
        else:
            print(address + ": has no zestimate")
    except:
        print(address + ": unable to find an estimate")