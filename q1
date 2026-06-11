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

        # Apply discount based on category and day of the week
        if self.category == "dairy" and day_of_week in [1, 3]:
            price = self.price * 0.85

        elif self.category == "bakery" and day_of_week in [5, 6]:
            price = self.price * 0.75

        elif self.category == "produce" and day_of_week in [0, 1, 2, 3, 4]:
            price = self.price * 0.90

        # Round discounted prices to the nearest $0.50
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
        # Add item only if enough stock is available
        if product.sell(quantity):
            unit_price = product.apply_discount(day_of_week)

            item = {
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": unit_price * quantity
            }

            self.items.append(item)

        else:
            print(f"Not enough stock available for {product.name}.")

    def remove_item(self, product):
        for item in self.items:
            if item["product"] == product:
                product.restock(item["quantity"])
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


# ----------------------
# Testing the program
# ----------------------

milk = Product("P001", "Full Cream Milk", 3.20, 24, "dairy")
bread = Product("P002", "White Bread", 4.73, 15, "bakery")
apples = Product("P003", "Apples", 2.50, 40, "produce")
chips = Product("P004", "Potato Chips", 3.75, 20, "snacks")

# Display product information
print(milk)
print(bread)
print(apples)
print(chips)

# Create a shopping cart
cart = ShoppingCart("Jacob Roy")

# Tuesday (1) - dairy discount applies
cart.add_item(milk, 2, 1)

# Saturday (5) - bakery discount applies
cart.add_item(bread, 1, 5)

# Wednesday (2) - produce discount applies
cart.add_item(apples, 4, 2)

# Friday (4) - snacks have no discount
cart.add_item(chips, 2, 4)

# Print the receipt
print()
print(cart.get_receipt())
