import sys
from pathlib import Path

# Dynamic path injection to allow importing from the 'src' directory
# without requiring the package to be installed globally.
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.resolve()))

from models import User, Product, Order


class TestUser:
    """Unit tests for the User model."""

    def test_user_initialization(self):
        """Check if the constructor correctly assigns fields."""
        user_id = 1
        username = "johndoe"

        user = User(user_id, username)

        assert user.user_id == user_id
        assert user.username == username

    def test_user_str_representation(self):
        """Check the formatting of the __str__ method."""
        user = User(5, "alice")

        user_str = str(user)

        expected_str = "User[ID: 5, Username: 'alice']"
        assert user_str == expected_str

    def test_user_equality(self):
        """Check the behavior of the __eq__ method with strict parameter isolation."""
        user_base = User(1, "johndoe")
        user_same = User(1, "johndoe")

        user_diff_id = User(2, "johndoe")
        user_diff_name = User(1, "janedoe")

        # Verify that objects with identical data are considered equal.
        assert user_base == user_same

        # Verify that differing on any single field results in inequality.
        assert user_base != user_diff_id
        assert user_base != user_diff_name

        # Verify type safety during comparison (comparing User with String/None).
        assert user_base != "not_a_user_object"
        assert not (user_base == None)


class TestProduct:
    """Unit tests for the Product model."""

    def test_product_initialization(self):
        """Check if the constructor correctly assigns fields."""
        product_id = 101
        name = "Laptop"
        price = 2999.99

        product = Product(product_id, name, price)

        assert product.product_id == product_id
        assert product.name == name
        assert product.price == price

    def test_product_str_representation(self):
        """Check the formatting of the __str__ method."""
        product = Product(101, "Laptop", 2999.99)

        product_str = str(product)

        expected_str = "Product[ID: 101, Name: 'Laptop', Price: $2999.99]"
        assert product_str == expected_str

    def test_product_equality(self):
        """Check the behavior of the __eq__ method with strict parameter isolation."""
        prod_base = Product(10, "Mouse", 49.50)
        prod_same = Product(10, "Mouse", 49.50)

        prod_diff_id = Product(11, "Mouse", 49.50)
        prod_diff_name = Product(10, "Keyboard", 49.50)
        prod_diff_price = Product(10, "Mouse", 120.00)

        # Verify equality logic.
        assert prod_base == prod_same

        # Verify inequality logic for every distinct field.
        assert prod_base != prod_diff_id
        assert prod_base != prod_diff_name
        assert prod_base != prod_diff_price

        # Verify type safety.
        assert prod_base != 49.50
        assert not (prod_base == None)


class TestOrder:
    """Unit tests for the Order model."""

    def test_order_initialization(self):
        """Check if the constructor correctly assigns fields."""
        order_id = 500
        item_name = "Monitor"
        quantity = 2

        order = Order(order_id, item_name, quantity)

        assert order.order_id == order_id
        assert order.item_name == item_name
        assert order.quantity == quantity

    def test_order_str_representation(self):
        """Check the formatting of the __str__ method."""
        order = Order(500, "Monitor", 2)

        order_str = str(order)

        expected_str = "Order[ID: 500, Item: 'Monitor', Qty: 2]"
        assert order_str == expected_str

    def test_order_equality(self):
        """Check the behavior of the __eq__ method with strict parameter isolation."""
        order_base = Order(1, "Desk", 1)
        order_same = Order(1, "Desk", 1)

        order_diff_id = Order(2, "Desk", 1)
        order_diff_item = Order(1, "Chair", 1)
        order_diff_qty = Order(1, "Desk", 4)

        # Verify equality logic.
        assert order_base == order_same

        # Verify inequality logic for every distinct field.
        assert order_base != order_diff_id
        assert order_base != order_diff_item
        assert order_base != order_diff_qty

        # Verify type safety.
        assert order_base != "not_an_order_object"
        assert not (order_base == None)
