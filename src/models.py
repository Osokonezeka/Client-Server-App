"""
Data models representing the business logic entities required by the project.
Each class fulfills the requirement of having at least two fields and
custom implementations of constructor, toString, and equals methods.
"""


class User:
    def __init__(self, user_id: int, username: str):
        """Constructor"""
        self.user_id = user_id
        self.username = username

    def __str__(self) -> str:
        """toString equivalent"""
        return f"User[ID: {self.user_id}, Username: '{self.username}']"

    def __eq__(self, other) -> bool:
        """equals equivalent"""
        if not isinstance(other, User):
            return False
        return self.user_id == other.user_id and self.username == other.username


class Product:
    def __init__(self, product_id: int, name: str, price: float):
        """Constructor"""
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        """toString equivalent"""
        return f"Product[ID: {self.product_id}, Name: '{self.name}', Price: ${self.price:.2f}]"

    def __eq__(self, other) -> bool:
        """equals equivalent"""
        if not isinstance(other, Product):
            return False
        return (self.product_id == other.product_id and
                self.name == other.name and
                self.price == other.price)


class Order:
    def __init__(self, order_id: int, item_name: str, quantity: int):
        """Constructor"""
        self.order_id = order_id
        self.item_name = item_name
        self.quantity = quantity

    def __str__(self) -> str:
        """toString equivalent"""
        return f"Order[ID: {self.order_id}, Item: '{self.item_name}', Qty: {self.quantity}]"

    def __eq__(self, other) -> bool:
        """equals equivalent"""
        if not isinstance(other, Order):
            return False
        return (self.order_id == other.order_id and
                self.item_name == other.item_name and
                self.quantity == other.quantity)
