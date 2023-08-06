# Areix IO (Alpha Test)

[Documentation](http://alphagen.areix-ai.com/doc)

## Installation
Create a virtual environment 
```
virtualenv venv --python=python3
```
Activate the virtual environment 
```python
# Macbook / Linus
source venv/bin/activate 

# Windows
venv/Scripts/activate
```
Deactivate
```
deactivate
```
Install Areix-IO package
```
pip install Areix-IO
```


## Usage
Define your strategy class:
```python
from areix_io import (
    create_report_folder, SideType, set_token,
    Strategy, CryptoDataFeed, BackTest, BackTestBroker
)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import numpy as np

PRED_DAYS = 2 
PCT_CHANGE = 0.004
'''
Data pre processing step
'''
def bollinger_band(data, n_lookback, n_std):
    hlc3 = (data['high'] + data['low'] + data['close']) / 3
    mean, std = hlc3.rolling(n_lookback).mean(), hlc3.rolling(n_lookback).std()
    upper = mean + n_std*std
    lower = mean - n_std*std
    return upper, lower

def update_df(df):
    upper, lower = bollinger_band(df, 20, 2)

    df['ma10'] = df.close.rolling(10).mean()
    df['ma20'] = df.close.rolling(20).mean()
    df['ma50'] = df.close.rolling(50).mean()
    df['ma100'] = df.close.rolling(100).mean()

    df['x_ma10'] = (df.close - df.ma10) / df.close
    df['x_ma20'] = (df.close - df.ma20) / df.close
    df['x_ma50'] = (df.close - df.ma50) / df.close
    df['x_ma100'] = (df.close - df.ma100) / df.close

    df['x_delta_10'] = (df.ma10 - df.ma20) / df.close
    df['x_delta_20'] = (df.ma20 - df.ma50) / df.close
    df['x_delta_50'] = (df.ma50 - df.ma100) / df.close

    df['x_mom'] = df.close.pct_change(periods=2)
    df['x_bb_upper'] = (upper - df.close) / df.close
    df['x_bb_lower'] = (lower - df.close) / df.close
    df['x_bb_width'] = (upper - lower) / df.close

    # df = df.dropna().astype(float)
    return df

def get_X(data):
    return data.filter(like='x').values

def get_y(data):
    y = data.close.pct_change(PRED_DAYS).shift(-PRED_DAYS)  # Returns after roughly two days
    y[y.between(-PCT_CHANGE, PCT_CHANGE)] = 0             # Devalue returns smaller than 0.4%
    y[y > 0] = 1
    y[y < 0] = -1
    return y

def get_clean_Xy(df):
    X = get_X(df)
    y = get_y(df).values
    isnan = np.isnan(y)
    X = X[~isnan]
    y = y[~isnan]
    return X, y

class MLStrategy(Strategy):
    num_pre_train = 300

    def initialize(self):
        '''
        Model training step
        '''
        self.info('initialize')
        self.code = 'XRP/USDT'
        df = self.ctx.feed[self.code]
        self.ctx.feed[self.code] = update_df(df)

        self.y = get_y(df[self.num_pre_train-1:])
        self.y_true = self.y.values

        self.clf = KNeighborsClassifier(7)
        
        tmp = df.dropna().astype(float)
        X, y = get_clean_Xy(tmp[:self.num_pre_train])
        self.clf.fit(X, y)

        self.y_pred = []
    
    def before_trade(self, order):
        return True

    def on_order_ok(self, order):
        self.my_quantity = self.ctx.get_quantity(order['code'])
        self.info(
            f"{order['side'].name} order [number {order['id']}] ({order['order_type'].name}) executed [quantity {order['quantity']}] {order['code']} [price ${order['price']:2f}] [Cost ${order['cost']:2f}] [Commission: ${order['commission']}] [Available Cash: ${self.ctx.available_cash}] [Position: #{self.ctx.get_quantity(order['code'])}] [Gross P&L: ${order['pnl']}] [Net P&L: ${order['pnl_net']}]"
        )

        if not order['is_open']:
            self.info(f"Trade closed, pnl: {order['pnl']}========")

    def on_market_start(self):
        # self.info('on_market_start')
        pass

    def on_market_close(self):
        # self.info('on_market_close')
        pass

    def on_order_timeout(self, order):
        self.info(f'on_order_timeout. Order: {order}')
        pass

    def finish(self):
        self.info('finish')

    def on_bar(self, tick):
        '''
        Model scoring and decisioning step
        '''
        bar_data = self.ctx.bar_data[self.code]
        hist_data = self.ctx.hist_data[self.code]
        hist_df = self.ctx.history[self.code].copy()
   
        df = update_df(hist_df)
        # print(df)
        # if len(hist_data) < self.num_pre_train:
        #     return 
        bar_data = df.iloc[-1]
        check_res = np.any(np.isnan(bar_data))
        if check_res:
            return

        open, high, low, close = bar_data.open, bar_data.high, bar_data.low, bar_data.close
        X = get_X(bar_data)
        forecast = self.clf.predict([X])[0]
        self.y_pred.append(forecast)

        # self.ctx.cplot(forecast,'Forcast')
        # self.ctx.cplot(self.y[tick],'Groundtruth')
        # self.info(f"focasing result: {forecast}; {open}, {high}, {low}, {close}")

        upper, lower = close * (1 + np.r_[1, -1]*PCT_CHANGE)

        if forecast == 1 and not self.ctx.get_quantity(self.code):
            o1 = self.order_amount(code=self.code,amount=self.ctx.available_cash,side=SideType.BUY, asset_type='Crypto')
            self.info(f"BUY order [number {o1['id']}] created, [quantity {o1['quantity']}] [price {o1['price']}] [balance: {self.ctx.available_cash}]")
            
            osl = self.sell(code=self.code,quantity=o1['quantity'], price=lower, stop_price=lower, asset_type='Crypto')
            self.info(f"STOPLOSS order [number {osl['id']}] created, [quantity {osl['quantity']}] [price {osl['price']}] [balance: {self.ctx.available_cash}]")
            
        elif forecast == -1 and self.ctx.get_quantity(self.code):
            o2 = self.close(code=self.code, price=upper)
            self.info(f"SELL order [number {o2['id']}] created, [quantity {o2['quantity']}] [price {o2['price']}] [balance: {self.ctx.available_cash}]")

```

Run your strategy:
```python


if __name__ == '__main__':
    # tk = 'eyJ0eXAiOi......'
    # set_token(tk)
    
    base = create_report_folder()

    start_date = '2021-01-01'
    end_date = '2021-07-01'

    sdf = CryptoDataFeed(
        symbols=['XRP/USDT', 'BTC/USDT'], 
        start_date=start_date, 
        end_date=end_date,  
        interval='4h', 
        # interval='1m', 
        order_ascending=True, 
        store_path=base
    )
    feed, idx = sdf.fetch_data()
    benchmark = feed.pop('BTC/USDT')

    broker = BackTestBroker(
        commission_rate=0.001, 
        min_commission=None, 
        trade_at='close', 
        cash=5000, 
        short_cash=False, 
        slippage=0.0)

    mytest = BackTest(
        feed, 
        MLStrategy, 
        benchmark=('BTC/USDT', benchmark), 
        broker=broker, 
        tradedays=idx, 
        store_path=base
    )

    mytest.start()


```

Retrieve statistic results:
```python
    prefix = ''
    stats = mytest.ctx.statistic.stats(pprint=True, annualization=252, risk_free=0.0442)
    stats['model_name'] = 'Simple KNN Signal Generation Strategy'
    stats['algorithm'] = ['KNN', 'Simple Moving Average', 'Bollinger Band']
    print(stats)
    mytest.contest_output(is_plot=True)
```
Result:
```
start                                                2021-01-01 00:00:00+08:00
end                                                  2021-07-01 00:00:00+08:00
duration                                                     181 days 00:00:00
trading_pairs                                                       (XRP/USDT)
benchmark                                                             BTC/USDT
beginning_balance                                                         5000
ending_balance                                                     9622.580449
total_net_profit                                                   4622.580449
gross_profit                                                      68000.370935
gross_loss                                                       -63377.790486
profit_factor                                                         1.072937
return_on_initial_capital                                             0.924516
annualized_return                                                     0.163897
total_return                                                          0.924516
max_return                                                            2.472148
min_return                                                           -0.000999
number_trades                                                              398
number_winning_trades                                                      179
number_losing_trades                                                        65
avg_daily_trades                                                      3.344538
avg_weekly_trades                                                    15.920000
avg_monthly_trades                                                   66.333333
win_ratio                                                             0.449749
loss_ratio                                                            0.163317
win_days                                                                    53
loss_days                                                                   34
max_win_in_day                                                     2236.412270
max_loss_in_day                                                   -2620.335665
max_consecutive_win_days                                                    31
max_consecutive_loss_days                                                    2
avg_profit_per_trade                                               1024.975575
trading_period                                         0 years 6 months 0 days
avg_daily_pnl($)                                                      4.256520
avg_daily_pnl                                                         0.000897
avg_weekly_pnl($)                                                   177.791556
avg_weekly_pnl                                                        0.035889
avg_monthly_pnl($)                                                  509.819819
avg_monthly_pnl                                                       0.106800
avg_quarterly_pnl($)                                              -1589.908852
avg_quarterly_pnl                                                    -0.124188
avg_annualy_pnl($)                                                         NaN
avg_annualy_pnl                                                            NaN
sharpe_ratio                                                          0.482168
sortino_ratio                                                         0.826390
annualized_volatility                                                 0.377342
omega_ratio                                                           0.021357
downside_risk                                                         0.273549
information_ratio                                                     0.019368
beta                                                                  0.444923
alpha                                                                -0.997702
calmar_ratio                                                          0.340877
tail_ratio                                                            1.295467
stability_of_timeseries                                               0.568724
max_drawdown                                                          0.480809
max_drawdown_period          (2021-04-12 16:00:00+08:00, 2021-06-23 04:00:0...
max_drawdown_duration                                         71 days 12:00:00
sqn                                                                   1.321773
model_name                               Simple KNN Signal Generation Strategy
algorithm                         [KNN, Simple Moving Average, Bollinger Band]

```