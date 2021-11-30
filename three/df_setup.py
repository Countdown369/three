# Import the module
import three
import pandas as pd
import time

# Set your city
three.city('boston')

"""
three.requests() takes a start date ('start') and an end date ('end)
to gather service calls from the start date to the end date.

It also takes an optional "count" argument which can grab as many or as few
service calls as needed (if not specified, default is 50).

As far as I can tell, there is no way to request specific types of service
requests (like Rodent Sighting, Bicycle Issues, etc). But we can request a
lot of service requests and then filter them.

It will return a list of dictionaries, each dict containing 1 service request.
"""

# test_request = three.requests(start='10-31-2021', end = '11-1-2021', count = 20)
# print()
# print("List of Service Request Dictionaries:")
# print(test_request)
# print()
# print("Number of Service Requests in List:")
# print(len(test_request))

# test_df = pd.DataFrame(data=test_request)

"""
Columns of test_df (all strings):
    service_request_id
    status
    status_notes
    service_name
    service_code
    description
    requested_datetime
    updated_datetime
    address
    lat
    long
    media_url  
"""

dfs = []
endmonth = 11
endday = 28
countnum = 50


for year in ['2019', '2020', '2021']:
    print("Month of 2021: " + year)
    for month in range(1, endmonth):
        print("Month of 10:  " + str(month))
        if month == 3:
            pass
        for day in range(1, endday):
            try:
                # import pdb; pdb.set_trace()
                startstring = str(month) + '-' + str(day) + '-' + year
                endstring = str(month) + '-' + str(day + 1) + '-' + year
                request_instance = three.requests(start = startstring, end = endstring, count= countnum)
                df_instance = pd.DataFrame(data=request_instance)
                dfs.append(df_instance)
                print("Day of 27: " + str(day))
            except ValueError:
                print("Too many requests, waiting 10 seconds.")
                time.sleep(10)
                try:
                    startstring = str(month) + '-' + str(day) + '-' + year
                    endstring = str(month) + '-' + str(day + 1) + '-' + year
                    request_instance = three.requests(start = startstring, end = endstring, count= countnum)
                    df_instance = pd.DataFrame(data=request_instance)
                    dfs.append(df_instance)
                    print("Day of 27: " + str(day))
                except ValueError:
                    try:
                        print("Too many requests, waiting 80 seconds.")
                        time.sleep(80)
                        startstring = str(month) + '-' + str(day) + '-' + year
                        endstring = str(month) + '-' + str(day + 1) + '-' + year
                        request_instance = three.requests(start = startstring, end = endstring, count= countnum)
                        df_instance = pd.DataFrame(data=request_instance)
                        dfs.append(df_instance)
                        print("Day of 27: " + str(day))
                    except ValueError:
                        print("Uh oh.")
        
result = pd.concat(dfs)
result.to_pickle("output.pkl")

pls = pd.read_pickle("output.pkl")

import pdb; pdb.set_trace()