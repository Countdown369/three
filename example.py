# Import the module
import three

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

test_request = three.requests(start='10-28-2021', end = '11-1-2021', count = 2)
print()
print("List of Service Request Dictionaries:")
print(test_request)
print()
print("Number of Service Requests in List:")
print(len(test_request))