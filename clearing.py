def process_clearing_and_settlement(buyer, seller, stock, quantity, price):
    """
    Processes the clearing and settlement of a trade.
    """
    # Calculate total trade value
    total_value = quantity * price

    # Check buyer's cash and seller's stock availability
    if buyer.cash < total_value:
        print(f"Buyer {buyer.trader_id} does not have enough cash for the trade.")
        return
    if seller.portfolio.get(stock, 0) < quantity:
        print(f"Seller {seller.trader_id} does not have enough shares of {stock}.")
        return

    # Adjust buyer's cash and portfolio
    buyer.cash -= total_value
    buyer.portfolio[stock] = buyer.portfolio.get(stock, 0) + quantity

    # Adjust seller's cash and portfolio
    seller.cash += total_value
    if seller.portfolio[stock] == quantity:
        del seller.portfolio[stock]  # Remove stock if fully sold
    else:
        seller.portfolio[stock] -= quantity


def process_transaction_fees(trader, transaction_value, fee_percentage=0.1):
    """
    Deducts a transaction fee from a trader's account based on the trade value.
    """
    fee = transaction_value * (fee_percentage / 100)
    if trader.cash < fee:
        print(f"Trader {trader.trader_id} does not have enough cash for the transaction fee.")
        return
    trader.cash -= fee
    return fee


def batch_clearing_and_settlement(trades, traders):
    """
    Processes clearing and settlement for a batch of trades.
    Returns total fees collected.
    """
    total_fees_collected = 0

    for trade in trades:
        buyer = traders[trade["buyer"]]
        seller = traders[trade["seller"]]
        stock = trade["stock"]
        quantity = trade["quantity"]
        price = trade["price"]

        # Process clearing and settlement
        process_clearing_and_settlement(buyer, seller, stock, quantity, price)

        # Calculate and deduct transaction fees for both buyer and seller
        total_fees_collected += process_transaction_fees(buyer, quantity * price)
        total_fees_collected += process_transaction_fees(seller, quantity * price)

    return total_fees_collected


def display_trader_balances(traders):
    """
    Displays the cash balance and portfolio of all traders.
    """
    print("Trader Balances and Portfolios:")
    print(f"{'Trader ID':<10}{'Cash Balance':<15}{'Portfolio':<20}")
    print("-" * 45)
    for trader_id, trader in traders.items():
        print(f"{trader.trader_id:<10}${trader.cash:<14.2f}{trader.portfolio}")


def display_clearing_summary(trades, total_fees_collected):
    """
    Displays a summary of the clearing and settlement process.
    """
    print("Clearing and Settlement Summary:")
    print(f"{'Buyer':<10}{'Seller':<10}{'Stock':<10}{'Quantity':<10}{'Price':<10}")
    print("-" * 50)
    for trade in trades:
        print(f"{trade['buyer']:<10}{trade['seller']:<10}{trade['stock']:<10}{trade['quantity']:<10}{trade['price']:<10.2f}")
    print(f"\nTotal Fees Collected: ${total_fees_collected:.2f}")
