"""

Maharshii Patel
251353283
mpate588
December 8, 2023,
This file includes 4 objects and 2 functions. The first object is a product which has the parameters of product name,
price, and category. The second object is an inventory, which keeps track of all products and their quantities and also
their prices. The third object is the shopping cart which is what the customer has. You can see what's in the cart and
and and remove from it which affects the inventory. The last object is the catalog which just displays all the products
and their prices. The two external functions serve the same purpose, they take a csv and then put the product data into
the catalog and/or the inventory.

"""


class Product:
    def __init__(self, name, price, category):  # Initialize the variables
        # Initialize product attributes
        self._name = name
        self._price = price
        self._category = category

    def __eq__(self, other):  # Checks if two products are the same
        if isinstance(other, Product):
            if self._name == other._name and self._price == other._price and self._category:
                return True
            else:
                return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        # return f"Product:{self._name}, Price:{self._price},Category:{self._category}"
        rep = 'Product(' + self._name + ', ' + str(self._price) + ', ' + self._category + ')'
        return rep


class Inventory:
    def __init__(self):  # Initialize the variables
        self._name = []
        self._price = []
        self._quantity = []

    def add_to_productInventory(self, productName, productPrice, productQuantity):
        # Adds product and its price and quantity into the lists
        self._name.append(productName)
        self._price.append(int(productPrice))
        self._quantity.append(int(productQuantity))

    def add_productQuantity(self, nameProduct, addQuantity):
        self._quantity[self._name.index(nameProduct)] += addQuantity

    def remove_productQuantity(self, nameProduct, removeQuantity):
        self._quantity[self._name.index(nameProduct)] -= removeQuantity

    def get_productPrice(self, nameProduct):
        return self._price[self._name.index(nameProduct)]

    def get_productQuantity(self, nameProduct):
        return self._quantity[self._name.index(nameProduct)]

    def display_Inventory(self):
        space = ", "
        for i in range(len(self._name)):
            print(self._name[i] + space + str(self._price[i]) + space + str(self._quantity[i]))


class ShoppingCart:  # Initialize the variables
    def __init__(self, buyerName, inventory):
        self._buyerName = buyerName
        self._inventory = inventory
        self._products = []
        self._prices = []
        self._quantities = []

    def add_to_cart(self, nameProduct, requestedQuantity):
        if requestedQuantity > self._inventory.get_productQuantity(nameProduct):
            # If the requested amount exceeds the inventory amount, cannot be fulfilled
            return "Can not fill the order"
        else:
            if nameProduct in self._products:  # For if product is already in cart
                self._quantities[self._products.index(nameProduct)] += requestedQuantity
                self._inventory.remove_productQuantity(nameProduct, requestedQuantity)
            else:  # For if product is not yet in cart
                self._products.append(nameProduct)
                self._prices.append(self._inventory.get_productPrice(nameProduct))
                self._quantities.append(requestedQuantity)
                self._inventory.remove_productQuantity(nameProduct, requestedQuantity)
            return "Filled the order"

    def remove_from_cart(self, nameProduct, requestedQuantity):
        if nameProduct in self._products:
            product_index = self._products.index(nameProduct)
            if requestedQuantity <= self._quantities[product_index]:  # If the requested quantity is valid
                self._quantities[product_index] -= requestedQuantity
                if self._quantities[product_index] == 0:  # If the quantity of the product is 0, then it's removed
                    self._products.remove(nameProduct)
                    self._prices.remove(self._prices[product_index])
                    self._quantities.remove(0)
                self._inventory.add_productQuantity(nameProduct, requestedQuantity)  # Add quantity back to inventory
                return "Successful"
            else:
                # If the requested amount exceeds the cart amount, cannot be fulfilled
                return "The requested quantity to be removed from cart exceeds what is in the cart"
        else:
            return "Product not in the cart"

    def view_cart(self):
        total_price = 0
        for p in self._products:  # Get total price of cart
            quantity = self._quantities[self._products.index(p)]
            total_price += self._inventory.get_productPrice(p) * quantity
            print(p, str(quantity))  # Prints name then quantity
        print("Total: " + str(total_price))  # Total price
        print("Buyer Name: " + self._buyerName)  # Name of buyer


class Catalog:
    def __init__(self):  # Initialize the variables
        self._products = []
        self._low_price = []  # 0 and 99 inclusive
        self._med_price = []  # 100 and 499 inclusive
        self._high_price = []  # 500 and higher inclusive

    def addProduct(self, product):
        self._products.append(product)

    def price_category(self):  # Puts the products into categories of low, medium, and high then prints them out
        for p in self._products:
            if p.get_price() <= 99:
                self._low_price.append(p)
            elif 100 <= p.get_price() <= 499:
                self._med_price.append(p)
            else:
                self._high_price.append(p)

        print("Number of low price items: " + str(len(self._low_price)))
        print("Number of medium price items: " + str(len(self._med_price)))
        print("Number of high price items: " + str(len(self._high_price)))

    def display_catalog(self):
        my_list = self._low_price + self._med_price + self._high_price
        for p in self._products:
            # Product: (Product Name) Price: (Product Price) Category: (Category of Product)
            print("Product: " + p.get_name() + " Price: " + str(p.get_price()) + " Category: " + p.get_category())


def populate_inventory(filename):  # Reads csv file contents and adds products to the inventory
    with open(filename, "r") as f:
        f_new = []

        for line in f.readlines():  # Read all the lines and split into arrays
            f_new.append(line.strip().split(","))

        inventory_object = Inventory()  # Create catalog object

        for product in f_new:
            # Adds product name, price, and total quantity of product
            inventory_object.add_to_productInventory(product[0].strip(), int(product[1].strip()), product[2].strip())

        return inventory_object


def populate_catalog(fileName):  # Reads csv file contents and adds products to the catalog
    with open(fileName, "r") as f:
        f_new = []

        for line in f.readlines():  # Read all the lines and split into arrays
            f_new.append(line.strip().split(","))

        catalog_object = Catalog()  # Create catalog object

        for product in f_new:
            # Adds product name, price, and category as a product object
            product_object = Product(product[0].strip(), int(product[1].strip()), product[3].strip())
            catalog_object.addProduct(product_object)

        return catalog_object




