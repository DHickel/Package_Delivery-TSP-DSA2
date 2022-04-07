import csv
from hashtable import HashTable
from package import Package, Status
from truck import Truck


class Load:

    # loads the trucks in a somewhat modular way, though it doesnt enforce restrictions this could be added later.
    def __init__(self, package_csv):
        self.package_table = HashTable(sum(1 for line in open(package_csv)))
        self.trucks = [Truck("Truck1", 1), Truck("Truck2", 2), Truck("Truck3", 3)]
        self.__load_trucks(package_csv)

    def __load_trucks(self, package_csv):

        t1_zips = [84107, 84115, 84106, 84105, 84106]
        t2_zips = [84103, 84104, 84111, 84119, 84123]

        with open(package_csv) as packages:
            csv_reader = csv.reader(packages, delimiter=',')

            for row in csv_reader:
                package = Package()
                package.ID = row[0]
                package.address = row[1]
                package.city = row[2]
                package.state = row[3]
                package.zipcode = int(row[4])
                package.deadline = row[5]
                package.weight = row[6]
                package.note = row[7]

                if "will not arrive to depot until" in row[7]:
                    package.truck = 3
                elif row[0] == "15":
                    package.truck = 1
                elif "delivered with" in row[7]:
                    package.truck = 1
                elif "Can only be on" in row[7]:
                    package.truck = 2
                elif int(row[4]) in t1_zips:
                    package.truck = 1
                elif int(row[4]) in t2_zips:
                    package.truck = 2
                else:
                    package.truck = 3

                if "Wrong" in row[7]:
                    package.status = Status.HOLD

                # Offset by -1 to account for list starting index being 0 but starting truck index being 1
                self.trucks[package.truck - 1].package_list.append(row[0])
                # Inserts key(package ID) Value(package Object) into HashTable
                self.package_table.put(package.ID, package)

            packages.close()


