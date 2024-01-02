"""
Student name: Pei-Jiun Chuang
Student ID: 33624208
Creation date: 10/09/2023
Last modified date: 02/01/2024
Description: implement and simulate a simple car retailer system, including menu display, test data generation, user inputs, and program logic handling.
"""

import random
import re
import time
from car import Car
from retailer import Retailer
from car_retailer import CarRetailer


def main_menu():
    """
    Description
    -----------
    Display all available operations for users to choose from.
    """
    print('========== Main Menu ==========')
    menu = ['a. Find the nearest car retailer', 'b. Get car purchase advice', 'c. Place a car order', 'd. Exit']
    for option in menu:
        print(option)


def generate_test_data():
    """
    Description
    -----------
    Generate test data for the program, including a total of 12 cars and 3 retailers (each retailer with 4 cars in their stock).
    """
    list_retailer = []
    list_stock = []
    for i in range(3):
        # Generate retailer information.
        retailer = Retailer()
        retailer.generate_retailer_id(list_retailer)
        retailer_name = ''
        for i in range(10):
            retailer_name += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ')
        address_street = ['George Street', 'William Street', 'Church Street', 'High Street', 'King Street', 'Elizabeth Street', 'Victoria Street', 'Queen Street', 'Bridge Road', 'Clayton Road', 'Camberwell Road', 'Wellington Road', 'Burwood Road', 'Station Road', 'Carrington Road']
        address_suburb = ['Carlton', 'Brighton', 'Richmond', 'Arlington', 'Centerville', 'Georgetown', 'Springfield', 'Greenville', 'Newtowns', 'Hamiltons']
        carretailer_address = random.choice(address_street) + ' ' + random.choice(address_suburb) + ', '
        for i in range(3):    # Generate a random state name.
            carretailer_address += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # random.uniform(a, b): generate a random floating-point number between a (inclusive) and b (inclusive).
        # random.randint(a, b): generate a random integer between specified integers, a (inclusive) and b (inclusive).
        # random.choice(sequence): choose a random element from a sequence (can be list, tuple, or string).
        carretailer_address += ' ' + str(random.randint(1000, 9999))    # Should use random.randint(1000, 9999).
        open_business_hours = round(random.uniform(6.0, 23.0), 1)
        close_business_hours = round(random.uniform(open_business_hours, 23.0), 1)
        car_retailer = CarRetailer(retailer.retailer_id, retailer_name, carretailer_address)
        car_retailer.carretailer_business_hours = (open_business_hours, close_business_hours)
        list_car = []
        list_car_code = []
        for i in range(4):
            # Generate car information.
            car_code = ''
            for num in range(2):
                car_code += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            for num in range(6):
                car_code += random.choice('0123456789')
            car_name = ''
            for i in range(10):
                car_name += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
            car_capacity = random.randint(2, 30)
            car_horsepower = random.randint(50, 1000)
            car_weight = random.randint(1000, 8000)
            car_type = random.choice(['FWD', 'RWD', 'AWD'])    # can be either list or tuple
            car = Car(car_code, car_name, car_capacity, car_horsepower, car_weight, car_type)
            car_retailer.add_to_stock(car)
            list_car.append(str(car))
            list_car_code.append(car_code)
        car_retailer.carretailer_stock = list_car    # Should be a list of 'car_code', not car objects. Here just temporarily make 'carretailer_stock' as a list of 'Car objects' in order to write stock.txt.
        list_stock.append(str(car_retailer))
        car_retailer.carretailer_stock = list_car_code    # Should be a list of 'car_code', not car objects. Now change 'carretailer_stock' as a list of 'car_code'.
    with open('./stock.txt', 'w') as stock_file:
        for stock in list_stock:
            stock_file.write(stock + '\n')
    with open('./order.txt', 'w') as order_file:
        order_file.truncate(0)    # truncate(0): resize the file to the given size (in bytes), if size = 0 means clearing the contents of the file, making it empty.


