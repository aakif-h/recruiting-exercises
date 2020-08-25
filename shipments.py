from collections import OrderedDict

class InventoryAllocator:
    def __init__(self, warehouses, orders):
        self.warehouses = warehouses
        self.catalog = self.process_catalog(self.warehouses)
        self.orders = orders
    
    
    # worst case time complexity: O(N*M) 
    # worst case space complexity: O(M)
    # where N = number of warehouses and M = number of items
    def process_catalog(self, warehouses):
        catalog = {}
        for warehouse in warehouses:
            for item in warehouse["inventory"]:
                if item in catalog:
                    catalog[item] += warehouse["inventory"][item]
                else:
                    catalog[item] = warehouse["inventory"][item]
        for warehouse in warehouses:
            for item in catalog:
                if not item in warehouse["inventory"]:
                    warehouse["inventory"][item] = 0
        return catalog


    def get_shipments(self):
        shipments = []
        n = len(self.warehouses)
        # in the case that there are no warehouses, we cannot get any shipments, so just
        # return an empty list, as defined by the coding challenge criteria
        if not n:
            return []

        for item in self.orders.keys():
            if self.catalog[item] < self.orders[item] or self.orders[item] == 0:
                continue
            self.warehouses.sort(key = lambda w: w["inventory"][item], reverse=True)
            retrieval_amount = self.orders[item]
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
            shipments.append(OrderedDict(sorted(shipment.items())))
        return shipments