import csv
from hashtable import HashTable


class Route:

    # Initializes a route object, this constructor is what is called to calculate a route based on several parameters
    def __init__(self, address_table, deliveries, start):
        self.addresses = address_table.addresses
        self.route = []
        self.deliveries = deliveries
        self.current = start
        self.hub = '4001 South 700'
        self.total = 0
        self.__calculate_route()

    # Loops through deliveries calling the __shortest_next method to calculate the next closest stop, then set return
    # to current and continues. Could all be done in one function, but make code slightly more modular for later edits.
    # O(n), though it practice it is O(n^2) since it calls an O(n) function inside a loop that relies on the same input
    def __calculate_route(self):
        while self.deliveries:
            self.current = self.__shortest_next(self.current)[0]

    # Loops through deliveries list to find the address contained in it is the least distance from the address
    # before(current). It accomplishes this by keeping a running variable(min_distance) of the lowest found distance
    # value and a variable of the address it relates to. These are set via a outcome of a comparison check each loop of
    # them vs current value from the delivery list loop.
    # After completing the loop it appends the closest address found to the route list, removes it from the deliveries
    # list and return the value to be set by the parent function to the current address, or for other uses if needed.
    # A field called total is incremented with the distance, this variable is mainly for debug/testing and isn't
    # actively used.
    # O(n)
    def __shortest_next(self, current):
        closest_address = None
        min_distance = 9999.0  # Unrealistic value will be replaced first iteration with the shortest distance so far

        for d in self.deliveries:
            address = self.addresses.get(current).paths.get(d[0])

            if address <= min_distance:
                min_distance = address
                closest_address = d

        self.route.append(closest_address)
        self.deliveries.remove(closest_address)
        self.total += min_distance
        return closest_address


# Class for addresses and their data. It contains a HashTable, that has nested HashTables in it which are used for O(n)
# look-ups of the distance from one address to another. A raw matrix could also be used for this, but it is more
# readable this way and also avoids errors that could come from a positional matrix, that could be hard to trace
class Addresses:
    def __init__(self, address_data, distance_data_raw):
        self.address_list = []
        self.addresses = None
        self.__init_address_list(address_data)
        self.__init_addresses(distance_data_raw)

    # Parses the addressData(address names) into a list that is indexed the same as the distanceTable data
    # Also initializes the base address hashTable that is used for address to address distance look ups
    # O(n)
    def __init_address_list(self, address_data):
        self.addresses = HashTable(sum(1 for line in open(address_data)))
        with open(address_data) as addresses:
            csv_reader = csv.reader(addresses, delimiter=',')

            for row in csv_reader:
                address, s, zipcode = row[0].partition("(")
                self.address_list.append(address)
                self.addresses.put(address, Address(address))

    # Parse the distanceTable data and converts it to a full matrix.
    # Then loops through each address in the address_list using it as a key to access the addresses hashtable.
    # Has an inner loop that also loops through all the address in the address list and sets a key for all of the
    # address, who value is the distance from the parent address to all other address.
    # O(n^2)
    def __init_addresses(self, distance_data_raw):
        with open(distance_data_raw) as distance:
            matrix = list(csv.reader(distance, delimiter=','))

        for r, row in enumerate(matrix):
            for c, col in enumerate(row):
                if col == '':
                    matrix[r][c] = matrix[c][r]

        for i in range(0, len(self.address_list)):
            for j in range(0, len(self.address_list)):
                self.addresses.get(self.address_list[i]).add_path(self.address_list[j], matrix[i][j])


# Simple class/container for addresses and a hashtable of their distances from other addresses
class Address:

    def __init__(self, address):
        self.address = address
        self.paths = HashTable(sum(1 for line in open('Data/addressData.csv')))

    def add_path(self, address, distance):
        self.paths.put(address, float(distance))