def main():
    """
    Description
    -----------
    Handle all program logic, including user input, calling methods from objects and handling validations.
    """
    generate_test_data()
    list_car_retailer = []    # Maintain a list of all existing CarRetailer 'objects'.
    path = './stock.txt'
    with open(path, 'r') as stock_file:
        for line in stock_file:
            retailer_id = int(line.split(', ')[0])
            retailer_name = line.split(', ')[1]
            carretailer_address = line.split(', ')[2] + ', ' + line.split(', ')[3]
            carretailer_business_hours = (float(line.split(', ')[4][1:]), float(line.split(', ')[5][:-1]))
            carretailer = CarRetailer(retailer_id, retailer_name, carretailer_address, carretailer_business_hours)
            carretailer.carretailer_stock = []
            carretailer.load_current_stock(path)
            list_car_retailer.append(carretailer)

    while True:
        try:
            main_menu()
            choice = input('Please select an option ( a / b / c / d ): ').lower()
            if choice == 'a':
                # Functionality 3
                while True:
                    try:
                        user_postcode = int(input('Please enter a 4-digit postcode: '))
                        if user_postcode < 1000 or user_postcode > 9999:
                            raise ValueError('Please enter a valid 4-digit postcode.')    # If invalid, a ValueError exception is raised and this will trigger the code to jump to the except block.
                        min_distance = list_car_retailer[0].get_postcode_distance(user_postcode)    # Calculate the distance between the user-provided postcode and the postcode of the first retailer in the list.
                        car_retailer = list_car_retailer[0]    # Assume that the first retailer in the list (list_car_retailer[0]) is the nearest one.
                        for i in list_car_retailer:
                            if i.get_postcode_distance(user_postcode) < min_distance:    # Calculate the distance between the user-provided postcode and the postcode of the current retailer (i).
                                min_distance = i.get_postcode_distance(user_postcode)    # If the current retailer is closer, it updates min_distance and sets car_retailer to the current retailer.
                                car_retailer = i
                        print(f'The nearest car retailer no.{car_retailer.retailer_id} is called "{car_retailer.retailer_name}". The address is {car_retailer.carretailer_address}.\n')
                        break
                    except ValueError as e:
                        print('Invalid: Please enter a valid 4-digit postcode.')
            elif choice == 'b':
                # Functionality 4
                # List all the available car retailers and prompt the users to select one to continue the advising process
                for i in list_car_retailer:
                    print(f'The car retailer no.{i.retailer_id} is called {i.retailer_name}, and the address is {i.carretailer_address}.')
                print()
                while True:
                    try:
                        user_retailer = int(input('Please enter a car retailer number (ID): '))
                        list_retailer_id = []
                        for i in list_car_retailer:    # 'i' is 'each CarRetailer object'
                            list_retailer_id.append(i.retailer_id)    # Create a list of all retailer IDs available in 'list_car_retailer'.
                        if user_retailer not in list_retailer_id:
                            raise ValueError('Please enter a valid car retailer number (ID).')
                        break
                    except ValueError as e:
                        print('Invalid: Please enter a valid car retailer number (ID).')
                # Show sub-menu
                print('\n========== Sub-Menu ==========')
                submenu = ['1. Recommend a car', '2. Get all cars in stock', '3. Get cars in stock by car types',
                           '4. Get probationary licence permitted cars in stock', '5. Back to main menu']
                for option in submenu:
                    print(option)
                while True:
                    try:
                        subchoice = input('\nPlease select an option ( 1 / 2 / 3 / 4 / 5 ): ')
                        # Randomly select one car from the current stock of the car retailer.
                        if subchoice == '1':
                            for i in list_car_retailer:    # 'i' is 'each CarRetailer object'
                                if user_retailer == i.retailer_id:
                                    random_car = i.car_recommendation()
                                    print(f'Car no.{random_car.car_code} name {random_car.car_name}, with {random_car.car_capacity} seats and {random_car.car_horsepower} horsepower, is a {random_car.car_weight} kilogram {random_car.car_type} type car.')
                            break
                        # Show all the stocks of a car retailer
                        elif subchoice == '2':
                            for i in list_car_retailer:
                                if user_retailer == i.retailer_id:
                                    list_all_stock = i.get_all_stock()    # 'get_all_stock()' returns a list of Car objects.
                                    for car in list_all_stock:
                                        print(f'Car no.{car.car_code} name {car.car_name}, with {car.car_capacity} seats and {car.car_horsepower} horsepower, is a {car.car_weight} kilogram {car.car_type} type car.')
                            break
                        # Show the current stock of specific car type(s)
                        elif subchoice == '3':
                            while True:
                                try:
                                    user_type = input('Please choose car type(s): FWD / RWD / AWD (use white space to seperate if enter more than one car type): ').split()
                                    for i in user_type:
                                        if i not in ['FWD', 'RWD', 'AWD']:
                                            raise ValueError('Please select valid car type(s).')
                                    for i in list_car_retailer:
                                        if user_retailer == i.retailer_id:
                                            list_type_stock = i.get_stock_by_car_type(list(set(user_type)))    # 'get_stock_by_car_type()' returns a list of Car objects.
                                            if list_type_stock == []:
                                                for i in user_type:
                                                    print(f'Sorry! There is no {i} type car in this retailer.')
                                            for car in list_type_stock:
                                                print(f'Car no.{car.car_code} name {car.car_name}, with {car.car_capacity} seats and {car.car_horsepower} horsepower, is a {car.car_weight} kilogram {car.car_type} type car.')
                                    break
                                except ValueError as e:
                                    print(f'Invalid: {e}')
                        # Show the current stock of specific licence type
                        elif subchoice == '4':
                            while True:
                                try:
                                    user_licence = input('Please choose a licence type ( Full / L / P ): ').upper()
                                    if user_licence != 'FULL' and user_licence != 'L' and user_licence != 'P':
                                        raise ValueError('Please select a valid licence type.')
                                    for i in list_car_retailer:
                                        if user_retailer == i.retailer_id:
                                            list_licence_stock = i.get_stock_by_licence_type(user_licence)    # 'get_stock_by_licence_type()' returns a list of Car objects.
                                            if list_licence_stock == []:
                                                print(f'Sorry! There is no {user_licence} licence type car in this retailer.')
                                            for car in list_licence_stock:
                                                print(f'Car no.{car.car_code} name {car.car_name}, with {car.car_capacity} seats and {car.car_horsepower} horsepower, is a {car.car_weight} kilogram {car.car_type} type car.')
                                    break
                                except ValueError as e:
                                    print(f'Invalid: {e}')
                        elif subchoice == '5':
                            break
                    except ValueError as e:
                        print('Invalid choice. Please select a valid option: 1 / 2 / 3 / 4 / 5.')
            elif choice == 'c':
                # Functionality 5
                for car_retailer in list_car_retailer:
                    print(f'The car retailer no.{car_retailer.retailer_id} is called "{car_retailer.retailer_name}". The address is {car_retailer.carretailer_address}.')
                    # show business_hours to users
                    open_business_hours = int(car_retailer.carretailer_business_hours[0])
                    open_business_minutes = int((car_retailer.carretailer_business_hours[0] - open_business_hours) * 60)
                    close_business_hours = int(car_retailer.carretailer_business_hours[1])
                    close_business_minutes = int((car_retailer.carretailer_business_hours[1] - close_business_hours) * 60)
                    print(f'Business hour: from {open_business_hours:02d}:{open_business_minutes:02d} to {close_business_hours:02d}:{close_business_minutes:02d}')
                    for i in car_retailer.carretailer_stock:
                        print(f'The car stock in this retailer: car no.{i}')
                    print()
                while True:
                    try:
                        user_retailer_car = input('Please choose a car retailer number (ID) and car code (ID), separated by a white space: ').split()
                        if len(user_retailer_car) != 2:
                            raise ValueError('Please choose a car retailer number (ID) and car code (ID).')
                        user_retailer = int(user_retailer_car[0])
                        list_retailer_id = []
                        for i in list_car_retailer:
                            list_retailer_id.append(i.retailer_id)    # Create a list of all retailer IDs available in 'list_car_retailer'.
                        if user_retailer not in list_retailer_id:
                            raise ValueError('Please choose a valid car retailer number (ID).')
                        user_car = user_retailer_car[1]
                        for i in list_car_retailer:
                            if user_retailer == i.retailer_id:
                                car_retailer = i    # Identify the CarRetailer object which matches the user input retailer ID.
                        list_stock_code = car_retailer.carretailer_stock
                        if user_car not in list_stock_code:
                            raise ValueError('Please choose a valid car code (ID).')
                        cur_hour = ((int(time.time()) % 86400) / 3600) + 10    # Unix timestamp 0 = midnight (00:00 UTC+0) on 1 January 1970
                        is_open = car_retailer.is_operating(cur_hour)
                        print('You are placing an order of car no.', user_car, 'from retailer no.', user_retailer, '...')
                        if is_open:
                            new_order = car_retailer.create_order(user_car)
                            print(f'Congratulation! Your order ID is {new_order.order_id}.')
                            print(f'You have successfully placed an order for the car no.{new_order.order_car.car_code} from the retailer "{new_order.order_retailer.retailer_name}" (no.{new_order.order_retailer.retailer_id}).\n')
                        else:
                            print('Sorry! The retailer is closed now.\n')
                        break
                    except ValueError as e:
                        print(f'Invalid: {e}')
            elif choice == 'd':
                print('Goodbye!')
                break
        except ValueError as e:
            print('Invalid choice. Please select a valid option.')


if __name__ == "__main__":
    main()
