from collections import OrderedDict

class InventoryAllocator:
    def __init__(self, warehouses, orders):
        self.warehouses = warehouses
        self.catalog = self.process_catalog(self.warehouses)
        self.orders = orders
    
    
    # worst case time complexity: O(N*M) 
    # worst case space complexity: O(M)
    # where N = number of warehouses and M = number of items
    #
    # input: warehouses -> a list of dicts
    # output: catalog -> a dict with info of all items stocked across warehouses (basically, one big warehouse)
    def process_catalog(self, warehouses):
        catalog = {}

        # each entry (warehouse) in warehouses is a dict, with the following fields:
        # "name" -> the name of the warehouse
        # "inventory" -> the item and count inside the warehouse
        for warehouse in warehouses:
            for item in warehouse["inventory"]:
                if item in catalog:
                    catalog[item] += warehouse["inventory"][item]
                else:
                    catalog[item] = warehouse["inventory"][item]
        
        # reiterate over each warehouse to fill in items that are present in catalog, but are absent in the warehouse
        # NOTE: this loop is relevant for the edge cases in the process_shipments() function
        for warehouse in warehouses:
            for item in catalog:
                if not item in warehouse["inventory"]:
                    warehouse["inventory"][item] = 0
        return catalog


    # this function finds the optimal shipments for each order requested by the user
    # time complexity: O(M*NlogN)
    # space complexity: O(N*M)
    # where N = number of warehouses and M = number of items
    #
    # input: None
    # output: shipments -> a list of OrderedDicts with each representing the most optimal shipment for a given order
    def get_shipments(self):

        shipments = []

        n = len(self.warehouses)

        # in the case that there are no warehouses, we cannot get any shipments, so
        # return an empty list, as defined by the coding challenge criteria
        if not n:
            return []

        # check all the different types of orders
        for item in self.orders.keys():
            # edge cases:
            # 1. if the item is not in the warehouse, then don't bother checking the warehouses
            # 2. if the current stock of the item is less than the requested order, the shipment cannot be fulfilled
            # 3. if there is no requested amount of an item (relevant: otherwise would return [OrderedDict()])
            if not item in self.catalog or self.catalog[item] < self.orders[item] or self.orders[item] == 0:
                continue

            # sort the warehouses by the biggest stock of the current order item, from biggest to smallest
            self.warehouses.sort(key = lambda w: w["inventory"][item], reverse=True)
            retrieval_amount = self.orders[item]
            
            # iterate through all the warehouses to find the most optimal combinations of warehouses 
            # for the requested retrieval amount
            i = 0
            shipment = {}
            while retrieval_amount > 0:
                if self.warehouses[i]["inventory"][item] != 0:
                    removal_amount = min(self.warehouses[i]["inventory"][item], retrieval_amount)
                    retrieval_amount -= removal_amount
                    self.warehouses[i]["inventory"][item] -= removal_amount
                    self.catalog[item] -= removal_amount
                    shipment[self.warehouses[i]["name"]] = {item: removal_amount}
                i += 1
            
            # use ordered dict to preserve the lexicographical order
            shipments.append(OrderedDict(sorted(shipment.items())))
        
        return shipments