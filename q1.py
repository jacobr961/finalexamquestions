class Product:
    def __init__(self, product_id, name, price, stock, category):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.category = category.lower()

    def __str__(self):
        return (
            f"[{self.product_id}] {self.name} | "
            f"${self.price:.2f} | "
            f"Stock: {self.stock} | "
            f"Category: {self.category}"
        )

    def apply_discount(self, day_of_week):
        price = self.price

        # Check category and day to decide if discount applies
        if self.category == "dairy" and day_of_week in [1, 3]:
            price = self.price * 0.85
        elif self.category == "bakery" and day_of_week in [5, 6]:
            price = self.price * 0.75
        elif self.category == "produce" and day_of_week in [0, 1, 2, 3, 4]:
            price = self.price * 0.90

        # Only discounted prices are rounded to the nearest 50 cents
        if price != self.price:
            price = round(price * 2) / 2

        return price

    def restock(self, amount):
        self.stock += amount

    def sell(self, amount):
        if amount <= self.stock:
            self.stock -= amount
            return True

        return False


class ShoppingCart:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []

    def add_item(self, product, quantity, day_of_week):
        # Stock is not reduced here. It is reduced later in process_sale().
        unit_price = product.apply_discount(day_of_week)

        item = {
            "product": product,
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": unit_price * quantity
        }

        self.items.append(item)

    def remove_item(self, product):
        for item in self.items:
            if item["product"] == product:
                self.items.remove(item)
                return True

        return False

    def get_total(self):
        total = 0

        for item in self.items:
            total += item["line_total"]

        return round(total, 2)

    def get_receipt(self):
        receipt = f"Receipt for {self.customer_name}\n"
        receipt += "-" * 50 + "\n"

        for item in self.items:
            receipt += (
                f"{item['product'].name} | "
                f"Unit Price: ${item['unit_price']:.2f} | "
                f"Quantity: {item['quantity']} | "
                f"Line Total: ${item['line_total']:.2f}\n"
            )

        receipt += "-" * 50 + "\n"
        receipt += f"Grand Total: ${self.get_total():.2f}"

        return receipt


class Supermarket:
    def __init__(self, name):
        self.name = name
        self.products = []
        self.daily_revenue = 0.0

    def add_product(self, product):
        self.products.append(product)

    def process_sale(self, cart, day_of_week):
        # First check all items before taking away any stock
        for item in cart.items:
            product = item["product"]
            quantity = item["quantity"]

            if quantity > product.stock:
                print(f"Sale failed. Not enough stock for {product.name}.")
                return False

        # If all stock is available, then complete the sale
        for item in cart.items:
            product = item["product"]
            quantity = item["quantity"]
            product.sell(quantity)

        self.daily_revenue += cart.get_total()
        print(cart.get_receipt())
        return True

    def find_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product

        return None

    def low_stock_report(self):
        low_stock_items = []

        for product in self.products:
            if product.stock <= 5:
                low_stock_items.append(product)

        return low_stock_items

    def save_inventory(self, filename):
        file = open(filename, "w")

        for product in self.products:
            file.write(
                f"{product.product_id}|{product.name}|{product.price}|"
                f"{product.stock}|{product.category}\n"
            )

        file.close()

    def load_inventory(self, filename):
        self.products = []

        file = open(filename, "r")

        for line in file:
            parts = line.strip().split("|")

            product = Product(
                parts[0],
                parts[1],
                float(parts[2]),
                int(parts[3]),
                parts[4]
            )

            self.products.append(product)

        file.close()

    def print_daily_summary(self):
        print("\nDaily Summary")
        print("-" * 50)
        print(f"Supermarket: {self.name}")
        print(f"Daily Revenue: ${self.daily_revenue:.2f}")

        print("\nLow Stock Products:")
        low_stock_items = self.low_stock_report()

        if len(low_stock_items) == 0:
            print("No low stock products.")
        else:
            for product in low_stock_items:
                print(product)


# Main program

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

print("Discount Testing")
print("-" * 50)
print("Milk on Tuesday:", milk.apply_discount(1))
print("Bread on Saturday:", bread.apply_discount(5))
print("Apples on Wednesday:", apples.apply_discount(2))

print("\nProcessing Cart 1")
print("-" * 50)

cart1 = ShoppingCart("Jacob")
cart1.add_item(milk, 2, 1)
cart1.add_item(bread, 1, 5)
cart1.add_item(apples, 4, 2)

shop.process_sale(cart1, 1)

print("\nProcessing Cart 2")
print("-" * 50)

cart2 = ShoppingCart("David")
cart2.add_item(cheese, 10, 1)
cart2.add_item(bananas, 2, 1)

shop.process_sale(cart2, 1)

print("\nSaving inventory...")
shop.save_inventory("inventory.txt")

print("Clearing product list...")
shop.products = []

print("Loading inventory again...")
shop.load_inventory("inventory.txt")

shop.print_daily_summary()
```
