class Product:
    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.category = category.lower()

    def __str__(self):
        return (
            f"{self.product_id} - {self.name} | "
            f"${self.price:.2f} | "
            f"Stock: {self.stock} | "
            f"{self.category}"
        )

    def apply_discount(self, day_of_week):
        new_price = self.price

        # Monday = 0 and Sunday = 6
        if self.category == "dairy" and day_of_week in [1, 3]:
            new_price = self.price * 0.85
        elif self.category == "bakery" and day_of_week in [5, 6]:
            new_price = self.price * 0.75
        elif self.category == "produce" and day_of_week in [0, 1, 2, 3, 4]:
            new_price = self.price * 0.90

        if new_price != self.price:
            new_price = round(new_price * 2) / 2

        return new_price

    def restock(self, amount):
        self.stock = self.stock + amount

    def sell(self, amount):
        if amount <= self.stock:
            self.stock = self.stock - amount
            return True

        return False


class ShoppingCart:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []

    def add_item(self, product, quantity, day_of_week):
        # Only adds to the cart. However, the shop reduces its stock later line.
        unit_price = product.apply_discount(day_of_week)

        cart_item = {
            "product": product,
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": unit_price * quantity
        }

        self.items.append(cart_item)

    def remove_item(self, product):
        for cart_item in self.items:
            if cart_item["product"] == product:
                self.items.remove(cart_item)
                return True

        return False

    def get_total(self):
        total_price = 0

        for cart_item in self.items:
            total_price = total_price + cart_item["line_total"]

        return round(total_price, 2)

    def get_receipt(self):
        receipt = f"Receipt for {self.customer_name}\n"
        receipt = receipt + "-" * 45 + "\n"

        for cart_item in self.items:
            product = cart_item["product"]
            receipt = receipt + (
                f"{product.name}: "
                f"${cart_item['unit_price']:.2f} x {cart_item['quantity']} = "
                f"${cart_item['line_total']:.2f}\n"
            )

        receipt = receipt + "-" * 45 + "\n"
        receipt = receipt + f"Total: ${self.get_total():.2f}"

        return receipt


class Supermarket:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.daily_revenue = 0.0

    def add_product(self, product):
        self.products.append(product)

    def process_sale(self, cart, day_of_week):
        # Check all stock first before changing
        for cart_item in cart.items:
            product = cart_item["product"]
            quantity = cart_item["quantity"]

            if quantity > product.stock:
                print(f"Sale could not be completed. Not enough {product.name}.")
                return False

        # If everything is available then reduce the stock
        for cart_item in cart.items:
            product = cart_item["product"]
            quantity = cart_item["quantity"]
            product.sell(quantity)

        self.daily_revenue = self.daily_revenue + cart.get_total()
        print(cart.get_receipt())

        return True

    def find_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product

        return None

    def low_stock_report(self):
        low_stock = []

        for product in self.products:
            if product.stock <= 5:
                low_stock.append(product)

        return low_stock

    def save_inventory(self, filename):
        inventory_file = open(filename, "w")

        for product in self.products:
            inventory_file.write(
                f"{product.product_id}|{product.name}|{product.price}|"
                f"{product.stock}|{product.category}\n"
            )

        inventory_file.close()

    def load_inventory(self, filename):
        self.products = []

        inventory_file = open(filename, "r")

        for line in inventory_file:
            product_data = line.strip().split("|")

            new_product = Product(
                product_data[0],
                product_data[1],
                float(product_data[2]),
                int(product_data[3]),
                product_data[4]
            )

            self.products.append(new_product)

        inventory_file.close()

    def print_daily_summary(self):
        print("\nDaily Summary")
        print("-" * 45)
        print(f"Shop name: {self.name}")
        print(f"Money made today: ${self.daily_revenue:.2f}")

        print("\nLow stock items:")

        low_stock = self.low_stock_report()

        if len(low_stock) == 0:
            print("No products are low in stock.")
        else:
            for product in low_stock:
                print(product)


# Final test code

shop = Supermarket("CDU Supermarket")

milk = Product("P001", "Full Cream Milk", 3.20, 24, "dairy")
cheese = Product("P002", "Cheddar Cheese", 5.80, 4, "dairy")
bread = Product("P003", "White Bread", 4.73, 15, "bakery")
cake = Product("P004", "Chocolate Cake", 8.50, 5, "bakery")
apples = Product("P005", "Apples", 2.50, 40, "produce")
bananas = Product("P006", "Bananas", 3.10, 3, "produce")

shop.add_product(milk)
shop.add_product(cheese)
shop.add_product(bread)
shop.add_product(cake)
shop.add_product(apples)
shop.add_product(bananas)

print("Discount Test")
print("-" * 45)
print("Milk on Tuesday:", milk.apply_discount(1))
print("Bread on Saturday:", bread.apply_discount(5))
print("Apples on Wednesday:", apples.apply_discount(2))

print("\nCart 1")
print("-" * 45)

cart1 = ShoppingCart("Jacob")
cart1.add_item(milk, 2, 1)
cart1.add_item(bread, 1, 5)
cart1.add_item(apples, 4, 2)

shop.process_sale(cart1, 1)

print("\nCart 2")
print("-" * 45)

cart2 = ShoppingCart("David")
cart2.add_item(cheese, 10, 1)
cart2.add_item(bananas, 2, 1)

shop.process_sale(cart2, 1)

print("\nSaving inventory...")
shop.save_inventory("inventory.txt")

print("Clearing products...")
shop.products = []

print("Loading inventory...")
shop.load_inventory("inventory.txt")

shop.print_daily_summary()
