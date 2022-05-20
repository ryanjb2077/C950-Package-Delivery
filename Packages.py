import csv
from pprint import pprint
from Hash_Table import Hash_Map

# Creates nested dictionary of address locations from file
with open('Data/WGUPS_Address_File.csv', newline='') as address_file:
    cvs_address_list = csv.DictReader(address_file, delimiter=',')
    address_table = {}

    for row in cvs_address_list:

        name = row['address_id']
        del row['address_id']
        address_table[name] = dict(row)

# reads package information and loads into the hash map
with open('Data/WGUPS_Package_File.csv', newline='') as package_file:
    cvs_package_list = csv.reader(package_file, delimiter=',')

    package_table = Hash_Map()  # creates the hash table for package data storage

    # adds all the package data into a list
    for row in cvs_package_list: # for every line in the package fill

        package_id = row[0]
        address = row[1]
        city = row[2]
        state = row[3]
        postal = row[4]
        delivery_deadline = row[5]
        weight = row[6]
        special_instruction = row[7]
        delivery_time_start = ''
        delivery_time_end = ''
        delivery_status = ''
        address_id = ''

        value = [package_id, address, city, state, postal, delivery_deadline, weight, special_instruction,
                 delivery_time_start, delivery_time_end, delivery_status, address_id]

        package_table.insert_value(int(package_id) - 1, value)

# global package amount for iteration
    amount_of_packages = int(package_id)

    # Adds address id of delivery location to each package(foreign key)
for package_index in range(40):

    package_info = package_table.get(package_index)

    for address_index in address_table:

        if package_info[1] == address_table[address_index]['address']:
            package_info[11] = address_index
            package_table.update(package_index, package_info)
            break


# tester
# pprint(address_table)
