import datetime
from package import Status
from route import Route


class Truck:
    # Constructor of various fields related to the truck, its route, mileage, start time, end time, and some internal
    # ones used for delivery simulation.
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.package_list = []
        self.route = []
        self.start_time = None
        self.end_time = None
        self.mileage = 0
        self.hub = ('4001 South 700', None)
        self.mph = 18
        self.at_hub = True
        self.finished = False
        self.current = self.hub
        self.next = None
        self.addresses = None
        self.dist_to_next = 0
        self.package_table = None

    # Updates the route, takes a new package as a parameter and recalculates the existing route with it calculated in.
    # O(1)
    def update_route(self, addresses_table, new_delivery):
        self.route.append(new_delivery)
        new_route = Route(addresses_table, self.route, self.route[0][0])
        self.route = new_route.route

    # Initializes the trucks internal delivery simulation fields. Set package statuses to ENROUTE if they are not on
    # hold Then calculates the distance from its current location to the next stop on the route. Then set the next
    # field to the next addresses stop. The distance between these is then added to the distance_to_next field,
    # which is used to monitor if a truck has reached the location of its next stop. This data is used by the main
    # simulation class loop.
    # O(n)
    def init_delivery_sim(self, addresses, package_table):
        self.package_table = package_table

        for p in self.package_list:
            package = package_table.get(p)

            if package.status != Status.HOLD:
                package.status = Status.ENROUTE

        self.addresses = addresses
        self.dist_to_next = self.__calc_dist_to_next(self.current[0], self.route[0][0])
        self.next = self.route[0]

    # O(n) because of while loop that may be triggered, but generally will have a constant run time and
    # shouldn't loop through all of n

    # Called from the main simulation loop and simulates the delivering of a package. THe involves getting the
    # package id from the route tuple, calling a function to set it as delivered as well as the time delivered. Then
    # if there is a next stop in the route list set it to next and calculate the distance to it. If the next address
    # is the same as the current address, then it while loops delivering all the packages that need delivered to the
    # same address. The elif is triggered if there are no more addresses in the route and the next stop has not yet
    # been set to the hub address, if so it set the next address to the hub, and calculates the distance needed to
    # travel to reach it. If route is also empty and the next position is the hub, then the hub has been reached and
    # the trucks  at_hub, finished, and end time variables can be set. Also sets current location to the address of
    # the hub.
    def deliver_next(self, time):
        package_id = None
        if self.next is not None:
            package_id = self.next[1]
            self.mark_delivered(package_id, time)

        if self.route:
            self.current = self.next
            self.route.remove(self.next)

            if self.route:
                self.next = self.route[0]
                self.dist_to_next += self.__calc_dist_to_next(self.current[0], self.next[0])

                # Delivers multiple packages at address if they exists
                while self.current[0] == self.next[0]:
                    self.mark_delivered(self.next[1], time)
                    self.current = self.next
                    self.route.remove(self.next)
                    self.next = self.route[0]
                    self.dist_to_next += self.__calc_dist_to_next(self.current[0], self.next[0])

        elif self.next != self.hub:
            self.next = self.hub
            self.dist_to_next += self.__calc_dist_to_next(self.current[0], self.next[0])

        else:
            self.at_hub = True
            self.finished = True
            self.end_time = time
            self.current = self.hub[0]

    # Called by deliver_next to avoid code redundancy and marks a packages' status as delivered and set the delivered
    # time to the current simulation time.
    def mark_delivered(self, package_id, time):
        if package_id is not None:
            package = self.package_table.get(package_id)
            package.status = Status.DELIVERED
            package.time_delivered = time

    # Simple method to get the distance between two addresses
    def __calc_dist_to_next(self, current, next):
        return self.addresses.get(current).paths.get(next)
