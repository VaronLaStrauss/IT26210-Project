import urllib.parse
import requests
from operator import itemgetter
import json

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "zTPMdKRWp9kgYVPLVPtGUGfNHhu2dmUY"


while True:
    locations = []
    shouldQuit = input("Continue? (Y/n): ").lower()
    if shouldQuit in ['n', 'no']: break 
    loc1 = ""
    loc2 = ""
    while loc1 == "":
        loc1 = input("Starting Location: ")
    while loc2 == "":
        loc2 = input("Destination: ")
    
    distUnit = 1 if input("Use kilometers for distance? (Y/n)").lower() == "n" else 1.6
    gasUnit = 1 if input("Use Liters for gasoline? (Y/n)").lower() == "n" else 3.78541

    locations.append(loc1)
    locations.append(loc2)

    if("" in locations): 
        print("Please enter a value for both locations")
        continue
    url = main_api + urllib.parse.urlencode({"key": key, "from": locations[0], "to": locations[1]})
    print ("URL: ", (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    match json_status:
        case 402:
            print("**********************************************")
            print("Status Code: 402 - Invalid input for one or both locations.")
            print("**********************************************")
        case 611:
            print("**********************************************")
            print("Status Code: 611 - Missing an entry for one or both locations.")
            print("**********************************************")
        case 0:
            print("API Status: 0 - A successful route call.")
            print("=============================================")
            print("Directions from " + (locations[0]) + " to " + (locations[1]))
            print()

            route = itemgetter('route')(json_data)
            hasTollRoad, hasBridge, hasTunnel, \
                hasCountryCross, formattedTime, \
                distance, fuelUsed = itemgetter(
                    'hasTollRoad',
                    'hasBridge',
                    'hasTunnel',
                    'hasCountryCross',
                    'formattedTime',
                    'distance',
                    'fuelUsed'
                )(route)

            if hasTollRoad:
                print("The road that you will go through will have a toll gate so ready your cash.")
            if hasBridge:
                print("The road that you will go through will have a bridge so be safe when driving.")
            if hasTunnel:
                print("The road that you will go through will have a tunnel so make sure your lights are working.")
            if hasCountryCross:
                print("You need to go to another country to reach your destination.")

            print("Trip Duration: " + formattedTime)
            print(
                "Distance: " + 
                str("{:.2f}".format(distance)) + 
                (" mi" if distUnit == 1 else " km"))
            print("Fuel Used: " + 
                str("{:.2f}".format(fuelUsed * gasUnit)) + 
                (" gallon(s)" if gasUnit == 1 else " Liter(s)"))

            print()

            print(json.dumps(route["legs"], indent=4, sort_keys=True))

            for maneuver in route["legs"][0]["maneuvers"]:
                narrative, dist, time =  itemgetter('narrative', 'distance', 'formattedTime')(maneuver)
                print(
                    narrative + 
                    " With a distance of " + 
                    str("{:.2f}".format(dist * distUnit) + 
                    (" mi" if distUnit == 1 else " km")) + 
                    " and estimated time of " + 
                    str(time))
            print("=============================================\n")
        case _:
            print("************************************************************************")
            print("For Staus Code: " + 
                str(json_status) + 
                "; Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("************************************************************************")
