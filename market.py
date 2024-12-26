import random


def update_market_prices(stock_prices, trades):
    """
    Updates market prices based on executed trades.
    Here we simply nudge prices up or down depending on whether
    the last trade price is above or below the current price.
    """
    for trade in trades:
        stock = trade["stock"]
        if stock not in stock_prices:
            continue

        last_trade_price = trade["price"]
        current_price = stock_prices[stock]

        # If trade executed above the current price, push price up slightly
        if last_trade_price > current_price:
            stock_prices[stock] += (last_trade_price - current_price) * 0.1
        # If trade executed below the current price, push price down slightly
        elif last_trade_price < current_price:
            stock_prices[stock] -= (current_price - last_trade_price) * 0.1

        # Ensure price doesn't drop below $1
        stock_prices[stock] = max(stock_prices[stock], 1)

    return stock_prices


def simulate_random_events(stock_prices):
    """
    Simulates random market events, such as news or economic factors, to affect stock prices.
    Randomly increases or decreases stock prices by a small percentage.
    """
    for stock in stock_prices:
        change_percentage = random.uniform(-0.05, 0.05)  # Price change between -5% and +5%
        stock_prices[stock] *= (1 + change_percentage)
        stock_prices[stock] = max(stock_prices[stock], 1)  # Ensure prices don't drop below $1

    return stock_prices


def calculate_volatility(stock_prices, historical_prices):
    """
    Calculates the volatility of each stock based on historical prices (standard deviation).
    """
    from statistics import stdev

    volatilities = {}
    for stock, prices in historical_prices.items():
        if len(prices) > 1:
            # Calculate percentage changes between consecutive prices
            percentage_changes = [
                (prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))
            ]
            volatilities[stock] = stdev(percentage_changes)
        else:
            volatilities[stock] = 0

    return volatilities


def generate_historical_prices(stock_prices, historical_prices, steps=1):
    """
    Updates the historical prices of stocks by appending current prices.
    """
    for _ in range(steps):
        for stock, price in stock_prices.items():
            if stock not in historical_prices:
                historical_prices[stock] = []
            historical_prices[stock].append(price)
    return historical_prices


def display_market_summary(stock_prices, historical_prices):
    """
    Displays a summary of the market, including current prices and recent volatility.
    """
    volatilities = calculate_volatility(stock_prices, historical_prices)
    print("Market Summary:")
    print(f"{'Stock':<10}{'Current Price':<15}{'Volatility':<15}")
    print("-" * 40)
    for stock, price in stock_prices.items():
        volatility = volatilities.get(stock, 0)
        print(f"{stock:<10}${price:<14.2f}{volatility:<15.2f}")
