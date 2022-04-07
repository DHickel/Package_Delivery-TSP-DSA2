import copy
import datetime


from package import Status


class Simulation:

    def __init__(self, package_table, address_table, trucks):
        self.package_table = copy.deepcopy(package_table)
        self.address_table = address_table
        self.addresses = address_table.addresses
        self.trucks = copy.deepcopy(trucks)

    def start_deliveries(self, stop_time):
        deliveries_finished = False
        truck1, truck2, truck3 = self.trucks[0], self.trucks[1], self.trucks[2]
        truck1.start_time = datetime.datetime(1, 1, 1, 8, 0, 0)
        truck2.start_time = datetime.datetime(1, 1, 1, 8, 45, 0)
        truck3.start_time = datetime.datetime(1, 1, 1, 23, 0, 0)
        delayed_arrival = datetime.datetime(1, 1, 1, 9, 5, 0)
        time = datetime.datetime(1, 1, 1, 8, 0, 0)

        while not deliveries_finished and time <= stop_time:

            for truck in self.trucks:

                if not truck.finished and time > truck.start_time:

                    if truck.at_hub:
                        truck.init_delivery_sim(self.addresses, self.package_table)
                        truck.at_hub = False

                    truck.mileage += .1

                    if not truck.finished and truck.mileage > truck.dist_to_next:
                        truck.deliver_next(time)


                if time == datetime.datetime(1, 1, 1, 10, 20, 0):
                    package = self.package_table.get("9")
                    package.status = Status.ENROUTE
                    package.address = "410 S State St"

                    if truck.id == package.truck:
                        truck.update_route(self.address_table, (package.address, package.ID))

            if truck1.finished or truck2.finished and not truck3.finished:
                if time > delayed_arrival and truck3.at_hub and not truck3.finished:
                    truck3.start_time = time

            time = time + datetime.timedelta(seconds=20)

    def package_info(self, pid):
        p = self.package_table.get(pid)
        print("----------------------------------------------------------------------------------------------------------- "
            "------------------------------------------------------------------")
        self.__print_pinfo(p)
        print("\n")

    def all_packages(self):
        print("-----------------------------------------------------------------------------------------------------------"
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

        print(f"Total Mileage: {round((self.trucks[0].mileage + self.trucks[1].mileage + self.trucks[2].mileage),1)} Miles")
        print("----------------------------------------------------------------------------------------------------")

    def __print_tinfo(self, truck):
        if truck.end_time == None:
            endtime = "Still On Route"
        else:
            endtime = truck.end_time.strftime('%H:%M:%S')

        print (f"|{truck.name}| At Hub: {truck.at_hub} | Finished: {truck.finished} | Current Location: {truck.current} "
               f"\n         Start Time: {truck.start_time.strftime('%H:%M:%S')} | End TIme : {endtime} | Mileage: {round(truck.mileage,1)} Miles  ")
        print("----------------------------------------------------------------------------------------------------")

    def __print_pinfo(self, package):

        if package.time_delivered is not None:
            dtime = package.time_delivered.strftime('%H:%M:%S')
        else:
            dtime = "YTD"

        print(f"ID: {package.ID} | Address: {package.address} | Deadline: {package.deadline} | City: {package.city} | Zipcode: "
              f"{package.zipcode} | Weight: {package.weight} | Status: {package.status.name} | Time Delivered: {dtime}")
        print("-----------------------------------------------------------------------------------------------------------"
            "------------------------------------------------------------------")