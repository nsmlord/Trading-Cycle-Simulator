from order import sort_order_book
from trader import Trader

def match_orders(order_book, traders):
    """
    Matches buy and sell orders in the order book.
    Orders are matched based on price priority (best price) and then time priority (FIFO).
    :param order_book: Dictionary with 'buy' and 'sell' order lists.
    :param traders: Dictionary of Trader objects, keyed by trader ID.
    :return: List of executed trades (each trade is a dictionary with details of the match).
    """
    executed_trades = []

    # Ensure buy orders are sorted by highest price first and sell orders by lowest price first
    sort_order_book(order_book, "buy")
    sort_order_book(order_book, "sell")

    while order_book["buy"] and order_book["sell"]:
        buy_order = order_book["buy"][0]
        sell_order = order_book["sell"][0]

        # Check if the orders match (buy price >= sell price)
        if buy_order.price >= sell_order.price:
            # Determine the trade quantity
            trade_quantity = min(buy_order.quantity, sell_order.quantity)
            trade_price = sell_order.price  # Use the sell order price as the trade price

            # Execute the trade
            execute_trade(
                traders[buy_order.trader_id],
                traders[sell_order.trader_id],
                buy_order.stock,
                trade_quantity,
                trade_price
            )

            # Record the trade
            executed_trades.append({
                "buyer": buy_order.trader_id,
                "seller": sell_order.trader_id,
                "stock": buy_order.stock,
                "quantity": trade_quantity,
                "price": trade_price
            })

            # Adjust the order quantities
            buy_order.quantity -= trade_quantity
            sell_order.quantity -= trade_quantity

            # Remove fully filled orders
            if buy_order.quantity == 0:
                order_book["buy"].pop(0)
            if sell_order.quantity == 0:
                order_book["sell"].pop(0)
        else:
            # No match possible, exit loop
            break

    return executed_trades


def execute_trade(buyer, seller, stock, quantity, price):
    """
    Executes a trade between a buyer and a seller.
    Adjusts their cash and portfolio based on the trade details.
    :param buyer: Trader object for the buyer.
    :param seller: Trader object for the seller.
    :param stock: Stock ticker symbol.
    :param quantity: Number of shares traded.
    :param price: Price per share for the trade.
    :return: None
    """
    # Deduct cash from buyer
    total_cost = quantity * price
    if buyer.cash < total_cost:
        print(f"Buyer {buyer.trader_id} does not have enough cash.")
        return
    buyer.cash -= total_cost

    # Add stock to buyer's portfolio
    buyer.portfolio[stock] = buyer.portfolio.get(stock, 0) + quantity

    # Add cash to seller
    seller.cash += total_cost

    # Remove stock shares from seller's portfolio
    if stock not in seller.portfolio or seller.portfolio[stock] < quantity:
        print(f"Seller {seller.trader_id} does not have enough shares of {stock}.")
        return
    seller.portfolio[stock] -= quantity
    if seller.portfolio[stock] == 0:
        del seller.portfolio[stock]


def display_executed_trades(executed_trades):
    """
    Displays the details of executed trades in a readable format.
    :param executed_trades: List of executed trades.
    :return: None
    """
    print("Executed Trades:")
    print(f"{'Buyer':<10}{'Seller':<10}{'Stock':<10}{'Quantity':<10}{'Price':<10}")
    print("-" * 50)
    for trade in executed_trades:
        print(f"{trade['buyer']:<10}{trade['seller']:<10}{trade['stock']:<10}{trade['quantity']:<10}{trade['price']:<10.2f}")
