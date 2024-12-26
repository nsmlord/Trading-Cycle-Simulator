import csv
import matplotlib.pyplot as plt


def generate_trade_report(trades, file_name="trade_report.csv"):
    """
    Generates a CSV report of all executed trades.
    :param trades: List of executed trades, where each trade is a dictionary with:
        - 'buyer': Buyer's trader ID
        - 'seller': Seller's trader ID
        - 'stock': Stock ticker symbol
        - 'quantity': Number of shares traded
        - 'price': Price per share
    :param file_name: Name of the CSV file to generate.
    :return: None
    """
    with open(file_name, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["buyer", "seller", "stock", "quantity", "price"])
        writer.writeheader()
        writer.writerows(trades)
    print(f"Trade report saved as {file_name}")


def generate_performance_metrics(traders):
    """
    Calculates and displays performance metrics for each trader, such as net worth and portfolio composition.
    :param traders: Dictionary of Trader objects, keyed by trader ID.
    :return: A dictionary of performance metrics for each trader.
    """
    metrics = {}
    # Example simplistic metrics (replace with a real calculation if desired)
    for trader_id, trader in traders.items():
        # Suppose we just fix a hypothetical price of 100 for each stock:
        portfolio_value = sum([quantity * 100 for _, quantity in trader.portfolio.items()])
        metrics[trader_id] = {
            "cash_balance": trader.cash,
            "portfolio_value": portfolio_value,
            "net_worth": trader.cash + portfolio_value,
        }

    print("Trader Performance Metrics:")
    print(f"{'Trader ID':<10}{'Cash Balance':<15}{'Portfolio Value':<20}{'Net Worth':<15}")
    print("-" * 60)
    for trader_id, metric in metrics.items():
        print(f"{trader_id:<10}${metric['cash_balance']:<14.2f}${metric['portfolio_value']:<19.2f}${metric['net_worth']:<14.2f}")

    return metrics


def visualize_trade_activity(trades):
    """
    Visualizes trading activity with bar plots showing the number of shares traded for each stock.
    :param trades: List of executed trades.
    :return: None
    """
    trade_counts = {}
    for trade in trades:
        stock = trade["stock"]
        trade_counts[stock] = trade_counts.get(stock, 0) + trade["quantity"]

    # Plotting the data
    stocks = list(trade_counts.keys())
    quantities = list(trade_counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(stocks, quantities, alpha=0.7)
    plt.xlabel("Stock")
    plt.ylabel("Total Quantity Traded")
    plt.title("Trading Activity by Stock")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def generate_fee_summary(total_fees_collected):
    """
    Generates a summary of transaction fees collected during the simulation.
    :param total_fees_collected: Total transaction fees collected.
    :return: None
    """
    print(f"Total Transaction Fees Collected: ${total_fees_collected:.2f}")


def export_trader_balances(traders, file_name="trader_balances.csv"):
    """
    Exports trader balances and portfolio details to a CSV file.
    :param traders: Dictionary of Trader objects, keyed by trader ID.
    :param file_name: Name of the CSV file to generate.
    :return: None
    """
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Trader ID", "Cash Balance", "Portfolio"])
        for trader_id, trader in traders.items():
            writer.writerow([trader.trader_id, trader.cash, trader.portfolio])
    print(f"Trader balances exported as {file_name}")
