import csv
import datetime
from pprint import pprint
from Packages import package_table
from Packages import amount_of_packages

# Creates matrix of distances from file
with open('Data/WGUPS_Distance_Matrix.csv', newline='') as distance_file:
    cvs_distance_list = csv.reader(distance_file, delimiter=',')
    distance_table = list(cvs_distance_list)

# Initializes global variables
delivery_start = ['8:00:00', '9:10:00', '10:20:00', '9:50:00']
package_master = []
total_distance = 0

# Creates nested dictionary of trucks. 
# add additional trucks here
truck_table = {1: {'status': 'at hub'},
               2: {'status': 'at hub'},
               3: {'status': 'at hub'},
               4: {'status': 'at hub'}, }  # second load of truck 1 = truck 4

# Fills package_master with every package ID
for index in range(1, amount_of_packages + 1):
    package_master.append(int(index))

# Adds special packages to trucks and removes package ID's from package_master
for index in range(1, amount_of_packages + 1):

    package_info = package_table.get(index - 1)

    # load packages on truck 1 that have time requirement or need to be shipped together
    if package_info[5] != 'EOD' and package_info[7] == 'None' or ('Must' in package_info[7]):
        truck_table[1]["slot_{0}".format(len(truck_table[1]))] = index
        package_master.remove(int(index))

    # load packages on truck 1 second trip that are delayed and time sensitive
    elif index == 25:
        truck_table[4]["slot_{0}".format(len(truck_table[4]))] = index
        package_master.remove(int(index))

    # load packages on truck 2 that are delayed in route
    elif 'truck 2' in package_info[7] or 'Delayed' in package_info[7]:
        truck_table[2]["slot_{0}".format(len(truck_table[2]))] = index
        package_master.remove(int(index))

    # load package on truck 3 with change of address and change said address
    elif 'Wrong' in package_info[7]:
        truck_table[3]["slot_{0}".format(len(truck_table[3]))] = index
        package_master.remove(int(index))
        package_info[1] = '410 S State St.'
        package_info[2] = 'Salt Lake City'
        package_info[4] = '84111'
        package_table.update(index - 1, package_info)


# nearest neighbor algorithm
# Sorts package clusters into trucks based on least distance from previously loaded packages
#  # time complexity: O(n^3) +O(n)
for package_index in range(len(package_master)):  # for every package not loaded from special conditions

    lowest_distance = 50
    best_truck = 0
    empty_truck = []

    # if truck is full of 16 packages remove from sort
    for truck_index in truck_table:  # for every truck

        if len(truck_table[truck_index]) < 17:
            empty_truck.append(truck_index)

    for truck_index in empty_truck:  # for every empty truck

        for index in range(len(truck_table[truck_index]) - 1):  # for every loaded package

            # fetch package info and distance from last package
            package_id = truck_table[truck_index]["slot_{0}".format(index + 1)]
            package_info = package_table.get(package_id - 1)
            address_id = package_info[11]

            distance = distance_table[int(package_index)][int(address_id)]

            # if distance matrix doesn't return a valid distance, flip x, y  and try again
            if distance == '':
                distance = distance_table[int(address_id)][int(package_index)]

            # if new distance is less, save for insert
            if float(distance) < lowest_distance:
                lowest_distance = float(distance)
                best_truck = truck_index

    # load closest package into empty package slot
    truck_table[best_truck]["slot_{0}".format(len(truck_table[best_truck]))] = package_master[package_index]


# Greedy algorithm
# organize packages by least distance between each stop and sets delivery time
# time complexity: O(n log(n))
# excludes sorted items, reducing complexity. Similar to heapsort
for truck_index in truck_table:  # for each truck
    current_location = 0  # start at hub

    # tester for each individual truck distance, requires line 130
    # truck_distance = 0

    for package_index in range(1, len(truck_table[truck_index])):  # for each package in truck
        lowest_distance = 100
        closest_package = 0
        closest_address = 0
        address_info = []

        for index in range(package_index - 1, len(truck_table[truck_index]) - 1):  # for every non ordered package

            # fetch package info and distance from last package
            package_id = truck_table[truck_index]["slot_{0}".format(index + 1)]
            package_info = package_table.get(package_id - 1)
            address_id = package_info[11]

            distance = distance_table[int(current_location)][int(address_id)]

            # if distance matrix doesn't return a valid distance, flip x, y  and try again
            if distance == '':
                distance = distance_table[int(address_id)][int(current_location)]

            # if new distance is less save for swap
            if float(distance) < lowest_distance:
                lowest_distance = float(distance)
                closest_package = int(index) + 1
                closest_address = address_id

        # swap package with closer package
        truck_table[truck_index]["slot_{0}".format(package_index)], truck_table[truck_index][
            "slot_{0}".format(closest_package)] = truck_table[truck_index]["slot_{0}".format(closest_package)], \
                                                  truck_table[truck_index]["slot_{0}".format(package_index)]

        # adds up truck distance
        total_distance += lowest_distance

        # tester for each individual truck distance, requires line 102
        # truck_distance += least_distance

        # sets the trucks location to the newly stored package
        current_location = closest_address

    # adds returning to hub mileage
    # print(truck_distance)
    # total_distance += float(distance_table[int(current_location)][0])

# sets each package start time and delivered time
# time complexity: O(n^2)
for truck_index in truck_table:  # for each truck

    current_location = 0  # starts at hub

    # create time tally for truck starting when it leaves the hub
    truck_time = delivery_start[truck_index - 1]
    (h, m, s) = truck_time.split(':')
    truck_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

    for package_index in range(0, len(truck_table[truck_index]) - 1):  # for each package in truck

        # fetch package info and distance from last package
        package_id = truck_table[truck_index]["slot_{0}".format(package_index + 1)]
        package_info = package_table.get(package_id - 1)
        address_id = package_info[11]

        distance = distance_table[int(current_location)][int(address_id)]

        # if distance matrix doesn't return a valid distance, flip x, y  and try again
        if distance == '':
            distance = distance_table[int(address_id)][int(current_location)]

        package_info[8] = delivery_start[truck_index - 1]

        # determines the time required to travel the calculated route, adds to tally and sets package delivery
        time = float(distance) / 18
        time_minutes = '{0:02.0f}:{1:02.0f}'.format(*divmod(time * 60, 60))
        convert_time = time_minutes + ':00'
        (h, m, s) = convert_time.split(':')
        convert_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        truck_time = truck_time + convert_time

        # updates the hash map with new delivery time
        package_info[9] = str(truck_time)
        package_table.update(int(package_id) - 1, package_info)

        current_location = address_id

# Testers

# pprint(truck_table)
# print(total_distance)
