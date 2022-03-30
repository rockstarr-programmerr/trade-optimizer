import sys
import time

import pandas as pd


class Trade:
    def __init__(self, buying_time, selling_time, profit):
        self.buying_time = buying_time
        self.selling_time = selling_time
        self.profit = profit

    def __str__(self):
        return f'Buy: {self.buying_time}, Sell: {self.selling_time}, Profit: {self.profit:.4f}'


def optimize_trade(csv_file_name):
    trade_data = pd.read_csv(csv_file_name)

    best_trades = []

    ########################################################

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
        profit = max_profit['Profit']

        if profit <= 0:
            continue

        trade = Trade(int(buying_time), int(selling_time), profit)
        best_trades.append(trade)

    ########################################################

    best_trades.sort(key=lambda trade: trade.profit, reverse=True)

    ########################################################

    traded_slots = []
    chosen_trades = []

    for trade in best_trades:
        trade_slots = range(trade.buying_time, trade.selling_time + 1)
        if any(slot in traded_slots for slot in trade_slots):
            continue

        chosen_trades.append(trade)
        traded_slots.extend(trade_slots)

    ########################################################

    chosen_trades.sort(key=lambda trade: trade.buying_time)
    total_profit = 0
    for trade in chosen_trades:
        print(trade)
        total_profit += trade.profit
    print(f'Total profit: {total_profit:.4f}',)


if __name__ == '__main__':
    csv_file_name = sys.argv[1]

    s = time.perf_counter_ns()
    optimize_trade(csv_file_name)
    e = time.perf_counter_ns()
    print(f'Time taken: {(e-s)/1e9:.4f} seconds')
