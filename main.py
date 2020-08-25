from json import loads
from collections import OrderedDict
import unittest
from shipments import InventoryAllocator



class TestInventoryAllocator(unittest.TestCase):
    

    # the first test case listed out in the README
    def test_example_one(self):
        warehouses = [{"name":"owd", "inventory":{"apple":5, "orange":10}}, {"name":"dm", "inventory":{"banana":5, "orange":10}}]
        orders = {"apple":5, "banana":5, "orange":5}
        expected = [OrderedDict([('owd', {'orange': 5})]), OrderedDict([('owd', {'apple': 5})]), OrderedDict([('dm', {'banana': 5})])]
        
        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # one of the test cases from the README, this test case checks to see 
    def test_exact_inventory_match(self):
        warehouses = [{"name":"owd", "inventory":{"apple":1}}]
        orders = {"apple":1}
        expected = [OrderedDict([('owd', {'apple': 1})])]

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)


    # one of the test cases from the README, 
    def test_not_enough_inventory(self):
        warehouses = [{"name":"owd", "inventory":{"apple":0}}]
        orders = {"apple":1}
        expected = []

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)

    
    # one of the test cases from the README, 
    def test_split_across_warehouses(self):
        warehouses = [{"name":"owd", "inventory":{"apple":5}},{"name":"dm", "inventory":{"apple":5}}]
        orders = {"apple":10}
        expected = [OrderedDict([('dm', {'apple': 5}), ('owd', {'apple': 5})])]

        allocator = InventoryAllocator(warehouses, orders)
        self.assertEqual(allocator.get_shipments(), expected)
    


if __name__ == '__main__':
    unittest.main()

