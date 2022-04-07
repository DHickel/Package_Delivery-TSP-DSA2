import datetime
from package import Status
from route import Route, Addresses
from simulation import Simulation
from load import Load

package_data = 'Data/packageData.csv'
address_data = 'Data/addressData.csv'
distance_data = 'Data/distanceTable.csv'
hub = '4001 South 700'

# Loads the packages on trucks, and initiates the HashTable of package data
load = Load(package_data)
# Initiates the nested HashTable containing distances as well a helper list of addresses strings
address_table = Addresses(address_data, distance_data)
# Assigns the package_table to a variable
package_table = load.package_table
# Assigns the list of loaded truck objects to a variable
trucks = load.trucks

# Iterates through list of trucks, uses their package_lists of package IDs to make a list of tuples with their ID and
# address. Then uses this list to generate a route using the algorithm in the route class, and assigns it to route
# field for each truck. Finally, it sets their first delivery address to the address at the beginning of the route list.
for truck in trucks:
    deliveries = []
    for p in truck.package_list:
        if package_table.get(p).status != Status.HOLD:
            deliveries.append((package_table.get(p).address, p))
    truck.route = Route(address_table, deliveries, hub).route
    truck.next = truck.route[0][0]

quit = False

# Simple function for input validation on menu
# O(1)

# While loop with menu options, loops until q inputted to quit
while not quit:
    print("############################################")
    print("                    Menu                    ")
    print("############################################")
    print(" 1 | Status Of Package(Single) [id, time]")
    print(" 2 | Status Of Package(All)    [time]")
    print(" 3 | Status Of Delivery Trucks [time]")
    print(" 4 | Total Mileage Of Trucks   [End of Day] ")
    print(" q | Quit\n")

    user_input = input("Input:")
    pid = ""
    time_hr = ""
    time_min = ""

    if user_input == "1":
        pid = input("Package ID:")
        time_hr = input("Hour:")
        time_min = input("Minute:")
        delivery_sim = Simulation(package_table, address_table, trucks)
        try:
            time = datetime.datetime(1, 1, 1, int(time_hr), int(time_min), 0)
            delivery_sim.start_deliveries(time)
            delivery_sim.package_info(pid)
        except:
            print("Invalid Input")
        input("Press Enter To Continue...")

    elif user_input == "2":
        time_hr = input("Hour:")
        time_min = input("Minute:")
        delivery_sim = Simulation(package_table, address_table, trucks)
        try:
            time = datetime.datetime(1, 1, 1, int(time_hr), int(time_min), 0)
            delivery_sim.start_deliveries(time)
            delivery_sim.all_packages()
        except:
            print("Invalid Input")
        input("Press Enter To Continue...")

    elif user_input == "3":
        time_hr = input("Hour:")
        time_min = input("Minute:")
        delivery_sim = Simulation(package_table, address_table, trucks)
        try:
            time = datetime.datetime(1, 1, 1, int(time_hr), int(time_min), 0)
            delivery_sim.start_deliveries(time)
            delivery_sim.trucks_at_time()
        except :
            print("Invalid Input")
        input("Press Enter To Continue...")

    elif user_input == "4":
        delivery_sim = Simulation(package_table, address_table, trucks)
        time = datetime.datetime(1, 1, 1, 23, 59, 0)
        delivery_sim.start_deliveries(time)
        delivery_sim.trucks_final()
        input("Press Enter To Continue...")

    elif user_input == "q":
        quit = True

    else:
        print("\nError! Invalid Input!\n")
