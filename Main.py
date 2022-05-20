# WGU C950 Data Structures and Algorithms II
# Ryan Barnes
# Student ID: 000970605

import datetime
from Delivery import total_distance
from Delivery import package_table
from Packages import amount_of_packages


class Main:
    #  Declares user input variables
    package_range = 0
    user_timestamp = 0
    user_input = 0

    # Beginning of console menu, displays name and mile total
    print("Western Governors University Postal Service's package tracking system")
    print('Estimated distance for deliveries is', total_distance.__round__(2), 'miles')

    # checks for user ending the program with 'exit'
    while user_input != 'exit':  # until program stopped

        # defines and resets the start of package range for printing
        package_index = 1

        # Formatting space
        print()

        # request time input and informs user of 'exit' command
        print("Type 'exit' to end the program at any time")

        # checks for user ending the program with 'exit' or runs loop until valid timestamp\command is given
        while user_input != 'exit':

            # request for console input for timestamp
            print("Enter a time in hh:mm:ss format to view a specific time, 'complete' to view the finished route")
            user_input = input('Time: ')

            # sets timestamp to last second of the day to few the completed routes
            if user_input == 'complete':
                user_timestamp = '23:59:59'
                (h, m, s) = user_timestamp.split(':')
                user_timestamp = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                break  # with a valid input end the while loop

            # checks the users input for valid timestamp
            else:

                # tries to convert user input into a date time
                try:
                    (h, m, s) = user_input.split(':')
                    user_timestamp = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    break  # with a valid input end the while loop

                # if not valid request new input
                except ValueError:
                    if user_input == 'exit':
                        exit()
                    print('Invalid Input, please enter again')

        # checks for user ending the program with 'exit' or runs loop until valid package\command is given
        while user_input != 'exit':  # until valid package input

            # request for console input for package id
            print("Enter a package ID or 'complete' to see all packages")
            user_input = input('Package ID: ')

            # set range to view all packages if user types 'complete'
            if user_input == 'complete':
                package_range = amount_of_packages + 1
                break  # with a valid input end the while loop

            # checks if the user input is between 1 and 40, if not request new input
            elif not 1 <= int(user_input) <= amount_of_packages:
                if user_input == 'exit':
                    exit()
                print('Invalid Input, please enter again')

            # sets range to view specified package
            else:
                package_index = int(user_input)
                package_range = int(user_input) + 1
                break  # with a valid input end the while loop

        # outputs package information filtered by user input
        while package_index < package_range:  # until all packages in range displayed

            # gets a single package's information
            # then converts the delivery value to a date time value for comparision to user timestamp
            package_info = package_table.get(package_index - 1)
            delivery_time = package_info[9]
            (h, m, s) = delivery_time.split(':')
            delivery_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            # checks if package has been delivered against user timestamp and set status

            # if package has not been delivered yet, set status to 'in transit'
            if user_timestamp < delivery_time:
                status = 'In Transit'

            # if package has been delivered, set status to 'delivered'
            else:
                status = 'Delivered'

            # formatted output to make reading the requested information easier
            # outputs: package Id, delivery address, deadline, status and time it will be delivered
            print("ID:% 3d% 40s%   15s   Status: %   10s   Delivered by: % 7s " % (
                package_index, package_info[1], package_info[5], status, delivery_time))

            # iterates loop
            package_index += 1

        # reruns the program if 'exit' is not typed
        user_input = input("Type 'exit' or hit enter to search again")
