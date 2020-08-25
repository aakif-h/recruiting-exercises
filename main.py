from collections import OrderedDict
import unittest
from shipments import InventoryAllocator
from json import loads


class TestInventoryAllocator(unittest.TestCase):
    

    # TEST 1: the first test case listed out in the README
    def test_example_one(self):
        warehouses = [{"name":"owd", "inventory":{"apple":5, "orange":10}}, {"name":"dm", "inventory":{"banana":5, "orange":10}}]
        orders = {"apple":5, "banana":5, "orange":5}
        expected = [OrderedDict([('owd', {'apple': 5})]), OrderedDict([('dm', {'banana': 5})]), OrderedDict([('dm', {'orange': 5})])]
        
        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # TEST 2: one of the test cases from the README, basic test of when
    #         the order matches the number of items currently stocked
    def test_exact_inventory_match(self):
        warehouses = [{"name":"owd", "inventory":{"apple":1}}]
        orders = {"apple":1}
        expected = [OrderedDict([('owd', {'apple': 1})])]

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # TEST 3: one of the test cases from the README, basic test of handling
    #         "not enough items" conditions
    def test_not_enough_inventory(self):
        warehouses = [{"name":"owd", "inventory":{"apple":0}}]
        orders = {"apple":1}
        expected = []

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)

    
    # TEST 4: one of the test cases from the README, basic test of splitting a shipment
    #         across several warehouses
    def test_split_across_warehouses(self):
        warehouses = [{"name":"owd", "inventory":{"apple":5}},{"name":"dm", "inventory":{"apple":5}}]
        orders = {"apple":10}
        expected = [OrderedDict([('dm', {'apple': 5}), ('owd', {'apple': 5})])]

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)
    

    # TEST 5: check the scenario when both inputs are empty
    def test_both_empty(self):
        warehouses = []
        orders = {}
        expected = []
        
        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)
    

    # TEST 6: check the scenario when the warehouses input is empty
    def test_warehouse_empty(self):
        warehouses = []
        orders = {"apple":10}
        expected = []

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # TEST 7: test the scenario when the orders input is empty        
    def test_orders_empty(self):
        warehouses = [{"name":"owd", "inventory":{"apple":5}},{"name":"dm", "inventory":{"apple":5}}]
        orders = {}
        expected = []

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # TEST 8: a test of duplicate items in the orders map
    def test_duplicate_order(self):
        warehouses = [{"name":"owd", "inventory":{"apple":15}}]
        orders = {"apple":5,"apple":15,"apple":25,"apple":35} 
        expected = [] #  all keys inside a hashmap are unique, so there is only one entry in orders: {"apple":35}

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # TEST 9: test a large number of warehouses with overlapping orders
    def test_large_scenario(self):
        warehouses = [{"name":"a", "inventory":{"1":115, "2": 55, "3": 16, "4": 71, "5": 28}},
                      {"name":"b", "inventory":{"1": 82, "2": 34, "3": 74, "4":158, "5": 31}},
                      {"name":"c", "inventory":{"1":172, "2":114, "3": 43, "4": 84, "5":118}},
                      {"name":"d", "inventory":{"1": 15, "2":199, "3":161, "4":154, "5":154}}, 
                      {"name":"e", "inventory":{"1":114, "2": 89, "3": 15, "4":189, "5":152}},
                      {"name":"f", "inventory":{"1": 36, "2":131, "3": 84, "4":103, "5": 63}},
                      {"name":"g", "inventory":{"1": 37, "2":156, "3":133, "4": 51, "5": 34}},
                      {"name":"h", "inventory":{"1":197, "2": 75, "3": 97, "4": 44, "5": 85}},
                      {"name":"i", "inventory":{"1":189, "2":85, "3":179, "4":82, "5":122}},
                      {"name":"j", "inventory":{"1":187, "2":65, "3":78, "4":152, "5":146}}]
        orders = {"1":1000, "2": 1000, "3": 1000, "4": 1000, "5": 1000}
        expected = [OrderedDict([('a', {'1': 115}), ('b', {'1': 26}), ('c', {'1': 172}), ('e', {'1': 114}), ('h', {'1': 197}), ('i', {'1': 189}), ('j', {'1': 187})]), 
                    OrderedDict([('a', {'2': 55}), ('b', {'2': 31}), ('c', {'2': 114}), ('d', {'2': 199}), ('e', {'2': 89}), ('f', {'2': 131}), ('g', {'2': 156}), 
                                 ('h', {'2': 75}), ('i', {'2': 85}), ('j', {'2': 65})]), 
                    OrderedDict([('a', {'4': 71}), ('b', {'4': 158}), ('c', {'4': 84}), ('d', {'4': 154}), ('e', {'4': 189}), ('f', {'4': 103}), ('g', {'4': 7}), 
                                 ('i', {'4': 82}), ('j', {'4': 152})])]
        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


if __name__ == '__main__':
    while True:
        response = input("Would you like to run tests? Type 'Y' for \"Yes\" or type 'N' for \"No\": ")
        if response.upper() == 'N':
            break
        elif response.upper() == 'Y':
            response = input("Would you like to run the unit tests? Type 'Y' for \"Yes\" or type 'N' for \"No\": ")
            if response.upper() == 'N':
                warehouses = loads(input("Enter the list representation of your warehouses (with brackets): "))
                orders = loads(input("Enter the hashmap representation of your orders (with brackets): "))
                allocator = InventoryAllocator(warehouses, orders)
                print("shipments: {}".format(allocator.get_shipments()))
            elif response.upper() == 'Y':
                unittest.main()
            else:
                print("INVALID INPUT: You chose {}, but the only valid inputs are 'Y' or 'N'. Please try again.".format(response))
        else:
            print("INVALID INPUT: You chose {}, but the only valid inputs are 'Y' or 'N'. Please try again.".format(response))