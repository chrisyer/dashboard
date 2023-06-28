import pandas_ta as ta
from quants_lab.strategy.directional_strategy_base import DirectionalStrategyBase

from quants_lab.utils import data_management


class Bollinger(DirectionalStrategyBase):
    def __init__(self,
                 exchange="binance_perpetual",
                 trading_pair="ETH-USDT",
                 interval="1h",
                 bb_length=24,
                 bb_std=2.0):
        self.exchange = exchange
        self.trading_pair = trading_pair
        self.interval = interval
        self.bb_length = bb_length
        self.bb_std = bb_std

    def get_raw_data(self):
        df = data_management.get_dataframe(
            exchange=self.exchange,
            trading_pair=self.trading_pair,
            interval=self.interval,
        )
        return df

    def add_indicators(self, df):
        df.ta.bbands(length=self.bb_length, std=self.bb_std, append=True)
        return df

    def add_signals(self, df):
        df["side"] = 0
        long_condition = df[f"BBP_{self.bb_length}_{self.bb_std}"] < 0.05
        short_condition = df[f"BBP_{self.bb_length}_{self.bb_std}"] > 0.95
        df.loc[long_condition, "side"] = 1
        df.loc[short_condition, "side"] = -1
        return df
