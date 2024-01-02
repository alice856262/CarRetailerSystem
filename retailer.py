"""
Student name: Pei-Jiun Chuang
Student ID: 33624208
Creation date: 10/09/2023
Last modified date: 22/09/2023
Description: define Retailer class that represents various operations related to a retailer.
"""

import random


class Retailer:
    """
	Contains all the operations related to a retailer.
	"""

    def __init__(self, retailer_id=10000000, retailer_name=''):
        """
        Description
        -----------
        Constructs a Retailer object.

        Instance variable
        -----------------
        retailer_id : int (must be unique integer of 8 digits)
        retailer_name: string (consist of 10 alphabetic and/or white space character)
        """
        self.retailer_id = retailer_id
        self.retailer_name = retailer_name

    def __str__(self):
        """
        Description
        -----------
        Return the retailer information as a formatted string.

        Returns
        -------
        A string in the following format: "retailer_id, retailer_name".
        """
        return f'{self.retailer_id}, {self.retailer_name}'

    def generate_retailer_id(self, list_retailer):
        """
        Description
        -----------
		Generate a randomly generated unique retailer ID that is different from the existing retailer IDs and set it as the retailer_id.

		Arguments
        ---------
        list_retailer: list (a list of all existing retailer objects)
		"""
        random_id = random.randint(10000000, 99999999)
        if random_id not in list_retailer:
            self.retailer_id = random_id
            list_retailer.append(random_id)
        else:    # If the random_id is already in the list, then recursively calls the generate_retailer_id() method to generate a new one until a unique ID is found.
            self.generate_retailer_id(list_retailer)
