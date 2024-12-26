import matplotlib.pyplot as plt
import numpy as np


def plot_stock_prices_over_time(historical_prices):
    """
    Plots each stock's price over time on one chart.
    :param historical_prices: dict of stock -> list of prices.
                             E.g. { 'AAPL': [100, 102, 101, ...], 'GOOG': [...], ... }
    """
    plt.figure(figsize=(10, 6))

    # Each stock is a separate line
    for stock, price_list in historical_prices.items():
        plt.plot(price_list, label=stock, marker='o', linewidth=2)

    plt.title("1) Stock Prices Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Price ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_trader_volume_over_time(trader_volume_history):
    """
    Plots each trader's total traded volume at each time step on one chart.
    :param trader_volume_history: dict of trader_id -> list of volumes per step
                                  E.g. {1: [3, 2, 0, 5], 2: [...], ...}
    """
    plt.figure(figsize=(10, 6))

    # Each trader is a separate line
    for trader_id, volumes in trader_volume_history.items():
        plt.plot(volumes, label=f"Trader {trader_id}", marker='o', linewidth=2)

    plt.title("2) Trader Volume Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Number of Shares Traded")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_trader_net_worth_over_time(net_worth_history):
    """
    Plots each trader's net worth (cash + portfolio value) at each step, overlaid on one chart.
    :param net_worth_history: dict of trader_id -> list of net worth per step
                              E.g. {1: [10500, 10400, 11000, ...], 2: [...], ...}
    """
    plt.figure(figsize=(10, 6))

    for trader_id, worth_list in net_worth_history.items():
        plt.plot(worth_list, label=f"Trader {trader_id}", marker='o', linewidth=2)

    plt.title("3) Trader Net Worth Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("Net Worth ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_final_portfolio_composition(traders, stock_prices):
    """
    Creates a grouped bar chart: for each stock on the X-axis, plot a bar for each trader,
    color-coded to show how much of that stock they hold (in total value).
    :param traders: dict of trader_id -> Trader object (with .portfolio and .cash)
    :param stock_prices: dict of stock -> float (final stock price)
    """
    # Gather a set of all stocks that exist in the simulation
    all_stocks = set(stock_prices.keys())
    # Also include any stock that might be in a trader's portfolio but not in stock_prices (rare)
    for trader in traders.values():
        all_stocks.update(trader.portfolio.keys())
    all_stocks = sorted(list(all_stocks))

    # We need a bar for each trader in each stock
    trader_ids = sorted(traders.keys())
    n_stocks = len(all_stocks)
    n_traders = len(trader_ids)

    # We'll build a 2D matrix: row = stock index, column = trader index -> total value
    data_matrix = np.zeros((n_stocks, n_traders))

    for i, stock in enumerate(all_stocks):
        for j, t_id in enumerate(trader_ids):
            qty = traders[t_id].portfolio.get(stock, 0)
            price = stock_prices.get(stock, 0)
            data_matrix[i, j] = qty * price

    # Now we create a grouped bar chart
    plt.figure(figsize=(10, 6))
    bar_width = 0.8 / n_traders  # fraction of total available width
    x_positions = np.arange(n_stocks)

    for j, t_id in enumerate(trader_ids):
        # shift each trader's bars by j * bar_width
        offsets = x_positions + j * bar_width
        plt.bar(offsets, data_matrix[:, j], bar_width, label=f"Trader {t_id}")

    plt.title("4) Final Portfolio Composition (Value)")
    plt.xlabel("Stock")
    plt.ylabel("Total Value Held ($)")
    plt.xticks(x_positions + bar_width * (n_traders / 2 - 0.5), all_stocks)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()
