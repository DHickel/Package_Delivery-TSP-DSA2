import copy
import datetime

from package import Status


class Simulation:

    # Constructor for the delivery simulation. A deep copy is made of the package_table so manipulation can happen
    # without overwriting the initial package data, this way the simulation can see the status of truck and packages
    # in various ways without having to re-construct the initial package table.
    def __init__(self, package_table, address_table, trucks):
        self.package_table = copy.deepcopy(package_table)
        self.address_table = address_table
        self.addresses = address_table.addresses
        self.trucks = copy.deepcopy(trucks)

    # Set some hardcoded start times, these could be expanded to be parameters if needed, but this work fines for this
    # use case. Approached this function in more of a scripting style, instead of modularity since it needs some
    # hard coded events to happen, that if made modular would add more complexity than needed for the current scope of
    # the project. Assigns the indexes of the trucks list to some variables for slightly better readability.
    #
    # Stop time parameter, is a time to stop running the simulation so the state of packages and trucks can be seen up
    # to that point in time.
    # O(n^2)
    def start_deliveries(self, stop_time):
        deliveries_finished = False
        truck1, truck2, truck3 = self.trucks[0], self.trucks[1], self.trucks[2]
        # These times use a "bogus" date since it is not needed for the simulation, but needed for deltatime calculations
        truck1.start_time = datetime.datetime(1, 1, 1, 8, 0, 0)
        truck2.start_time = datetime.datetime(1, 1, 1, 8, 45, 0)
        truck3.start_time = datetime.datetime(1, 1, 1, 23, 0, 0)
        delayed_arrival = datetime.datetime(1, 1, 1, 9, 5, 0)
        time = datetime.datetime(1, 1, 1, 8, 0, 0)

        # Loop checks a boolean deliveries finished, which is true only when all trucks are finished for the day
        # and also checks to see if simulation time is under stop time.
        # This loop is the main state of the simulation and use to increment time and distance, as well as package
        # delivery simulation and truck distance simulation based off its time variable.
        # The design here is like a "ticker" or a game loop, every iteration is 20 seconds in the delivery simulation
        # and if a truck is currently en route it will have a simulated .1 mile of travel each tick(iteration)
        while not deliveries_finished and time <= stop_time:

            # Loops through all the trucks every "tick" Check if the simulation time is past or equal to their start
            # time, if so they start their route if they are not already finished.
            for truck in self.trucks:

                if not truck.finished and time > truck.start_time:

                    # Separate if check to see if truck is at hub after their start time is passed
                    # If so it initiates the trucks internal delivery simulation and set them to no longer being at hub
                    if truck.at_hub:
                        truck.init_delivery_sim(self.addresses, self.package_table)
                        truck.at_hub = False

                    # Increments truck's travel simulation by .1 miles
                    truck.mileage += .1

                    # If a trucks current mileage is greater than the internal calculation of the total distance they
                    # would need to travel to make it to the next stop, then it executes the deliver_next function for
                    # that truck
                    if not truck.finished and truck.mileage >= truck.dist_to_next:
                        truck.deliver_next(time)

                # Hard coded status change for package 9 getting rerouted
                if time == datetime.datetime(1, 1, 1, 10, 20, 0):
                    package = self.package_table.get("9")
                    package.status = Status.ENROUTE
                    package.address = "410 S State St"

                    # Takes the existing route for the truck with the rerouted package and calculates the shortest route
                    # with that packages delivery address added in.
                    if truck.id == package.truck:
                        truck.update_route(self.address_table, (package.address, package.ID))

            # If either truck 1 or 2 are finished and truck 3 is not finished and still at hub, and the time is past
            # the time of the delayed package arrivals that truck 3 is meant to deliver, then set its start time to
            # current simulation time which then starts it on it's route.
            if truck1.finished or truck2.finished and not truck3.finished:
                if time > delayed_arrival and truck3.at_hub and not truck3.finished:
                    truck3.start_time = time

            # If all trucks are finished set deliveries_finished boolean to true, to stop the simulation
            if truck1.finished and truck2.finished and truck3.finished:
                deliveries_finished = True

            # Increments the simulation time by 20 seconds
            time = time + datetime.timedelta(seconds=20)

    # Various functions for printing out package and truck status of the simulated state.

    def package_info(self, pid):
        p = self.package_table.get(pid)
        print(
            "----------------------------------------------------------------------------------------------------------- "
            "------------------------------------------------------------------")
        self.__print_pinfo(p)
        print("\n")

    def all_packages(self):
        print(
            "-----------------------------------------------------------------------------------------------------------"
            "------------------------------------------------------------------")
        pckg_list = self.package_table.all()
        for p in pckg_list:
            self.__print_pinfo(p[1])
        print("\n")

    def trucks_at_time(self):
        print("----------------------------------------------------------------------------------------------------")
        for truck in self.trucks:
            self.__print_tinfo(truck)

    def trucks_final(self):
        print("----------------------------------------------------------------------------------------------------")
        for truck in self.trucks:
            self.__print_tinfo(truck)

        print(
            f"Total Mileage: {round((self.trucks[0].mileage + self.trucks[1].mileage + self.trucks[2].mileage), 1)} Miles")
        print("----------------------------------------------------------------------------------------------------")

    def __print_tinfo(self, truck):
        if truck.end_time == None:
            endtime = "Still On Route"
        else:
            endtime = truck.end_time.strftime('%H:%M:%S')

        print(f"|{truck.name}| At Hub: {truck.at_hub} | Finished: {truck.finished} | Current Location: {truck.current} "
              f"\n         Start Time: {truck.start_time.strftime('%H:%M:%S')} | End TIme : {endtime} | Mileage: {round(truck.mileage, 1)} Miles  ")
        print("----------------------------------------------------------------------------------------------------")

    def __print_pinfo(self, package):

        if package.time_delivered is not None:
            dtime = package.time_delivered.strftime('%H:%M:%S')
        else:
            dtime = "YTD"

        print(
            f"ID: {package.ID} | Address: {package.address} | Deadline: {package.deadline} | City: {package.city} | Zipcode: "
            f"{package.zipcode} | Weight: {package.weight} | Status: {package.status.name} | Time Delivered: {dtime}")
        print(
            "-----------------------------------------------------------------------------------------------------------"
            "------------------------------------------------------------------")
