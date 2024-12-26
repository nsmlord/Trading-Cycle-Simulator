import random
import string


def generate_unique_order_id(existing_ids):
    """
    Generates a unique order ID that does not conflict with existing IDs.
    """
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if new_id not in existing_ids:
            return new_id


def calculate_net_worth(trader, stock_prices):
    """
    Calculates the net worth of a trader by summing cash and the value of their portfolio.
    """
    portfolio_value = sum(
        stock_prices[stock] * quantity
        for stock, quantity in trader.portfolio.items()
        if stock in stock_prices
    )
    return trader.cash + portfolio_value


def calculate_average_price(trades, stock):
    """
    Calculates the average trade price for a specific stock.
    """
    total_quantity = 0
    total_value = 0

    for trade in trades:
        if trade["stock"] == stock:
            total_quantity += trade["quantity"]
            total_value += trade["price"] * trade["quantity"]

    if total_quantity == 0:
        return 0
    return total_value / total_quantity


def calculate_total_trade_volume(trades):
    """
    Calculates the total trade volume across all stocks.
    """
    return sum(trade["quantity"] for trade in trades)


def filter_trades_by_stock(trades, stock):
    """
    Filters trades for a specific stock.
    """
    return [trade for trade in trades if trade["stock"] == stock]


def summarize_trades(trades):
    """
    Generates a summary of trades, grouped by stock, showing total volume and average price.
    """
    summary = {}
    for trade in trades:
        stock = trade["stock"]
        if stock not in summary:
            summary[stock] = {"total_volume": 0, "total_value": 0}

        summary[stock]["total_volume"] += trade["quantity"]
        summary[stock]["total_value"] += trade["price"] * trade["quantity"]

    # Calculate average prices
    for stock, stats in summary.items():
        if stats["total_volume"] > 0:
            stats["average_price"] = stats["total_value"] / stats["total_volume"]
        else:
            stats["average_price"] = 0
        del stats["total_value"]

    return summary


def display_trade_summary(trade_summary):
    """
    Displays a summary of trades in a readable format.
    """
    print("Trade Summary:")
    print(f"{'Stock':<10}{'Total Volume':<15}{'Average Price':<15}")
    print("-" * 40)
    for stock, stats in trade_summary.items():
        print(f"{stock:<10}{stats['total_volume']:<15}{stats['average_price']:<15.2f}")


def simulate_random_stock_prices(stocks, base_price_range=(50, 150)):
    """
    Simulates random stock prices for a list of stocks.
    """
    return {stock: random.uniform(*base_price_range) for stock in stocks}


def random_trader_action(trader, stocks, stock_prices):
    """
    Simulates a random action (buy or sell) for a trader.
    """
    action_type = random.choice(["buy", "sell"])
    stock = random.choice(stocks)
    price = stock_prices[stock]

    if action_type == "buy":
        max_quantity = int(trader.cash / price)
        quantity = random.randint(1, max_quantity) if max_quantity > 0 else 0
    else:
        quantity = random.randint(1, trader.portfolio.get(stock, 0)) if stock in trader.portfolio else 0

    return {
        "type": action_type,
        "stock": stock,
        "quantity": quantity,
        "price": price,
    }
