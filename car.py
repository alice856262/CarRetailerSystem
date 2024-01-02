"""
Student name: Pei-Jiun Chuang
Student ID: 33624208
Creation date: 10/09/2023
Last modified date: 22/09/2023
Description: define Car class that represents various operations related to a car.
"""

class Car:
    """
    Contains all the operations related to a car.
    """
    def __init__(self, car_code = '', car_name = '', car_capacity = 1, car_horsepower = 1, car_weight = 1, car_type = ''):
        """
        Description
        -----------
        Constructs a car object.

        Instance variable
        -----------------
        car_code : string (must be unique and in the format of 2 uppercase letters plus 6 digits)
        car_name: string (consist of 10 alphabetic characters)
        car_capacity: int (maximum seating capacity, ranging from 2 to 30)
        car_horsepower: int (in kilowatts, ranging from 50 to 1000)
        car_weight: int (in kilograms, ranging from 1000 to 8000, and must not be zero)
        car_type: string (should be one of 'FWD', 'RWD' or 'AWD')
        """
        self.car_code = car_code    # Assign the values of the constructor parameters to the instance variables of the Car object being created ('self').
        self.car_name = car_name
        self.car_capacity = car_capacity
        self.car_horsepower = car_horsepower
        self.car_weight = car_weight
        self.car_type = car_type

    def __str__(self):    # Use str() or print() function on a Car object to call this method.
        """
        Description
        -----------
        Return the unit information as a formatted string.

        Returns
        -------
        A string in the following format: "car_code, car_name, car_capacity, car_horsepower, car_weight, car_type".
        """
        return f'{self.car_code}, {self.car_name}, {self.car_capacity}, {self.car_horsepower}, {self.car_weight}, {self.car_type}'

    def probationary_licence_prohibited_vehicle(self):
        """
        Description
        -----------
        Return whether the vehicle is a prohibited vehicle for probationary licence drivers.

        Returns
        -------
        A boolean value of True or False.
        True: the vehicle is a prohibited vehicle for probationary licence drivers.
        False: the vehicle is NOT a prohibited vehicle for probationary licence drivers.
        """
        # The formula to calculate the Power to Mass ratio is: RoundUp (Power / Weight) * 1000, three decimal places should be retained.
        power_mass_ratio = round((self.car_horsepower / self.car_weight), 3) * 1000
        if power_mass_ratio > 130:
            return True
        else:
            return False

    def found_matching_car(self, car_code):    # May be used in the 'create_order()' function in CarRetailer class.
        """
        Description
        -----------
        Return whether the current vehicle is the one to be found based on a car_code.

        Arguments
        ---------
        car_code: string (the car_code of the car to be searched)

        Returns
        -------
        A boolean value of True or False.
        True: the car_code matches the current car's car_code.
        False: the car_code does NOT match the current car's car_code.
        """
        if car_code == self.car_code:
            return True
        else:
            return False

    def get_car_type(self):
        """
        Description
        -----------
        Return the car_type of the current car.

        Returns
        -------
        A string value of the car_type.
        """
        return str(self.car_type)
