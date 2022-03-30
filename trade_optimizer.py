import sys
import time

import pandas as pd


class Trade:
    def __init__(self, buying_time, selling_time, buying_price, selling_price, profit):
        self.buying_time = buying_time
        self.selling_time = selling_time
        self.buying_price = buying_price
        self.selling_price = selling_price
        self.profit = profit

    def __str__(self):
        return (
            f'Buy at: {self.buying_time} ({self.buying_price:.4f}), '
            f'Sell at: {self.selling_time} ({self.selling_price:.4f}), '
            f'Profit: {self.profit:.4f}'
        )


def get_optimized_trades(csv_file_name):
    trade_data = pd.read_csv(csv_file_name)
    best_trades = get_best_trades(trade_data)
    chosen_trades = get_non_overlapping_trades(best_trades)
    return chosen_trades


def get_best_trades(trade_data):
    """
    Returns a list of best trades, order by the better trades on top.

    Given a buying time, a "best trade" is a trade that has the selling time
    between 30-60 minutes from the buying time, and returns the highest profit.

    For each time point in `trade_data`, find the best trade whose buying time is that time point.
    """

    best_trades = []

    for _, buying_point in trade_data.iterrows():
        buying_time = buying_point['Time']
        buying_price = buying_point['Price']

        possible_selling_points = trade_data[
            (trade_data['Time'] > buying_time + 30) &
            (trade_data['Time'] < buying_time + 60)
        ]

        if possible_selling_points.empty:
            continue

        get_profit = lambda selling_point: selling_point['Price'] - buying_price
        profits = possible_selling_points.assign(Profit=get_profit).reset_index(drop=True)

        if profits.empty:
            continue

        max_profit_index = profits['Profit'].idxmax()
        max_profit = profits.iloc[max_profit_index]

        selling_time = max_profit['Time']
        selling_price = max_profit['Price']
        profit = max_profit['Profit']

        if profit <= 0:  # You want profitable trades don't you :)
            continue

        trade = Trade(int(buying_time), int(selling_time), buying_price, selling_price, profit)
        best_trades.append(trade)

    # Sort the trades with higher profit to top
    best_trades.sort(key=lambda trade: trade.profit, reverse=True)

    return best_trades


def get_non_overlapping_trades(trades):
    """
    Returns a list of trades whose buying time to selling time don't overlap each other.
    """
    traded_slots = []
    chosen_trades = []

    for trade in trades:
        trade_slots = range(trade.buying_time, trade.selling_time + 1)
        if any(slot in traded_slots for slot in trade_slots):  # Overlapped
            continue

        chosen_trades.append(trade)
        traded_slots.extend(trade_slots)

    return chosen_trades


def print_result(trades):
    trades.sort(key=lambda trade: trade.buying_time)
    total_profit = 0

    for trade in trades:
        print(trade)
        total_profit += trade.profit

    print(f'Total profit: {total_profit:.4f}',)


if __name__ == '__main__':
    csv_file_name = sys.argv[1]

    start = time.perf_counter_ns()

    optimized_trades = get_optimized_trades(csv_file_name)
    print_result(optimized_trades)

    end = time.perf_counter_ns()
    print(f'Time taken: {(end-start)/1e9:.4f} seconds')
