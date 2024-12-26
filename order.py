class Order:
    """
    Represents a trade order.
    """

    def __init__(self, order_id, trader_id, order_type, stock, quantity, price):
        """
        Initializes an Order object.
        """
        self.order_id = order_id
        self.trader_id = trader_id
        self.order_type = order_type  # 'buy' or 'sell'
        self.stock = stock
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return (f"OrderID: {self.order_id} | Trader: {self.trader_id} | "
                f"{self.order_type} {self.quantity} shares of {self.stock} @ ${self.price:.2f}")


def create_order(trader, order_id, order_type, stock, quantity, price):
    """
    Creates a new order if valid. Does NOT automatically add it to the order book.
    """
    if not validate_order(trader, order_type, stock, quantity, price):
        raise ValueError("Invalid order: insufficient funds or stock.")

    new_order = Order(order_id, trader.trader_id, order_type, stock, quantity, price)
    return new_order


def validate_order(trader, order_type, stock, quantity, price):
    """
    Validates whether the trader can place the order.
    """
    if quantity <= 0 or price <= 0:
        return False

    if order_type == "buy":
        return trader.cash >= (quantity * price)
    elif order_type == "sell":
        return trader.portfolio.get(stock, 0) >= quantity
    return False


def add_order_to_book(order, order_book):
    """
    Adds an order to the appropriate list in the order book.
    """
    order_book[order.order_type].append(order)


def cancel_order(order_id, order_book):
    """
    Cancels an order from the order book.
    """
    for o_type in ["buy", "sell"]:
        for order in order_book[o_type]:
            if order.order_id == order_id:
                order_book[o_type].remove(order)
                return True
    return False


def get_order_by_id(order_id, order_book):
    """
    Retrieves an order from the order book using its ID.
    """
    for o_type in ["buy", "sell"]:
        for order in order_book[o_type]:
            if order.order_id == order_id:
                return order
    return None


def is_buy_order(order):
    return order.order_type == "buy"


def is_sell_order(order):
    return order.order_type == "sell"


def sort_order_book(order_book, order_type):
    """
    Sorts the order book for a specific order type ('buy' or 'sell').
    Buy orders: Desc by price.
    Sell orders: Asc by price.
    """
    if order_type == "buy":
        order_book[order_type].sort(key=lambda o: (-o.price, o.order_id))
    elif order_type == "sell":
        order_book[order_type].sort(key=lambda o: (o.price, o.order_id))


def display_order_book(order_book):
    """
    Displays the current state of the order book in a readable format.
    """
    print("Buy Orders:")
    for order in order_book["buy"]:
        print(f"  {order}")

    print("Sell Orders:")
    for order in order_book["sell"]:
        print(f"  {order}")
