"""
Student name: Pei-Jiun Chuang
Student ID: 33624208
Creation date: 10/09/2023
Last modified date: 22/09/2023
Description: define CarRetailer class that represents a car retailer and contains various methods related to car retail operations, including get car stocks and place orders.
"""

import random
import re
import time
from car import Car
from retailer import Retailer
from order import Order

pattern = r'\[\'(.*?)\'\]'

class CarRetailer(Retailer):    # Define the CarRetailer class, which inherits from the Retailer class.
	"""
	Contains all the operations related to the CarRetailer Class. This class inherits from the Retailer class.
	"""
	def __init__(self, retailer_id = 10000000, retailer_name = '', carretailer_address = '', carretailer_business_hours = (6.0, 23.0), carretailer_stock = []):
		"""
		Description
		-----------
		Constructs a CarRetailer object.

		Instance variable
		-----------------
		retailer_id : int (must be unique integer of 8 digits)
		retailer_name: string (consist of 10 alphabetic and/or white space character)
		carretailer_address: string (format: street address, state, postcode)
		carretailer_business_hours: a tuple of floats (start and end hours in 24hr, should be within the range of 6:00AM inclusive to 11:00PM inclusive)
		carretailer_stock: list (a list of available cars' car_codes from the retailer)
		"""
		super().__init__(retailer_id, retailer_name)    # super().__init__(): calls the constructor of the parent class (Retailer), it initialises the attributes inherited from the Retailer class.
		self.carretailer_address = carretailer_address
		self.carretailer_business_hours = carretailer_business_hours
		self.carretailer_stock = carretailer_stock

	def __str__(self):
		"""
        Description
        -----------
        Return the car retailer information as a formatted string.

        Returns
        -------
        A string in the following format: "retailer_id, retailer_name, carretailer_address, carretailer_business_hours, carretailer_stock".
		"""
		return f'{self.retailer_id}, {self.retailer_name}, {self.carretailer_address}, {self.carretailer_business_hours}, {self.carretailer_stock}'

	def load_current_stock(self, path = './stock.txt'):
		"""
		Description
		-----------
		Load the current stock of the car retailer according to the retailer_id from the stock.txt file and store the car_codes of the Cars in a list; this list should be saved to carretailer_stock.

		Arguments
		---------
		path: string (the path to the stock file)
		"""
		with open(path, 'r') as stock_file:
			for line in stock_file:
				retailer_id = line[0:8]    # identify retailer id in each line
				if int(retailer_id) == self.retailer_id:
					stock_car = []
					match = re.findall(pattern, line)    # 'match' is a list; 'match[0]' is a string
					for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
						stock_car.append(i)
					for i in stock_car:
						car_code = i[0:8]    # in each item, the first 8 characters are car code
						self.carretailer_stock.append(car_code)

	def is_operating(self, cur_hour):
		"""
		Description
		-----------
		Return a boolean value to indicate whether the car retailer is currently operating (i.e., within working hours).

		Arguments
		---------
		cur_hour: float (current hour in 24H format)

		Returns
		-------
		A boolean value of True or False.
		True: the car retailer is currently operating (within working hours).
		False: the car retailer is NOT operating.
		"""
		if self.carretailer_business_hours[0] <= cur_hour <= self.carretailer_business_hours[1]:
			return True
		else:
			return False

	def get_all_stock(self):
		"""
		Description
		-----------
		Returns the information of all available cars currently in stock at the car retailer.

		Returns
		-------
		stock_car: list (a list of Car objects)
		"""
		path = './stock.txt'
		with open(path, 'r') as stock_file:
			for line in stock_file:
				retailer_id = line[0:8]    # identify retailer id in each line
				if int(retailer_id) == self.retailer_id:
					stock_car = []
					match = re.findall(pattern, line)
					for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
						car_data = i.split(', ')
						car = Car(car_data[0], car_data[1], int(car_data[2]), int(car_data[3]), int(car_data[4]), car_data[5])    # create Car objects from the stock data
						stock_car.append(car)    # append Car objects to stock_car list
					return stock_car

	def get_postcode_distance(self, postcode):
		"""
		Description
		-----------
		Return the absolute difference of the postcode input by the user and that of the car retailer.

		Arguments
		---------
		postcode: int

		Returns
		-------
		difference: int (the absolute difference between the two postcodes)
		"""
		retailer_postcode = self.carretailer_address[-4:]
		difference = abs(int(postcode) - int(retailer_postcode))
		return difference

	def remove_from_stock(self, car_code):
		"""
		Description
		-----------
		Remove a car from the current stock at the car retailer. The car stock should be consistent with the stock.txt file.

		Arguments
		---------
		car_code: string (the car_code of the car to be removed)

		Returns
		-------
		A boolean value of True or False.
		True: the removal is successful.
		False: the removal is unsuccessful (car not existing in the current stock).
		"""
		if car_code in self.carretailer_stock:
			self.carretailer_stock.remove(car_code)
			#update self.stock_file
			path = './stock.txt'
			with open(path, 'r') as stock_file:
				updated_lines = []
				for line in stock_file:
					retailer_id = line[0:8]
					if int(retailer_id) == self.retailer_id:
						stock_car = []
						origin_line = line.split("['")[0]
						match = re.findall(pattern, line)
						for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
							stock_car.append(i)
						for i in stock_car:
							if car_code == i[0:8]:   # in each item, the first 8 characters are car code
								stock_car.remove(i)
						updated_line = origin_line + str(stock_car) + '\n'
						updated_lines.append(updated_line)
					else:
						updated_lines.append(line)    # The original lines already had '\n'.
			with open(path, 'w') as stock_file:
				stock_file.writelines(updated_lines)
			return True
		else:
			return False

	def add_to_stock(self, car):
		"""
		Description
		-----------
		Add a car to the current stock. The car stock should be consistent with the stock.txt file.

		Arguments
		---------
		car: object (a Car object)

		Returns
		-------
		A boolean value of True or False.
		True: the adding is successful.
		False: the adding is unsuccessful (car already existing in the current stock).
		"""
		if car.car_code not in self.carretailer_stock:
			self.carretailer_stock.append(car.car_code)
			#update self.stock_file
			path = './stock.txt'
			with open(path, 'r') as stock_file:    # Should use 'r' --> updated_lines --> 'w' (same as 'remove_from_stock()'), because it is not simply appending new lines but rather updating existing lines!!!
				updated_lines = []
				for line in stock_file:
					retailer_id = line[0:8]
					if int(retailer_id) == self.retailer_id:
						stock_car = []
						origin_line = line.split("['")[0]    # 'origin_line' extracts the part of the line that contains the retailer information.
						match = re.findall(pattern, line)
						for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
							stock_car.append(i)
						stock_car.append(str(car))
						updated_line = origin_line + str(stock_car) + '\n'
						updated_lines.append(updated_line)
					else:
						updated_lines.append(line)
			with open(path, 'w') as stock_file:
				stock_file.writelines(updated_lines)
			return True
		else:
			return False

	def get_stock_by_car_type(self, car_types):
		"""
		Description
		-----------
		Return the list of cars in the current stock by specific car_type values.

		Arguments
		---------
		car_types: list (a list of car_type values of the cars to be fetched)

		Returns
		-------
		stock_type_car: list (a list of Car objects)
		"""
		path = './stock.txt'
		with open(path, 'r') as stock_file:
			for line in stock_file:
				retailer_id = line[0:8]    # identify retailer id in each line
				if int(retailer_id) == self.retailer_id:
					stock_type_car = []
					match = re.findall(pattern, line)
					for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
						car_data = i.split(', ')
						car = Car(car_data[0], car_data[1], int(car_data[2]), int(car_data[3]), int(car_data[4]), car_data[5])
						for type in car_types:
							if car.get_car_type() == type:
								stock_type_car.append(car)
		return stock_type_car

	def get_stock_by_licence_type(self, licence_type):
		"""
		Description
		-----------
		Return the list of cars in the current stock that are not forbidden by the driver's licence type.

		Arguments
		---------
		licence_type: string ("L" (Learner Licence), "P" (Probationary Licence), or "Full" (Full Licence))

		Returns
		-------
		stock_licence_car: list (a list of Car objects)
		"""
		path = './stock.txt'
		with open(path, 'r') as stock_file:
			for line in stock_file:
				retailer_id = line[0:8]    # identify retailer id in each line
				if int(retailer_id) == self.retailer_id:
					stock_licence_car = []
					match = re.findall(pattern, line)
					for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
						car_data = i.split(', ')
						car = Car(car_data[0], car_data[1], int(car_data[2]), int(car_data[3]), int(car_data[4]), car_data[5])
						if licence_type == 'L' or licence_type == 'FULL':
							stock_licence_car.append(car)
						# The current regulation only forbids certain cars for probationary licence.
						elif licence_type == 'P':
							if car.probationary_licence_prohibited_vehicle() is False:
								stock_licence_car.append(car)
		return stock_licence_car

	def car_recommendation(self):
		"""
		Description
		-----------
		Return a car that is randomly selected from the cars in stock at the current car retailer.

		Returns
		-------
		random_car: object (a Car object)
		"""
		stock_car = self.get_all_stock()
		random_car = random.choice(stock_car)
		return random_car

	def create_order(self, car_code):
		"""
		Description
		-----------
		Return an order object of a created order. When an order is created, the car needs to be removed from the current stock of the car retailer. Such updates are reflected in "stock.txt" and "order.txt".

		Arguments
		---------
		car_code: string (the car_code of the car to be ordered)

		Returns
		-------
		order: object (an Order object)
		"""
		creation_time = int(time.time())
		path_order = './order.txt'
		with open(path_order, 'r') as order_file:
			order_id_list = []
			for line in order_file:
				each_order = line.split(', ')
				order_id_list.append(each_order[0])
			order = Order(order_creation_time = creation_time)
			new_order_id = order.generate_order_id(car_code)
			if new_order_id not in order_id_list:    # Check if the new order ID is not already in the order_id_list.
				order.order_id = new_order_id
				order_id_list.append(new_order_id)
				path = './stock.txt'
				with open(path, 'r') as stock_file:
					for line in stock_file:
						origin_line = line.split("['")[0]
						match = re.findall(pattern, line)
						for i in match[0].split("', '"):    # identify car stocks info (originally stored as a list in each line)
							if car_code == i[0:8]:    # in each item, the first 8 characters are car code
								car_data = i.split(', ')
								order_car = Car(car_data[0], car_data[1], int(car_data[2]), int(car_data[3]), int(car_data[4]), car_data[5])
								retailer_data = origin_line.split(', ')
								order_retailer = Retailer(retailer_data[0], retailer_data[1])
								order = Order(order_id = new_order_id, order_car = order_car, order_retailer = order_retailer, order_creation_time = creation_time)
		remove_result = self.remove_from_stock(car_code)
		if remove_result:
			with open(path_order, 'a') as order_file:
				updated_line = str(order) + '\n'
				order_file.write(updated_line)
		return order
