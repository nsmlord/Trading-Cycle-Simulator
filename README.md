
# Trade Cycle Simulator

This is a Python simulation that models traders placing buy and sell orders. It includes an order book for matching trades, updates stock prices, and generates reports via charts and CSV files.

## Contents

1. Features
2. Project Structure
3. Installation
4. Usage
5. Modules
6. How It Works
7. License

## Features

- Traders with unique IDs, cash, and stock portfolios
- Matching of buy and sell orders based on price and time
- Random stock price changes
- Clearing and settlement of trades, including fee processing
- Reports in CSV format and visualizations using Matplotlib

## Project Structure

```
.
├── clearing.py
├── main.py
├── market.py
├── matching_engine.py
├── order.py
├── reporting.py
├── trader.py
├── utils.py
├── visualizations.py
└── README.md
```

- main.py: Entry point for running the simulation
- trader.py: Defines traders and their portfolios
- order.py: Manages order creation and operations
- matching_engine.py: Matches buy and sell orders
- clearing.py: Handles post-trade processing
- market.py: Updates stock prices and simulates market events
- reporting.py: Exports data and creates summaries
- utils.py: Provides utility functions
- visualizations.py: Generates plots for analysis

## Installation

1. Clone or download the repository.
2. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate   # For Windows
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the simulation with:
   ```
   python main.py
   ```
2. View the console output for stock prices, orders, and trades.
3. Check the CSV reports and Matplotlib charts for market analysis.

## Modules

- main.py: Runs the simulation and records data
- visualizations.py: Creates graphs for stock prices, trader activity, and portfolios
- matching_engine.py: Matches and executes trades
- trader.py: Defines trader behavior
- order.py: Manages orders and the order book
- clearing.py: Processes trades and updates accounts
- market.py: Simulates stock price changes
- reporting.py: Generates CSV reports
- utils.py: Provides helper functions for the simulation

## How It Works

1. Initialization: Sets up traders, stock prices, and an order book
2. Simulation Steps: Updates stock prices, places orders, matches trades, and records data
3. Reporting: Exports trade data and generates charts for analysis

## License

This project is released under the MIT License. Contributions are welcome.
