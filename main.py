import random
import matplotlib.pyplot as plt

# Imports from your existing modules (adjust paths as needed):
from trader import Trader
from order import create_order, add_order_to_book
from matching_engine import match_orders
from clearing import batch_clearing_and_settlement
from reporting import generate_trade_report, visualize_trade_activity
from utils import simulate_random_stock_prices, generate_unique_order_id

# Our new visualization functions:
from visualizations import (
    plot_stock_prices_over_time,
    plot_trader_volume_over_time,
    plot_trader_net_worth_over_time,
    plot_final_portfolio_composition
)


def initialize_simulation():
    """
    Initializes the simulation state, including stock prices, traders, and order book.
    """
    stocks = ["AAPL", "GOOG", "MSFT", "TSLA"]
    # Slightly narrower base price range so they're affordable
    stock_prices = simulate_random_stock_prices(stocks, (50, 70))

    # Initialize traders with more cash + a small starting portfolio
    traders = {}
    for trader_id in range(1, 6):
        cash_amount = random.randint(20000, 30000)
        t = Trader(trader_id, cash=cash_amount)

        # Give each trader some shares in exactly one stock
        random_stock = random.choice(stocks)
        t.portfolio[random_stock] = random.randint(5, 15)

        traders[trader_id] = t

    order_book = {"buy": [], "sell": []}

    return {
        "stock_prices": stock_prices,
        "traders": traders,
        "order_book": order_book
    }


def place_order(trader, order_book, order_type, stock, quantity, price):
    """
    Places an order for a trader if valid. Creates a unique ID and adds to the order book.
    """
    try:
        # Gather existing IDs in order book
        existing_ids = {o.order_id for o in order_book["buy"] + order_book["sell"]}
        order_id = generate_unique_order_id(existing_ids)

        new_order = create_order(
            trader=trader,
            order_id=order_id,
            order_type=order_type,
            stock=stock,
            quantity=quantity,
            price=price
        )
        add_order_to_book(new_order, order_book)

    except ValueError as e:
        print(f"Order failed for Trader {trader.trader_id}: {e}")


def main():
    # Initialize simulation
    simulation_state = initialize_simulation()
    stock_prices = simulation_state["stock_prices"]
    traders = simulation_state["traders"]
    order_book = simulation_state["order_book"]

    # We'll store historical data for plotting:
    # 1) Stock prices over time
    historical_prices = {s: [] for s in stock_prices}
    # 2) Trader volume: how many shares each trader trades each step
    trader_volume_history = {t_id: [] for t_id in traders}
    # 3) Trader net worth
    net_worth_history = {t_id: [] for t_id in traders}

    trade_history = []

    # Pre-populate step 0
    for s in stock_prices:
        historical_prices[s].append(stock_prices[s])
    for t_id, trader in traders.items():
        trader_volume_history[t_id].append(0)  # no trades at step 0
        # net worth = cash + sum(qty * price)
        worth = trader.cash
        for st, qty in trader.portfolio.items():
            worth += stock_prices[st] * qty
        net_worth_history[t_id].append(worth)

    # Run the simulation
    num_steps = 20
    for step in range(num_steps):
        print(f"\n--- Simulation Step {step + 1} ---")

        # Show current stock prices
        print("Stock Prices:")
        for st, price in stock_prices.items():
            print(f"{st}: ${price:.2f}")

        # Randomly place orders for each trader
        for t_id, trader in traders.items():
            # Weighted approach to encourage some sells
            # If the trader actually owns something, maybe they do a sell 30% of time
            if trader.portfolio and random.random() < 0.3:
                order_type = "sell"
                # pick a random stock they own
                stock = random.choice(list(trader.portfolio.keys()))
                max_qty = trader.portfolio[stock]
                quantity = random.randint(1, max_qty) if max_qty > 0 else 0
            else:
                order_type = "buy"
                stock = random.choice(list(stock_prices.keys()))
                quantity = random.randint(1, 5)

            # Price close to current market
            price = stock_prices[stock] + random.uniform(-2, 2)
            if price <= 1:
                price = 1.0  # avoid zero or negative

            place_order(trader, order_book, order_type, stock, quantity, price)

        # Match orders
        trades = match_orders(order_book, traders)
        trade_history.extend(trades)

        # Count how many shares each trader traded this step
        # We'll do sum of shares as buyer + seller
        volumes_this_step = {t_id: 0 for t_id in traders}
        for tr in trades:
            volumes_this_step[tr["buyer"]] += tr["quantity"]
            volumes_this_step[tr["seller"]] += tr["quantity"]

        # Update each trader's volume for this step
        for t_id in traders:
            trader_volume_history[t_id].append(volumes_this_step[t_id])

        # Clear and settle
        batch_clearing_and_settlement(trades, traders)

        # Update the market prices (and store them in historical data)
        # If you have a function like "simulate_random_events" or "update_market_prices", call it
        # For now let's just do a small random wiggle:
        for st in stock_prices:
            # random +/- 3% shift
            shift = random.uniform(-0.03, 0.03)
            stock_prices[st] *= (1 + shift)
            if stock_prices[st] < 1:
                stock_prices[st] = 1.0
        # Save the updated stock prices in historical
        for st in stock_prices:
            historical_prices[st].append(stock_prices[st])

        # Now recalc each trader's net worth
        for t_id, trader in traders.items():
            worth = trader.cash
            for st, qty in trader.portfolio.items():
                worth += stock_prices[st] * qty
            net_worth_history[t_id].append(worth)

    # At the end, generate a trade report CSV (if you like)
    generate_trade_report(trade_history)

    # (You can still call your existing bar chart "visualize_trade_activity" for total shares)
    visualize_trade_activity(trade_history)

    # Now let's create our 4 new charts
    print("\nGenerating 4 overlayed charts...")

    # 1) Stock Price vs Time
    plot_stock_prices_over_time(historical_prices)

    # 2) Trader Volume vs Time
    plot_trader_volume_over_time(trader_volume_history)

    # 3) Trader Net Worth vs Time
    plot_trader_net_worth_over_time(net_worth_history)

    # 4) Final Portfolio Composition
    plot_final_portfolio_composition(traders, stock_prices)

    print("\nSimulation complete!")

if __name__ == "__main__":
    main()
