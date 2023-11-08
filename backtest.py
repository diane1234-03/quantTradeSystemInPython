import pandas as pd
import numpy as np


class BacktestBase:
    def __init__(self, symbol, start, end, amount, ftc=0.0, ptc=0.0, verbose=True):
        # 默认没有手续费
        self.symbol = symbol
        self.start = start
        self.end = end
        self.initial_amount = amount  # 静态初始资金
        self.amount = amount  # 动态资金
        self.ftc = ftc  # 固定交易成本
        self.ptc = ptc  # 可变交易成本，抽成比例
        self.units = 0  # 证券单位，例如手/
        self.position = 0  # 仓位
        self.trades = 0  # 交易次数
        self.verbose = verbose  # verbose暂时不理解
        self.get_data()

    def get_data(self):
        """Retrieves and prepares the data."""
        raw = pd.read_csv(
            "http://hilpisch.com/pyalgo_eikon_eod_data.csv",
            index_col=0,
            parse_dates=True,
        ).dropna()
        raw = pd.DataFrame(raw[self.symbol])
        raw = raw.loc[self.start : self.end]
        raw.rename(columns={self.symbol: "price"}, inplace=True)
        raw["return"] = np.log(raw / raw.shift(1))
        self.data = raw.dropna()

    def plot_data(self, cols=None):
        """Plots the closing prices for symbol."""
        if cols is None:
            cols = ["price"]
        self.data["price"].plot(figsize=(10, 6), title=self.symbol)

    def get_date_price(self, bar):
        """Return date and price for bar."""
        date = str(self.data.index[bar])[:10]
        price = self.data.price.iloc[bar]
        return date, price

    def print_balance(self, bar):
        """Print out current cash balance info."""
        date, price = self.get_date_price(bar)
        print(f"{date} | current balance {self.amount:.2f}")

    def print_net_wealth(self, bar):
        """Print out current cash balance info."""
        date, price = self.get_date_price(bar)
        net_wealth = self.units * price + self.amount
        print(f"{date} | current net wealth {net_wealth:.2f}")

    def place_buy_order(self, bar, units=None, amount=None):
        """Place a buy order."""
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount -= (units * price) * (1 + self.ptc) + self.ftc
        self.units += units
        self.trades += 1
        if self.verbose:
            print(f"{date} | selling {units} units at {price:.2f}")
        self.print_balance(bar)
        self.print_net_wealth(bar)

    def place_sell_order(self, bar, units=None, amount=None):
        """Place a sell order."""
        date, price = self.get_date_price(bar)
        if units is None:
            units = int(amount / price)
        self.amount += (units * price) * (1 - self.ptc) - self.ftc
        self.units -= units
        self.trades += 1
        if self.verbose:
            print(f"{date} | selling {units} units at {price:.2f}")
        self.print_balance(bar)
        self.print_net_wealth(bar)

    def close_out(self, bar):
        """Closing out a long or short position."""
        date, price = self.get_date_price(bar)
        self.amount += self.units * price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f"{date} | inventory {self.units} units at {price:.2f}")
            print("=" * 55)

        print("Final balance [$] {:.2f}".format(self.amount))
        perf = (self.amount - self.initial_amount) / self.initial_amount * 100
        print("Net Performance [%] {:.2f}".format(perf))
        print("Trades Executed [#] {:.2f}".format(self.trades))
        print("=" * 55)


if __name__ == "__main__":
    bb = BacktestBase("AAPL.O", "2010-1-1", "2019-12-31", 10000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()
