from collections import OrderedDict


class InventoryAllocator:
    def __init__(self, warehouses, orders):
        self.warehouses = warehouses
        self.catalog = self.process_catalog(self.warehouses)
        self.orders = orders
    
    
    # worst case time complexity: O(n*m) 
    # worst case space complexity: O(m)
    # where n = number of warehouses & m = number of items
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
        for item in self.orders.keys():
            if self.catalog[item] < self.orders[item]:
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







if __name__ == '__main__':
    w = [{"name":"owd", "inventory":{"apple":5}},{"name":"dm", "inventory":{"apple":5}}]
    o = {"apple":10}

    allocator = InventoryAllocator(w, o)

    print("shipments: {}".format(allocator.get_shipments()))