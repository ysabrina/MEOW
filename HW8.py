# Your name: Sabrina Yu
# Your student id: ysabrina
# Your email: ysabrina@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    outerdicty = {}
    sourcedir_meow = os.path.dirname(__file__)
    path_meow = os.path.join(sourcedir_meow, db)
    con = sqlite3.connect(path_meow)

    cur = con.cursor()

    cur.execute("""SELECT restaurants.name, categories.category, buildings.building, restaurants.rating
        FROM restaurants
        JOIN buildings ON buildings.id = restaurants.building_id
        JOIN categories ON categories.id = restaurants.category_id""")
    
    variable_meow = cur.fetchall()

    for x in variable_meow:
        meowy = list(x)
        innerdicty = {}
        name = meowy[0]
        genre = meowy[1]
        building = meowy[2]
        rating = meowy[3]

        innerdicty['category'] = genre
        innerdicty['building'] = building
        innerdicty['rating'] = rating
        outerdicty[name] = innerdicty 

    con.close()

    return outerdicty

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    sourcedir_meow = os.path.dirname(__file__)
    path_meow = os.path.join(sourcedir_meow, db)
    con = sqlite3.connect(db)

    cur = con.cursor()

    cur.execute("""SELECT categories.category, COUNT(restaurants.category_id)
        FROM restaurants
        JOIN categories ON categories.id = restaurants.category_id
        GROUP BY category""")
    
    variable_meow = cur.fetchall() #i like naming my variables silly things they will all be meow today :)
    dicty = dict(variable_meow)
    better_dicty = dict(sorted(dicty.items(), key = lambda t: t[1], reverse = True))
    #print(better_dicty)

    keyz = list(better_dicty.keys())
    valuez = list(better_dicty.values())

    plt.figure(figsize = (25,8))
    plt.bar(keyz,valuez)
    plt.title("Types of Restaurant on S University Ave")
    plt.xlabel("# of Restaurants") 
    plt.ylabel("Restaurant Categories")
    
    #print(better_dicty)    
    plt.show()

    return dicty

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    dictypoo = {}
    sourcedir_meow = os.path.dirname(__file__)
    path_meow = os.path.join(sourcedir_meow, db)
    con = sqlite3.connect(db)

    cur = con.cursor()

    cur.execute("""SELECT buildings.building, restaurants.name, restaurants.rating 
        FROM restaurants 
        JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = ?""", (building_num,))

    variable_meow = cur.fetchall()

    for x in variable_meow:
        rating = x[2]
        name = x[1]
        dictypoo[rating] = name
        
    newdictypoo = dict(sorted(dictypoo.items(), reverse = True))
    valuez_list = list(newdictypoo.values()) #<-- names of the restaurants

    return valuez_list

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    load_rest_data("South_U_Restaurants.db")
    plot_rest_categories("South_U_Restaurants.db")
    find_rest_in_building(1140,"South_U_Restaurants.db")

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    #def test_get_highest_rating(self):
        #highest_rating = get_highest_rating('South_U_Restaurants.db')
        #self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
