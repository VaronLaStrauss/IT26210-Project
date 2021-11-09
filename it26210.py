from operator import itemgetter
import json
import requests
from urllib import parse

MAIN_API = "https://open.mapquestapi.com/directions/v2/alternateroutes?"
KEY = "zTPMdKRWp9kgYVPLVPtGUGfNHhu2dmUY"

def test_api_status_matcher() -> bool:
    status = 402
    assert api_status_matcher(status) is False
    status = 611
    assert api_status_matcher(status) is False
    status = 0
    assert api_status_matcher(status) is True
    status = "any"
    assert api_status_matcher(status) is False

def get_route(origin: str, destination: str, number_of_routes: int) -> any:
    url = MAIN_API + parse.urlencode(
            {
                "key": KEY, 
                "from": origin, 
                "to": destination, 
                "maxRoutes": number_of_routes
            }
        )
    print(url)
    json_data = requests.get(url).json()
    json_data = json.dumps(json_data)
    json_data = json.loads(json_data)
    return json_data

def api_status_matcher(status: int) -> bool:
    should_continue = False
    match status:
        case 402:
            print("**********************************************")
            print("Status Code: 402 - Invalid input for one or both locations.")
            print("**********************************************")
        case 611:
            print("**********************************************")
            print("Status Code: 611 - Missing an entry for one or both locations.")
            print("**********************************************")
        case 0:
            print("API Status: 0 - A successful route call.\n")
            print("=============================================")
            should_continue = True
        case _:
            print("************************************************************************")
            print("For Staus Code: " + 
                str(status) + 
                "; Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("************************************************************************")
    print()
    return should_continue

def print_route(json_data: any, distUnit: float, gas_unit: float, inner = False) -> None:
    route = itemgetter('route')(json_data)
    has_toll, has_bridge, has_tunnel, \
        has_country_cross, formatted_time, \
        distance, fuel_used = itemgetter(
            'hasTollRoad',
            'hasBridge',
            'hasTunnel',
            'hasCountryCross',
            'formattedTime',
            'distance',
            'fuelUsed'
        )(route)

    if has_toll:
        print("The road that you will go through will have a toll gate so ready your cash.")
    if has_bridge:
        print("The road that you will go through will have a bridge so be safe when driving.")
    if has_tunnel:
        print("The road that you will go through will have a tunnel so make sure your lights are working.")
    if has_country_cross:
        print("You need to go to another country to reach your destination.")

    print("Trip Duration: " + formatted_time)
    print(
        "Distance: " + 
        str("{:.2f}".format(distance)) + 
        (" mi" if distUnit == 1 else " km"))

    print(
        "Fuel Used: " + 
        str("{:.2f}".format(fuel_used * gas_unit)) + 
        (" gallon(s)" if gas_unit == 1 else " Liter(s)"))
    print()

    for maneuver in route["legs"][0]["maneuvers"]:
        narrative, dist, time =  itemgetter('narrative', 'distance', 'formattedTime')(maneuver)
        print(
            narrative + 
            " With a distance of " + 
            str("{:.2f}".format(dist * distUnit) + 
            (" mi" if distUnit == 1 else " km")) + 
            " and estimated time of " + 
            str(time))

    print()
    print("=============================================\n")

    if "alternateRoutes" in route:
        for alternate in route["alternateRoutes"]:
            print("Alternate Route: \n")
            print_route(alternate, distUnit, gas_unit, True)
    elif not inner:
        print("No alternate routes found.")

def main():
    should_quit = False
    while not should_quit:
        loc1 = ""
        loc2 = ""
        while loc1 == "":
            loc1 = input("Starting Location: ")
        while loc2 == "":
            loc2 = input("Destination: ")
    
        dist_unit = 1 if input("Use kilometers for distance? (Y/n): ").lower() == "n" else 1.6
        gas_unit = 1 if input("Use Liters for gasoline? (Y/n): ").lower() == "n" else 3.78541

        if "" in [loc1, loc2]: 
            print("Please enter a value for both locations")
            continue

        number_of_routes = 1  
        try:
            route_str = (input("Number of routes (1): "))
            if route_str == "":
                number_of_routes = 1
            number_of_routes = int(route_str)
        except ValueError:
            print("Invalid number of routes. Using 1 route only")
            number_of_routes = 1

        json_data = get_route(loc1, loc2, number_of_routes)
        json_status = json_data["info"]["statuscode"]

        if api_status_matcher(json_status):
            print("Directions from " + (loc1) + " to " + (loc2))
            print()
            print_route(json_data, dist_unit, gas_unit)

        user_continue = input("Continue? (Y/n): ").lower()
        should_quit = user_continue in ["n", "no"]

if __name__ == "__main__":
    main()
