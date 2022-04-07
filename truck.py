import datetime
from package import Status
from route import Route


class Truck:

    def __init__(self, name, id):
        # A simple list is used instead of a sub HashTable since only ID is needed
        # IDs can be used to access information from main package_table HashTable
        # Delivery status updates will be recorded on the package_table as well
        # start_time will be set once deliveries commence, end time is set once returned to hub
        # Mileage is incremented as deliveries occur
        self.name = name
        self.id = id
        self.package_list = []
        self.route = []
        self.start_time = datetime.datetime(1, 1, 1, 0, 0, 0)
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

    def update_route(self, addresses_table, new_delivery):
        self.route.append(new_delivery)
        new_route = Route(addresses_table, self.route, self.route[0][0])
        self.route = new_route.route

    def init_delivery_sim(self, addresses, package_table):
        self.package_table = package_table

        for p in self.package_list:
            package = package_table.get(p)

            if package.status != Status.HOLD:
                package.status = Status.ENROUTE

        self.addresses = addresses
        self.dist_to_next = self.__calc_dist_to_next(self.current[0], self.route[0][0])
        self.next = self.route[0]

    def deliver_next(self,time):
        package_id = None
        if self.next is not None and self.next != 0:

            package_id = self.next[1]
            self.mark_delivered(package_id, time)

        if self.route:
            self.current = self.next
            self.route.remove(self.next)

            if self.route:
                self.next = self.route[0]
                self.dist_to_next += self.__calc_dist_to_next(self.current[0], self.next[0])
                #Deliveres multiple packages at address if they exists
                while self.current[0] == self.next[0]:
                    self.mark_delivered(self.next[1], time)
                    self.current = self.next
                    self.route.remove(self.next)
                    self.next = self.route[0]
                    self.dist_to_next += self.__calc_dist_to_next(self.current[0], self.next[0])
            else:
                self.next = None

        elif self.next != self.hub:
            self.next = self.hub
            self.dist_to_next += self.__calc_dist_to_next(self.current[0], self.next[0])

        else:
            self.at_hub = True
            self.finished = True
            self.end_time = time
            self.current = self.hub[0]

    def mark_delivered(self,package_id, time):
        if package_id is not None:
            package = self.package_table.get(package_id)
            package.status = Status.DELIVERED
            package.time_delivered = time

    def __calc_dist_to_next(self, current, next):
        return self.addresses.get(current).paths.get(next)












