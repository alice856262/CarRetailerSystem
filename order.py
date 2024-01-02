"""
Student name: Pei-Jiun Chuang
Student ID: 33624208
Creation date: 10/09/2023
Last modified date: 22/09/2023
Description: define Order class that represents various operations related to an order.
"""

import random
import time
from car import Car    # Import the Car class from a module named car.
from retailer import Retailer   # Import the Retailer class from a module named retailer.

class Order:
	"""
	Contains all the operations related to an order.
	"""
	def __init__(self, order_id = '', order_car = Car(), order_retailer = Retailer(), order_creation_time = int(time.time())):
		"""
		Description
		-----------
		Constructs an order object.

		Instance variable
		-----------------
		order_id : string (must be unique)
		order_car: object (the Car object related to this order)    # default is a new Car object
		order_retailer: object (the Retailer object related to this order)    # default is a new Retailer object
		order_creation_time: int (the UNIX timestamp of the order creation)    # default is the current timestamp, using int(time.time()))
		"""
		self.order_id = order_id
		self.order_car = order_car
		self.order_retailer = order_retailer
		self.order_creation_time = order_creation_time


	def __str__(self):
		"""
		Description
		-----------
		Return the order information as a formatted string.

		Returns
		-------
		A string in the following format: "order_id, order_car.car_code, order_retailer.retailer_id, order_creation_time".
		"""
		return f'{self.order_id}, {self.order_car.car_code}, {self.order_retailer.retailer_id}, {self.order_creation_time}'

	def generate_order_id(self, car_code):
		"""
		Description
		-----------
		Return a unique order ID.

		Arguments
		---------
		car_code: string (the car_code related to the current order)

		Returns
		-------
		order_id: string (a unique string representing the order ID)
		"""
		random_string = ''    # This will be used in Step 1
		modified_string = ''    # This will be used in Step 2
		correspond_str_1 = ''    # This will be used in Step 5
		str_1 = '~!@#$%^&*'
		len_str_1 = len('~!@#$%^&*')
		# Step 1: generate a random string of 6 lowercase alphabetic characters.
		for i in range(6):
			random_string += random.choice('abcdefghijklmnopqrstuvwxyz')
		# Step 2: convert every second character to uppercase.
		for index, char in enumerate(random_string):    # The enumerate() function can get both the character (char) and its index (index) in the string.
			if index % 2 == 1:    # Check if the current index is odd (= every second character).
				modified_string += char.upper()
			else:
				modified_string += char
		# Step 3: get the ASCII code of each character.
		for char in modified_string:
			# Step 4: calculate ASCII code to the power of 2 and get the remainder.
			code = ord(char)    # Obtain the ASCII code (integer) of the current char using ord() function.
			remainder = (int(code) ** 2) % len_str_1
			# Step 5: use the remainder as an index to obtain characters from str_1.
			correspond_str_1 += str_1[remainder]    # The remainder is used as an index to access a char from str_1, and then appended to correspond_str_1.
		# Step 6: append each character from Step 5 for n times.
		for index, char in enumerate(correspond_str_1):    # The enumerate() function can get both the character (char) and its index (index) in the string.
			modified_string += char * index
		# Step 7: append the car_code and the order creation time.
		order_id = f'{modified_string}{car_code}{self.order_creation_time}'
		return order_id
