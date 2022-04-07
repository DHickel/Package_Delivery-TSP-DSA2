import csv
from hashtable import HashTable



class Route:
    address_list = None
    addresses = None

    def __init__(self, address_table, deliveries, start):
        self.address_list = address_table.address_list
        self.addresses = address_table.addresses
        self.route = []
        self.deliveries = deliveries
        self.current = start
        self.hub = '4001 South 700'
        self.total = 0
        self.__calculate_route()

    def shortest_next(self, current):
        closest_address = None
        min_distance = 9999
        for d in self.deliveries:
            address = self.addresses.get(current).paths.get(d[0])
            if address <= min_distance:
                min_distance = address

                closest_address = d

        self.route.append(closest_address)
        self.deliveries.remove(closest_address)
        self.total += min_distance
        return closest_address

    def __calculate_route(self):
        while self.deliveries:
            self.current = self.shortest_next(self.current)[0]


class Addresses:
    def __init__(self, address_data, distance_data_raw):
        # Array of address name, indexed same as addresses for easy look ups

        # Array of address objects, containing a paths( distance) table to every other address
        self.address_list = []
        self.addresses = None
        self.__init_address_list(address_data)
        self.__init_addresses(distance_data_raw)

    def __init_address_list(self, address_data):
        self.addresses = HashTable(sum(1 for line in open(address_data)))
        with open(address_data) as addresses:
            csv_reader = csv.reader(addresses, delimiter=',')

            for row in csv_reader:
                address, s, zipcode = row[0].partition("(")
                self.address_list.append(address)
                self.addresses.put(address, Address(address))

    def __init_addresses(self, distance_data_raw):
        with open(distance_data_raw) as distance:
            matrix = list(csv.reader(distance, delimiter=','))

        for r, row in enumerate(matrix):
            for c, col in enumerate(row):
                if col == '':
                    matrix[r][c] = matrix[c][r]

        for i in range(0, 27):
            for j in range(0, 27):
                self.addresses.get(self.address_list[i]).add_path(self.address_list[j], matrix[i][j])


class Address:

    def __init__(self, address):
        self.address = address
        self.paths = HashTable(sum(1 for line in open('Data/addressData.csv')))


    def add_path(self, address, distance):
        self.paths.put(address, float(distance))
