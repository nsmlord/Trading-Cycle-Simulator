class Trader:
    """
    Represents a trader in the market with cash and a portfolio.
    """
    def __init__(self, trader_id, cash=0, portfolio=None):
        """
        Initializes a Trader object.
        :param trader_id: Unique ID for the trader.
        :param cash: Cash balance available for the trader.
        :param portfolio: Dictionary containing stocks and their quantities (default: empty portfolio).
        """
        self.trader_id = trader_id
        self.cash = cash
        self.portfolio = portfolio if portfolio else {}

    def __repr__(self):
        """
        Returns a string representation of the Trader object.
        """
        return f"Trader ID: {self.trader_id}, Cash Balance: {self.cash}, Portfolio: {self.portfolio}"


def add_stock_to_portfolio(trader, stock, quantity):
    """
    Adds stocks to a trader's portfolio.
    """
    if quantity <= 0:
        raise ValueError("Quantity to add must be greater than zero.")
    trader.portfolio[stock] = trader.portfolio.get(stock, 0) + quantity


def remove_stock_from_portfolio(trader, stock, quantity):
    """
    Removes stocks from a trader's portfolio.
    """
    if quantity <= 0:
        raise ValueError("Quantity to remove must be greater than zero.")
    if stock in trader.portfolio:
        if trader.portfolio[stock] <= quantity:
            del trader.portfolio[stock]
        else:
            trader.portfolio[stock] -= quantity
    else:
        raise ValueError(f"{trader.trader_id} does not own any shares of {stock}.")


def calculate_portfolio_value(trader, stock_prices):
    """
    Calculates the total value of a trader's portfolio based on current stock prices.
    """
    total_value = 0
    for each_stock, quantity in trader.portfolio.items():
        if each_stock in stock_prices:
            total_value += stock_prices[each_stock] * quantity
        else:
            raise ValueError(f"Price for stock {each_stock} not found in stock_prices.")
    return total_value


def add_cash(trader, amount):
    """
    Adds cash to a trader's account.
    """
    if amount <= 0:
        raise ValueError("Amount to add must be greater than zero.")
    trader.cash += amount


def deduct_cash(trader, amount):
    """
    Deducts cash from a trader's account, returns True if successful, else False.
    """
    if amount <= 0:
        return False
    if trader.cash >= amount:
        trader.cash -= amount
        return True
    else:
        return False


def calculate_pnl(trader, initial_portfolio_value, current_portfolio_value):
    """
    Calculates the profit and loss (PnL) of a trader.
    """
    return current_portfolio_value - initial_portfolio_value


def generate_trader_summary(trader, stock_prices):
    """
    Generates a summary of the trader's portfolio and cash balance.
    """
    portfolio_value = calculate_portfolio_value(trader, stock_prices)
    return {
        "Trader ID": trader.trader_id,
        "Cash Balance": trader.cash,
        "Portfolio Value": portfolio_value,
        "Total Net Worth": trader.cash + portfolio_value,
        "Portfolio": trader.portfolio
    }
